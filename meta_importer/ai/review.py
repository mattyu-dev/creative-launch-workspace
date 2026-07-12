from __future__ import annotations

import hashlib
import json
from typing import Any

from .contracts import CONTRACT_VERSION, FIELD_NAMES, PROMPT_VERSION, schema_sha256
from .policy import (
    CRITICAL_FIELDS,
    detect_input_risks,
    has_synthetic_declaration,
    release_decision,
    validate_mapping_draft,
    validate_model_output,
)


class HumanReviewError(ValueError):
    """Raised when a human-review receipt violates the proposal contract."""


def review_proposal(
    proposal: dict[str, Any], *, brief: str, reviewer: str, decisions: dict[str, str]
) -> dict[str, Any]:
    validate_proposal_envelope(proposal, brief)
    if not reviewer.strip() or len(reviewer) > 120:
        raise HumanReviewError("reviewer must be a non-empty name or role")
    if set(decisions) != set(FIELD_NAMES):
        raise HumanReviewError("every proposal field requires accept or reject")
    if any(value not in {"accepted", "rejected"} for value in decisions.values()):
        raise HumanReviewError("review decisions must be accepted or rejected")

    reviewed_fields = {}
    draft = {}
    blocked_reasons = []
    if proposal["status"] != "pending_human_review":
        blocked_reasons.append("proposal_not_releasable")
    for name in FIELD_NAMES:
        field = dict(proposal["fields"][name])
        decision = decisions[name]
        if decision == "accepted" and field["status"] != "proposed":
            raise HumanReviewError(f"cannot accept abstained field: {name}")
        field["review_status"] = decision
        reviewed_fields[name] = field
        if decision == "accepted":
            draft[name] = field["value"]
        elif name in CRITICAL_FIELDS:
            blocked_reasons.append(f"{name}_rejected")

    deterministic_validation = validate_mapping_draft(draft)
    if deterministic_validation["status"] != "pass":
        blocked_reasons.append("deterministic_mapping_validation_failed")
    status = "accepted_for_manifest_draft" if not blocked_reasons else "blocked"
    receipt = {
        "contract_version": "brief_mapping_review.v1",
        "proposal_id": proposal["proposal_id"],
        "proposal_output_sha256": proposal["output_sha256"],
        "brief_sha256": proposal["brief_sha256"],
        "reviewer": reviewer,
        "status": status,
        "fields": reviewed_fields,
        "manifest_draft": draft if status == "accepted_for_manifest_draft" else {},
        "blocked_reasons": blocked_reasons,
        "deterministic_validation": deterministic_validation,
        "mutation_allowed": False,
        "deterministic_validation_required": True,
    }
    payload_hash = receipt_payload_sha256(receipt)
    receipt["receipt_payload_sha256"] = payload_hash
    receipt["review_id"] = "review_" + payload_hash[:20]
    return receipt


def receipt_payload_sha256(receipt: dict[str, Any]) -> str:
    payload = {
        key: value
        for key, value in receipt.items()
        if key not in {"review_id", "receipt_payload_sha256"}
    }
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def validate_proposal_envelope(proposal: dict[str, Any], brief: str) -> None:
    if proposal.get("contract_version") != CONTRACT_VERSION:
        raise HumanReviewError("unsupported proposal contract")
    if proposal.get("prompt_version") != PROMPT_VERSION:
        raise HumanReviewError("proposal prompt version is stale or invalid")
    if proposal.get("schema_sha256") != schema_sha256():
        raise HumanReviewError("proposal schema hash does not match the current contract")
    brief_hash = hashlib.sha256(brief.encode()).hexdigest()
    if proposal.get("brief_sha256") != brief_hash:
        raise HumanReviewError("proposal does not belong to the supplied brief")
    if proposal.get("mutation_allowed") is not False or proposal.get("human_review_required") is not True:
        raise HumanReviewError("proposal safety envelope is invalid")
    if not isinstance(proposal.get("provider"), str) or not proposal["provider"]:
        raise HumanReviewError("proposal provider is missing")
    if not isinstance(proposal.get("model"), str) or not proposal["model"]:
        raise HumanReviewError("proposal model is missing")
    if not isinstance(proposal.get("prompt_sha256"), str) or len(proposal["prompt_sha256"]) != 64:
        raise HumanReviewError("proposal prompt hash is invalid")

    effective_output = {
        "fields": proposal.get("fields"),
        "assumptions": proposal.get("assumptions"),
        "risk_flags": proposal.get("risk_flags"),
    }
    try:
        validate_model_output(effective_output, brief)
    except ValueError as exc:
        raise HumanReviewError(f"proposal policy validation failed: {exc}") from exc
    expected_risks = sorted(
        set(proposal["risk_flags"]) | set(detect_input_risks(brief))
    )
    if proposal["risk_flags"] != expected_risks:
        raise HumanReviewError("proposal risk flags are incomplete or unordered")
    expected_status = release_decision(proposal["fields"], expected_risks)
    if proposal.get("status") != expected_status:
        raise HumanReviewError("proposal release status does not match policy")
    expected_classification = (
        "synthetic_fixture_only"
        if has_synthetic_declaration(brief)
        and not set(expected_risks)
        & {
            "credential_or_account_identifier",
            "customer_data_signal",
            "non_synthetic_destination",
        }
        else "unverified_or_blocked_input"
    )
    if proposal.get("data_classification") != expected_classification:
        raise HumanReviewError("proposal data classification is invalid")

    output_hash = hashlib.sha256(
        json.dumps(effective_output, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    if proposal.get("output_sha256") != output_hash:
        raise HumanReviewError("proposal output hash does not match its payload")
    expected_id = hashlib.sha256(
        (
            f"{brief_hash}|{proposal['schema_sha256']}|{proposal['prompt_sha256']}|"
            f"{proposal['provider']}|{proposal['model']}|{output_hash}"
        ).encode()
    ).hexdigest()[:20]
    if proposal.get("proposal_id") != f"proposal_{expected_id}":
        raise HumanReviewError("proposal identity does not match its provenance")
