from __future__ import annotations

import csv
import hashlib
import io
import os
import tempfile
from pathlib import Path
from typing import Any, cast

from ..launch_workspace import build_launch_plan, export_plan_dict, read_manifest
from .contracts import FIELD_NAMES
from .policy import CRITICAL_FIELDS, validate_mapping_draft
from .review import receipt_payload_sha256, review_proposal, validate_proposal_envelope


class MaterializationError(ValueError):
    """Raised when a review receipt cannot safely seed a manifest draft."""


def review_and_materialize(
    proposal: dict[str, Any],
    *,
    brief: str,
    reviewer: str,
    decisions: dict[str, str],
    template: str | Path,
    output: str | Path,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Review and materialize in one process; persisted receipts are evidence only."""
    receipt = review_proposal(
        proposal, brief=brief, reviewer=reviewer, decisions=dict(decisions)
    )
    if receipt["status"] != "accepted_for_manifest_draft":
        raise MaterializationError("current review decision blocks materialization")
    result = _materialize_reviewed_mapping(
        receipt,
        proposal=proposal,
        brief=brief,
        template=template,
        output=output,
    )
    return receipt, result


def _materialize_reviewed_mapping(
    receipt: dict[str, Any],
    *,
    proposal: dict[str, Any],
    brief: str,
    template: str | Path,
    output: str | Path,
) -> dict[str, Any]:
    _validate_receipt(receipt, proposal=proposal, brief=brief)
    template_path = Path(template)
    output_path = Path(output)
    with template_path.open(newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)
    if not rows:
        raise MaterializationError("manifest template must contain at least one creative row")
    missing_columns = sorted(set(FIELD_NAMES) - set(fieldnames))
    if missing_columns:
        raise MaterializationError(
            "manifest template is missing mapping columns: " + ", ".join(missing_columns)
        )

    draft = receipt["manifest_draft"]
    for row in rows:
        for name, value in draft.items():
            existing = (row.get(name) or "").strip()
            if existing and existing != value:
                raise MaterializationError(
                    f"template value for {name} conflicts with the reviewed mapping"
                )
            row[name] = value

    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    display_path = _canonical_path(output_path)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            newline="",
            dir=output_path.parent,
            prefix=f".{output_path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            handle.write(buffer.getvalue())
            temporary_path = Path(handle.name)
        plan = build_launch_plan(
            read_manifest(temporary_path), source_manifest=display_path
        )
        issue_severity = cast(dict[str, int], plan.summary["issue_severity"])
        blockers = int(issue_severity.get("blocker", 0))
        if blockers:
            raise MaterializationError(
                f"deterministic launch validation found {blockers} blocker(s)"
            )
        os.replace(temporary_path, output_path)
        temporary_path = None
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)

    plan_payload = export_plan_dict(plan)
    return {
        "contract_version": "reviewed_mapping_materialization.v1",
        "review_id": receipt["review_id"],
        "template_sha256": hashlib.sha256(template_path.read_bytes()).hexdigest(),
        "manifest_sha256": hashlib.sha256(output_path.read_bytes()).hexdigest(),
        "manifest_path": display_path,
        "row_count": len(rows),
        "validation_summary": plan.summary,
        "offline_launch_plan": plan_payload,
        "mutation_allowed": False,
    }


def _validate_receipt(
    receipt: dict[str, Any], *, proposal: dict[str, Any], brief: str
) -> None:
    try:
        validate_proposal_envelope(proposal, brief)
    except ValueError as exc:
        raise MaterializationError(f"source proposal validation failed: {exc}") from exc
    if receipt.get("contract_version") != "brief_mapping_review.v1":
        raise MaterializationError("unsupported review receipt contract")
    if receipt.get("status") != "accepted_for_manifest_draft":
        raise MaterializationError("review receipt is not accepted for manifest drafting")
    if receipt.get("mutation_allowed") is not False:
        raise MaterializationError("review receipt mutation guard is invalid")
    if receipt.get("proposal_id") != proposal.get("proposal_id"):
        raise MaterializationError("review receipt does not match the source proposal")
    if receipt.get("proposal_output_sha256") != proposal.get("output_sha256"):
        raise MaterializationError("review receipt output hash does not match the source proposal")
    if receipt.get("brief_sha256") != proposal.get("brief_sha256"):
        raise MaterializationError("review receipt brief hash does not match the source proposal")
    payload_hash = receipt_payload_sha256(receipt)
    if receipt.get("receipt_payload_sha256") != payload_hash:
        raise MaterializationError("review receipt payload hash does not match its contents")
    if receipt.get("review_id") != "review_" + payload_hash[:20]:
        raise MaterializationError("review receipt identity does not match its contents")
    draft = receipt.get("manifest_draft")
    if not isinstance(draft, dict):
        raise MaterializationError("review receipt manifest draft is invalid")
    validation = validate_mapping_draft(draft)
    if validation["status"] != "pass" or receipt.get("deterministic_validation") != validation:
        raise MaterializationError("review receipt deterministic validation is stale or invalid")
    fields = receipt.get("fields")
    if not isinstance(fields, dict) or set(fields) != set(FIELD_NAMES):
        raise MaterializationError("review receipt fields are invalid")
    for name in FIELD_NAMES:
        decision = fields[name].get("review_status")
        expected_field = dict(proposal["fields"][name])
        expected_field["review_status"] = decision
        if fields[name] != expected_field:
            raise MaterializationError(
                f"reviewed field {name} does not match the source proposal"
            )
        if decision == "accepted" and draft.get(name) != fields[name].get("value"):
            raise MaterializationError(f"accepted field {name} does not match the draft")
        if decision == "rejected" and name in draft:
            raise MaterializationError(f"rejected field {name} leaked into the draft")
    if any(fields[name].get("review_status") != "accepted" for name in CRITICAL_FIELDS):
        raise MaterializationError("every critical mapping field must be accepted")


def _canonical_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return path.name
