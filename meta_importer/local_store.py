from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from .asset_validation import validate_asset_metadata
from .launch_workspace import LaunchPlan, export_plan_dict
from .workspace_state import export_workspace_state_dict, workspace_batch_id


def write_batch_store(
    plan: LaunchPlan,
    store_dir: str | Path,
    *,
    asset_metadata_path: str | Path | None = None,
) -> dict[str, object]:
    batch_id = workspace_batch_id(plan)
    batch_dir = Path(store_dir) / batch_id
    snapshots_dir = batch_dir / "snapshots"
    audit_dir = batch_dir / "audit"
    snapshots_dir.mkdir(parents=True, exist_ok=True)
    audit_dir.mkdir(parents=True, exist_ok=True)

    source_snapshot = snapshots_dir / "source_manifest.csv"
    if plan.source_manifest and Path(plan.source_manifest).is_file():
        shutil.copy2(plan.source_manifest, source_snapshot)

    launch_plan_path = batch_dir / "launch_plan.json"
    review_state_path = batch_dir / "review_state.json"
    asset_validation_path = batch_dir / "asset_validation.json"
    audit_log_path = audit_dir / "events.jsonl"
    store_manifest_path = batch_dir / "batch_store.json"

    launch_plan = export_plan_dict(plan)
    review_state = export_workspace_state_dict(plan)
    asset_validation = (
        validate_asset_metadata(plan, asset_metadata_path)
        if asset_metadata_path
        else _asset_validation_not_run()
    )

    _write_json(launch_plan_path, launch_plan)
    _write_json(review_state_path, review_state)
    _write_json(asset_validation_path, asset_validation)

    events = [
        _audit_event(batch_id, "batch_store_created", "system", "Local batch store initialized."),
        _audit_event(batch_id, "source_snapshot_written", "system", "Source manifest snapshot persisted."),
        _audit_event(batch_id, "launch_plan_persisted", "system", "Dry-run launch plan persisted."),
        _audit_event(batch_id, "review_state_persisted", "system", "Review state persisted."),
        _audit_event(batch_id, "asset_validation_recorded", "system", "Asset validation report persisted."),
    ]
    appended_events = _append_audit_events(audit_log_path, events)

    manifest = {
        "contract_version": "local_batch_store.v1",
        "batch_id": batch_id,
        "mode": "local_filesystem_store_only",
        "mutation_allowed": False,
        "meta_api_compatibility": "not_claimed",
        "root": str(batch_dir),
        "source_manifest": plan.source_manifest,
        "source_snapshot": str(source_snapshot),
        "launch_plan": str(launch_plan_path),
        "review_state": str(review_state_path),
        "asset_validation": str(asset_validation_path),
        "audit_log": str(audit_log_path),
        "audit_events_appended": appended_events,
        "asset_validation_status": asset_validation["status"],
        "row_count": plan.summary["row_count"],
    }
    _write_json(store_manifest_path, manifest)
    return manifest


def _write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def _append_audit_events(path: Path, events: list[dict[str, object]]) -> int:
    existing_count = 0
    if path.exists():
        existing_count = sum(1 for line in path.read_text().splitlines() if line.strip())

    with path.open("a") as handle:
        for offset, event in enumerate(events, start=1):
            event = dict(event)
            event["sequence"] = existing_count + offset
            event["event_id"] = f"evt_{event['batch_id']}_{existing_count + offset:06d}"
            handle.write(json.dumps(event, sort_keys=True) + "\n")
    return len(events)


def _audit_event(
    batch_id: str, event_type: str, actor_role: str, message: str
) -> dict[str, object]:
    return {
        "batch_id": batch_id,
        "event_type": event_type,
        "actor_role": actor_role,
        "message": message,
        "occurred_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    }


def _asset_validation_not_run() -> dict[str, object]:
    return {
        "contract_version": "synthetic_asset_validation.v1",
        "status": "not_run",
        "rows_checked": 0,
        "unique_assets": 0,
        "blocker_count": 0,
        "warning_count": 0,
        "issue_count": 0,
        "issues": [],
        "summary": {},
    }
