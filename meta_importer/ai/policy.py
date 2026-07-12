from __future__ import annotations

import re
from typing import Any
from urllib.parse import urlparse

from .contracts import (
    CONFIDENCE_BANDS,
    EVIDENCE_STRENGTHS,
    FIELD_NAMES,
    FIELD_STATUSES,
    REVIEW_STATUSES,
    RISK_FLAGS,
)

OBJECTIVES = {"awareness", "traffic", "engagement", "leads", "app_promotion", "sales"}
PLACEMENTS = {"feed", "story", "reels", "marketplace", "right_column", "search"}
SLUG_FIELDS = {"campaign_key", "adset_key", "utm_campaign"}
CRITICAL_FIELDS = {"campaign_key", "adset_key", "objective", "destination_url"}
OPTIONAL_FIELDS = set(FIELD_NAMES) - CRITICAL_FIELDS
SYNTHETIC_DECLARATION = "Data classification: synthetic_fixture_only"


class ProposalPolicyError(ValueError):
    """Raised when a model proposal fails schema or policy validation."""


def validate_model_output(payload: dict[str, Any], brief: str) -> None:
    if set(payload) != {"fields", "assumptions", "risk_flags"}:
        raise ProposalPolicyError("model output root keys do not match the contract")
    fields = payload.get("fields")
    if not isinstance(fields, dict) or set(fields) != set(FIELD_NAMES):
        raise ProposalPolicyError("model output fields do not match the contract")
    assumptions = payload.get("assumptions")
    if not isinstance(assumptions, list) or not all(isinstance(item, str) for item in assumptions):
        raise ProposalPolicyError("assumptions must be a list of strings")
    risk_flags = payload.get("risk_flags")
    if (
        not isinstance(risk_flags, list)
        or len(risk_flags) != len(set(risk_flags))
        or any(flag not in RISK_FLAGS for flag in risk_flags)
    ):
        raise ProposalPolicyError("risk_flags are invalid")
    for name in FIELD_NAMES:
        _validate_field(name, fields[name], brief)


def _validate_field(name: str, field: Any, brief: str) -> None:
    required = {
        "status",
        "value",
        "evidence_quote",
        "evidence_strength",
        "confidence_band",
        "confidence_calibrated",
        "reason_code",
        "review_status",
    }
    if not isinstance(field, dict) or set(field) != required:
        raise ProposalPolicyError(f"{name}: field contract mismatch")
    if field["status"] not in FIELD_STATUSES:
        raise ProposalPolicyError(f"{name}: invalid status")
    if field["evidence_strength"] not in EVIDENCE_STRENGTHS:
        raise ProposalPolicyError(f"{name}: invalid evidence strength")
    if field["confidence_band"] not in CONFIDENCE_BANDS:
        raise ProposalPolicyError(f"{name}: invalid confidence band")
    if field["confidence_calibrated"] is not False:
        raise ProposalPolicyError(f"{name}: confidence cannot be called calibrated")
    if field["review_status"] not in REVIEW_STATUSES or field["review_status"] != "pending":
        raise ProposalPolicyError(f"{name}: model cannot review its own proposal")
    for key in ("value", "evidence_quote", "reason_code"):
        if not isinstance(field[key], str):
            raise ProposalPolicyError(f"{name}: {key} must be a string")
    if field["status"] == "abstained":
        if field["value"] or field["confidence_band"] != "abstain":
            raise ProposalPolicyError(f"{name}: abstention must have no value")
        return
    if not field["value"]:
        raise ProposalPolicyError(f"{name}: proposed values cannot be empty")
    if field["evidence_quote"] not in brief:
        raise ProposalPolicyError(f"{name}: evidence quote is not present in the brief")
    if field["evidence_strength"] not in {"direct", "normalized"}:
        raise ProposalPolicyError(f"{name}: proposed values require direct or normalized evidence")
    if field["confidence_band"] not in {"high", "medium"}:
        raise ProposalPolicyError(f"{name}: proposed values require high or medium confidence")
    _validate_value(name, field["value"])
    if _normalize_evidence(name, field["evidence_quote"]) != field["value"]:
        raise ProposalPolicyError(f"{name}: evidence quote does not support the proposed value")


