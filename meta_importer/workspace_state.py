from __future__ import annotations

import hashlib
from collections import defaultdict
from datetime import date

from .launch_workspace import (
    AdCandidate,
    Issue,
    LaunchPlan,
    _data_classification,
    _row_by_source,
    _source_manifest_sha256,
)


REVIEW_STATUS_BY_BATCH_STATE = {
    "launch_ready": "ready_to_review",
    "needs_review": "needs_confirmation",
    "blocked": "needs_fix",
}

REVIEW_ROLES = [
    {
        "role": "Media Buyer",
        "owns": ["destination_url", "placement", "utm_mapping", "post_lineage"],
    },
    {
        "role": "Creative Ops Manager",
        "owns": ["asset_path", "format", "naming_taxonomy", "source_lineage"],
    },
    {
        "role": "Approver",
        "owns": ["approval_status", "reviewer", "approved_at"],
    },
    {
        "role": "Account Manager",
        "owns": ["client_readiness", "batch_export_confirmation"],
    },
]


def workspace_batch_id(plan: LaunchPlan) -> str:
    manifest_hash = _source_manifest_sha256(plan.source_manifest)
    basis_parts = [
        manifest_hash or plan.source_manifest,
        str(len(plan.candidates)),
        *(candidate.idempotency_key for candidate in plan.candidates),
    ]
    return hashlib.sha256("|".join(basis_parts).encode()).hexdigest()[:16]


def export_workspace_state_dict(plan: LaunchPlan) -> dict[str, object]:
    batch_id = workspace_batch_id(plan)
    manifest_hash = _source_manifest_sha256(plan.source_manifest)
    data_classification = _data_classification(plan.rows)
    issues_by_row: dict[int, list[Issue]] = defaultdict(list)
    for issue in plan.issues:
        issues_by_row[issue.source_row].append(issue)

    return {
        "product": "Creative Launch Workspace for Meta Ads",
        "mode": "local_review_state_only",
        "contract_version": "workspace_review_state.v1",
        "generated_at": date.today().isoformat(),
        "batch_id": batch_id,
        "source_manifest": plan.source_manifest,
        "source_manifest_sha256": manifest_hash,
        "data_classification": data_classification,
        "mutation_allowed": False,
        "meta_api_compatibility": "not_claimed",
        "local_storage_key": f"meta-importer-review-state:{batch_id}",
        "roles": REVIEW_ROLES,
        "summary": plan.summary,
        "guardrails": [
            "No Meta API calls are made.",
            (
                "No credentials, OAuth tokens, live ad account identifiers, or customer assets are loaded."
                if data_classification == "synthetic_fixture_only"
                else "Operator-supplied rows remain local; no credentials, OAuth tokens, or live ad account identifiers are loaded."
            ),
            "Review decisions are local operator state and do not publish ads.",
            "Live Meta mutation requires separate platform proof and explicit HITL approval.",
        ],
        "review_statuses": [
            _review_state_for(candidate, issues_by_row[candidate.source_row], plan)
            for candidate in plan.candidates
        ],
        "audit_events": [
            _audit_event(batch_id, "batch_created", "system", "Workspace state created from manifest."),
            _audit_event(batch_id, "review_queue_seeded", "system", "Initial row review queue seeded."),
        ],
        "export_policy": {
            "export_name": "review_state.json",
            "offline_only": True,
            "can_seed_future_backend": True,
            "can_execute_meta_mutation": False,
            "requires_human_export_confirmation": True,
        },
    }


def _review_state_for(
    candidate: AdCandidate, row_issues: list[Issue], plan: LaunchPlan
) -> dict[str, object]:
    row = _row_by_source(plan.rows, candidate.source_row)
    owners = sorted({issue.owner for issue in row_issues}) or ["Media Buyer"]
    return {
        "source_row": candidate.source_row,
        "creative_id": candidate.creative_id,
        "campaign_key": candidate.campaign_key,
        "adset_key": candidate.adset_key,
        "format": candidate.format,
        "asset_path": candidate.asset_path,
        "account_id_alias": candidate.account_id_alias or "unmapped",
        "objective": candidate.objective or "unmapped",
        "placement": candidate.placement or "unmapped",
        "language": candidate.language or "unmapped",
        "country": candidate.country or "unmapped",
        "primary_text": row.primary_text,
        "headline": row.headline,
        "destination_url": candidate.destination_url,
        "final_url_preview": candidate.final_url_preview,
        "utm_campaign": candidate.utm_campaign or "unmapped",
        "utm_status": "mapped"
        if candidate.final_url_preview != candidate.destination_url
        else "unmapped",
        "post_id": candidate.post_id or candidate.post_id_type or "new",
        "source_lineage": candidate.source_row_id or str(candidate.source_row),
        "idempotency_key": candidate.idempotency_key,
        "operation_intent": candidate.operation_intent,
        "batch_state": candidate.batch_state,
        "issue_count": candidate.issue_count,
        "issue_codes": [issue.code for issue in row_issues],
        "issues": [_issue_dict(issue) for issue in row_issues],
        "owners": owners,
        "primary_owner": owners[0],
        "proposed_fix": row_issues[0].proposed_fix
        if row_issues
        else "Include in dry-run launch candidate.",
        "review_status": REVIEW_STATUS_BY_BATCH_STATE[candidate.batch_state],
        "decision": "pending",
        "note": "",
        "updated_by_role": "",
        "updated_at": "",
    }


def _issue_dict(issue: Issue) -> dict[str, object]:
    return {
        "source_row": issue.source_row,
        "creative_id": issue.creative_id,
        "severity": issue.severity,
        "code": issue.code,
        "owner": issue.owner,
        "message": issue.message,
        "proposed_fix": issue.proposed_fix,
    }


def _audit_event(
    batch_id: str, event_type: str, actor_role: str, message: str
) -> dict[str, object]:
    event_id = hashlib.sha256(f"{batch_id}|{event_type}".encode()).hexdigest()[:12]
    return {
        "event_id": f"evt_{event_id}",
        "event_type": event_type,
        "actor_role": actor_role,
        "message": message,
        "occurred_at": date.today().isoformat(),
    }
