from __future__ import annotations

import hashlib
import json
import sqlite3
from pathlib import Path

from .clock import now_iso
from .launch_workspace import LaunchPlan
from .review_policy import ReviewPolicyError, validate_review_transition
from .workspace_state import export_workspace_state_dict, workspace_batch_id

SCHEMA_VERSION = "sqlite_workspace_store.v1"


class SQLiteStoreError(ValueError):
    """Raised when the local SQLite workspace store guardrails fail."""


class SQLiteWorkspaceStore:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(self.path)
        self.connection.row_factory = sqlite3.Row

    def close(self) -> None:
        self.connection.close()

    def init_schema(self) -> None:
        self.connection.executescript(
            """
            create table if not exists schema_migrations (
              version text primary key,
              applied_at text not null
            );
            create table if not exists tenants (
              tenant_id text primary key,
              display_name text not null,
              data_classification text not null,
              created_at text not null
            );
            create table if not exists batches (
              batch_id text primary key,
              tenant_id text not null references tenants(tenant_id),
              source_manifest text not null,
              source_manifest_sha256 text not null,
              contract_version text not null,
              row_count integer not null,
              summary_json text not null,
              created_at text not null
            );
            create table if not exists review_rows (
              batch_id text not null references batches(batch_id),
              source_row integer not null,
              creative_id text not null,
              review_status text not null,
              decision text not null,
              note text not null,
              updated_by_role text not null,
              updated_at text not null,
              payload_json text not null,
              primary key (batch_id, source_row)
            );
            create table if not exists audit_events (
              event_id text primary key,
              batch_id text not null references batches(batch_id),
              tenant_id text not null references tenants(tenant_id),
              event_type text not null,
              actor_role text not null,
              source_row integer,
              payload_json text not null,
              occurred_at text not null
            );
            """
        )
        self.connection.execute(
            "insert or ignore into schema_migrations(version, applied_at) values(?, ?)",
            (SCHEMA_VERSION, _now()),
        )
        self.connection.commit()

    def ensure_fixture_tenant(
        self,
        tenant_id: str = "tenant_fixture_default",
        *,
        display_name: str = "Synthetic Fixture Tenant",
    ) -> None:
        if not tenant_id.startswith("tenant_fixture_"):
            raise SQLiteStoreError("Only tenant_fixture_* ids are allowed in the offline store.")
        self.connection.execute(
            """
            insert or ignore into tenants(tenant_id, display_name, data_classification, created_at)
            values(?, ?, ?, ?)
            """,
            (tenant_id, display_name, "synthetic_fixture_only", _now()),
        )
        self.connection.commit()

    def upsert_batch(
        self, plan: LaunchPlan, *, tenant_id: str = "tenant_fixture_default"
    ) -> dict[str, object]:
        self.init_schema()
        self.ensure_fixture_tenant(tenant_id)
        state = export_workspace_state_dict(plan)
        if state["data_classification"] != "synthetic_fixture_only":
            raise SQLiteStoreError("SQLite proof store only accepts synthetic fixture batches.")
        batch_id = workspace_batch_id(plan)
        now = _now()
        with self.connection:
            self.connection.execute(
                """
                insert into batches(
                  batch_id, tenant_id, source_manifest, source_manifest_sha256,
                  contract_version, row_count, summary_json, created_at
                )
                values(?, ?, ?, ?, ?, ?, ?, ?)
                on conflict(batch_id) do update set
                  tenant_id=excluded.tenant_id,
                  source_manifest=excluded.source_manifest,
                  source_manifest_sha256=excluded.source_manifest_sha256,
                  contract_version=excluded.contract_version,
                  row_count=excluded.row_count,
                  summary_json=excluded.summary_json
                """,
                (
                    batch_id,
                    tenant_id,
                    str(state["source_manifest"]),
                    str(state["source_manifest_sha256"]),
                    str(state["contract_version"]),
                    len(state["review_statuses"]),
                    json.dumps(state["summary"], sort_keys=True),
                    now,
                ),
            )
            for row in state["review_statuses"]:
                self.connection.execute(
                    """
                    insert into review_rows(
                      batch_id, source_row, creative_id, review_status, decision,
                      note, updated_by_role, updated_at, payload_json
                    )
                    values(?, ?, ?, ?, ?, ?, ?, ?, ?)
                    on conflict(batch_id, source_row) do update set
                      creative_id=excluded.creative_id,
                      review_status=excluded.review_status,
                      decision=excluded.decision,
                      payload_json=excluded.payload_json
                    """,
                    (
                        batch_id,
                        int(row["source_row"]),
                        str(row["creative_id"]),
                        str(row["review_status"]),
                        str(row["decision"]),
                        str(row["note"]),
                        str(row["updated_by_role"]),
                        str(row["updated_at"]),
                        json.dumps(row, sort_keys=True),
                    ),
                )
            self._append_audit(
                batch_id,
                tenant_id,
                "sqlite_batch_upserted",
                "system",
                None,
                {"row_count": len(state["review_statuses"])},
            )
        return {
            "contract_version": SCHEMA_VERSION,
            "database": str(self.path),
            "batch_id": batch_id,
            "tenant_id": tenant_id,
            "row_count": len(state["review_statuses"]),
            "mutation_allowed": False,
            "meta_api_compatibility": "not_claimed",
        }

    def record_row_decision(
        self,
        batch_id: str,
        source_row: int,
        *,
        review_status: str,
        decision: str,
        actor_role: str,
        note: str = "",
    ) -> None:
        batch = self._batch(batch_id)
        row = self.connection.execute(
            "select payload_json from review_rows where batch_id=? and source_row=?",
            (batch_id, source_row),
        ).fetchone()
        if row is None:
            raise SQLiteStoreError(f"row {source_row} not found in batch {batch_id}")
        payload = json.loads(row["payload_json"])
        try:
            validate_review_transition(
                batch_state=str(payload["batch_state"]),
                review_status=review_status,
                decision=decision,
                actor_role=actor_role,
                note=note,
            )
        except ReviewPolicyError as exc:
            raise SQLiteStoreError(f"review transition blocked: {exc}") from exc
        payload.update(
            {
                "review_status": review_status,
                "decision": decision,
                "note": note,
                "updated_by_role": actor_role,
                "updated_at": _now(),
            }
        )
        with self.connection:
            self.connection.execute(
                """
                update review_rows
                set review_status=?, decision=?, note=?, updated_by_role=?, updated_at=?, payload_json=?
                where batch_id=? and source_row=?
                """,
                (
                    review_status,
                    decision,
                    note,
                    actor_role,
                    payload["updated_at"],
                    json.dumps(payload, sort_keys=True),
                    batch_id,
                    source_row,
                ),
            )
            self._append_audit(
                batch_id,
                str(batch["tenant_id"]),
                "sqlite_row_decision_updated",
                actor_role,
                source_row,
                {"review_status": review_status, "decision": decision},
            )

    def export_batch_state(self, batch_id: str) -> dict[str, object]:
        batch = self._batch(batch_id)
        rows = self.connection.execute(
            "select payload_json from review_rows where batch_id=? order by source_row",
            (batch_id,),
        ).fetchall()
        audit_rows = self.connection.execute(
            "select event_type, actor_role, source_row, payload_json, occurred_at from audit_events where batch_id=? order by rowid",
            (batch_id,),
        ).fetchall()
        return {
            "contract_version": SCHEMA_VERSION,
            "mode": "local_sqlite_store_only",
            "batch_id": batch_id,
            "tenant_id": batch["tenant_id"],
            "data_classification": "synthetic_fixture_only",
            "source_manifest": batch["source_manifest"],
            "source_manifest_sha256": batch["source_manifest_sha256"],
            "mutation_allowed": False,
            "meta_api_compatibility": "not_claimed",
            "review_statuses": [json.loads(row["payload_json"]) for row in rows],
            "audit_events": [
                {
                    "event_type": row["event_type"],
                    "actor_role": row["actor_role"],
                    "source_row": row["source_row"],
                    "payload": json.loads(row["payload_json"]),
                    "occurred_at": row["occurred_at"],
                }
                for row in audit_rows
            ],
        }

    def _batch(self, batch_id: str) -> sqlite3.Row:
        row = self.connection.execute(
            "select * from batches where batch_id=?", (batch_id,)
        ).fetchone()
        if row is None:
            raise SQLiteStoreError(f"batch not found: {batch_id}")
        return row

    def _append_audit(
        self,
        batch_id: str,
        tenant_id: str,
        event_type: str,
        actor_role: str,
        source_row: int | None,
        payload: dict[str, object],
    ) -> None:
        occurred_at = _now()
        event_count = self.connection.execute(
            "select count(*) from audit_events where batch_id=?", (batch_id,)
        ).fetchone()[0]
        basis = f"{batch_id}|{event_count + 1}|{event_type}|{source_row}|{occurred_at}|{json.dumps(payload, sort_keys=True)}"
        event_id = "evt_sqlite_" + hashlib.sha256(basis.encode()).hexdigest()[:16]
        self.connection.execute(
            """
            insert into audit_events(
              event_id, batch_id, tenant_id, event_type, actor_role, source_row,
              payload_json, occurred_at
            )
            values(?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                event_id,
                batch_id,
                tenant_id,
                event_type,
                actor_role,
                source_row,
                json.dumps(payload, sort_keys=True),
                occurred_at,
            ),
        )


def _now() -> str:
    return now_iso()