def _validate_value(name: str, value: str) -> None:
    if name in SLUG_FIELDS and not re.fullmatch(r"[a-z0-9][a-z0-9_-]{1,79}", value):
        raise ProposalPolicyError(f"{name}: value is outside the slug allowlist")
    if name == "objective" and value not in OBJECTIVES:
        raise ProposalPolicyError("objective is outside the allowlist")
    if name == "placement" and value not in PLACEMENTS:
        raise ProposalPolicyError("placement is outside the allowlist")
    if name == "country" and not re.fullmatch(r"[A-Z]{2}", value):
        raise ProposalPolicyError("country must be ISO-like uppercase alpha-2")
    if name == "language" and not re.fullmatch(r"[a-z]{2}", value):
        raise ProposalPolicyError("language must be lowercase alpha-2")
    if name == "destination_url":
        parsed = urlparse(value)
        if parsed.scheme != "https" or parsed.hostname != "example.invalid":
            raise ProposalPolicyError("destination_url must use the synthetic example.invalid host")


def release_decision(fields: dict[str, dict[str, Any]], risk_flags: list[str]) -> str:
    if risk_flags:
        return "abstained"
    if any(fields[name]["status"] == "abstained" for name in CRITICAL_FIELDS):
        return "abstained"
    return "pending_human_review"


def detect_input_risks(brief: str) -> list[str]:
    lowered = brief.lower()
    flags = []
    if re.search(r"\b(publish|go live|mettre en ligne)\b", lowered):
        flags.append("live_mutation_requested")
    if re.search(r"\b(act_\d+|access[_ -]?token|oauth|api key)\b", lowered):
        flags.append("credential_or_account_identifier")
    if (
        re.search(r"\b(customer data|client data|real customer|données client)\b", lowered)
        or re.search(r"\b[\w.+-]+@[\w.-]+\.[a-z]{2,}\b", lowered)
        or re.search(r"\+?\d[\d .()-]{7,}\d", brief)
        or re.search(r"(?im)^\s*client\s*:\s*\S+", brief)
    ):
        flags.append("customer_data_signal")
    if re.search(r"\b(ignore (all|the|previous)|system prompt|developer message)\b", lowered):
        flags.append("prompt_injection_signal")
    for raw_url in re.findall(r"https://[^\s]+", brief):
        parsed = urlparse(raw_url.rstrip(".,;)"))._replace(fragment="")
        hostname = parsed.hostname or ""
        if parsed.username or parsed.password or not hostname.endswith(".invalid"):
            flags.append("non_synthetic_destination")
    return sorted(set(flags))


def has_synthetic_declaration(brief: str) -> bool:
    return SYNTHETIC_DECLARATION in brief.splitlines()


def validate_mapping_draft(draft: dict[str, str]) -> dict[str, Any]:
    issues = []
    for name in CRITICAL_FIELDS:
        if not draft.get(name):
            issues.append(f"missing_critical_field:{name}")
    for name, value in draft.items():
        if name not in FIELD_NAMES:
            issues.append(f"unknown_field:{name}")
            continue
        try:
            _validate_value(name, value)
        except ProposalPolicyError as exc:
            issues.append(str(exc))
    return {
        "contract_version": "brief_mapping_deterministic_validation.v1",
        "status": "pass" if not issues else "blocked",
        "checks": [
            "critical_fields_present",
            "field_allowlists",
            "synthetic_destination_hostname",
            "no_unknown_fields",
        ],
        "issues": issues,
    }


def _normalize_evidence(name: str, evidence: str) -> str:
    evidence = evidence.strip()
    if name in SLUG_FIELDS | {"objective", "placement"}:
        return evidence.lower().replace(" ", "_")
    if name == "country":
        return evidence.upper()
    if name == "language":
        return evidence.lower()
    return evidence
