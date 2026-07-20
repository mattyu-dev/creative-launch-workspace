from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .launch_workspace import build_launch_plan, read_manifest
from .workspace_state import export_workspace_state_dict

DEMO_FIXTURE = "fixtures/fake_agency_creatives/manifest_v2.csv"

ISSUE_TITLES = {
    "duplicate_asset": "Possible duplicate",
    "missing_approval": "Missing approval",
    "destination_mismatch": "Destination mismatch",
    "naming_error": "Naming error",
    "unsupported_format": "Unsupported format",
}

STATUS_LABELS = {
    "launch_ready": "Ready",
    "needs_review": "Needs decision",
    "blocked": "Blocked",
}

DECISIONS = {
    "confirm": {
        "review_status": "confirmed_ready",
        "decision": "approved_for_dry_run_export",
        "receipt_title": "Intentional reuse confirmed",
        "timeline": "Reuse confirmed",
    },
    "return": {
        "review_status": "needs_fix",
        "decision": "requires_fix",
        "receipt_title": "Returned for replacement",
        "timeline": "Return requested",
    },
    "block": {
        "review_status": "blocked",
        "decision": "blocked_from_export",
        "receipt_title": "Blocked from dry-run export",
        "timeline": "Row blocked",
    },
}


def _issue_title(review_state: dict[str, Any]) -> str:
    codes = review_state["issue_codes"]
    return ISSUE_TITLES.get(codes[0], codes[0].replace("_", " ").title()) if codes else ""


def _display_destination(url: str) -> str:
    return url.removeprefix("https://").removeprefix("http://")


def _queue_entry(review_state: dict[str, Any], rows_by_source: dict[int, object]) -> dict[str, Any]:
    row = rows_by_source[review_state["source_row"]]
    return {
        "source_row": review_state["source_row"],
        "creative_id": review_state["creative_id"],
        "name": review_state["headline"],
        "issue_title": _issue_title(review_state),
        "issue_message": review_state["issues"][0]["message"] if review_state["issues"] else "",
        "proposed_fix": review_state["proposed_fix"],
        "owner": review_state["primary_owner"],
        "batch_state": review_state["batch_state"],
        "status_label": STATUS_LABELS[review_state["batch_state"]],
        "primary_text": review_state["primary_text"],
        "format": review_state["format"],
        "facts": {
            "campaign": review_state["campaign_key"],
            "adset": review_state["adset_key"],
            "market": review_state["country"],
            "post_mode": row.post_id_type,
            "post_id": review_state["post_id"],
            "destination": _display_destination(str(review_state["destination_url"])),
        },
    }


def build_demo_payload(fixture: str = DEMO_FIXTURE) -> dict[str, Any]:
    """One truth source for every demo surface (landing, walkthrough, receipt).

    Everything shown by the public demo is derived from the real launch plan of
    the committed fixture: names, statuses, owners, counts, batch id and the
    manifest hash. Nothing is retyped by hand.
    """

    fixture_path = Path(fixture)
    plan = build_launch_plan(read_manifest(fixture_path), source_manifest=str(fixture_path))
    state = export_workspace_state_dict(plan)
    rows_by_source = {row.source_row: row for row in plan.rows}

    by_state: dict[str, list[dict[str, Any]]] = {
        "launch_ready": [],
        "needs_review": [],
        "blocked": [],
    }
    for review_state in state["review_statuses"]:
        by_state[review_state["batch_state"]].append(review_state)

    exception = _queue_entry(by_state["needs_review"][0], rows_by_source)
    walkthrough_neighbours = [
        _queue_entry(review_state, rows_by_source) for review_state in by_state["launch_ready"][:2]
    ]

    return {
        "contract_version": "landing_demo_payload.v1",
        "source_manifest": str(fixture_path),
        "batch_id": state["batch_id"],
        "source_manifest_sha256": state["source_manifest_sha256"],
        "data_classification": state["data_classification"],
        "workspace_storage_key": state["local_storage_key"],
        "workspace_contract_version": state["contract_version"],
        "counts": {
            "total": len(state["review_statuses"]),
            "ready": len(by_state["launch_ready"]),
            "needs_decision": len(by_state["needs_review"]),
            "blocked": len(by_state["blocked"]),
        },
        "walkthrough": {
            "rows": [
                walkthrough_neighbours[0],
                exception,
                walkthrough_neighbours[1],
            ],
            "exception": exception,
        },
        "queue": {
            "ready": [_queue_entry(item, rows_by_source) for item in by_state["launch_ready"][:4]],
            "needs_decision": [
                _queue_entry(item, rows_by_source) for item in by_state["needs_review"]
            ],
            "blocked": [_queue_entry(item, rows_by_source) for item in by_state["blocked"][:4]],
        },
        "decisions": DECISIONS,
        "reviewer_role": exception["owner"],
    }


def demo_payload_json(fixture: str = DEMO_FIXTURE) -> str:
    return json.dumps(build_demo_payload(fixture), sort_keys=True, separators=(",", ":"))
