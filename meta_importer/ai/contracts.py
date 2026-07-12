from __future__ import annotations

import hashlib
import json
from typing import Any

CONTRACT_VERSION = "brief_mapping_proposal.v1"
PROMPT_VERSION = "brief_mapping_prompt.v1"
FIELD_NAMES = (
    "campaign_key",
    "adset_key",
    "objective",
    "country",
    "language",
    "placement",
    "destination_url",
    "utm_campaign",
)
FIELD_STATUSES = {"proposed", "abstained"}
EVIDENCE_STRENGTHS = {"direct", "normalized", "inferred", "missing", "conflict"}
CONFIDENCE_BANDS = {"high", "medium", "low", "abstain"}
REVIEW_STATUSES = {"pending", "accepted", "rejected"}
RISK_FLAGS = {
    "live_mutation_requested",
    "credential_or_account_identifier",
    "customer_data_signal",
    "prompt_injection_signal",
    "non_synthetic_destination",
}


def field_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": sorted(FIELD_STATUSES)},
            "value": {"type": "string"},
            "evidence_quote": {"type": "string"},
            "evidence_strength": {
                "type": "string",
                "enum": sorted(EVIDENCE_STRENGTHS),
            },
            "confidence_band": {
                "type": "string",
                "enum": sorted(CONFIDENCE_BANDS),
            },
            "confidence_calibrated": {"type": "boolean", "enum": [False]},
            "reason_code": {"type": "string"},
            "review_status": {"type": "string", "enum": sorted(REVIEW_STATUSES)},
        },
        "required": [
            "status",
            "value",
            "evidence_quote",
            "evidence_strength",
            "confidence_band",
            "confidence_calibrated",
            "reason_code",
            "review_status",
        ],
        "additionalProperties": False,
    }


def model_output_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "properties": {
            "fields": {
                "type": "object",
                "properties": {name: field_schema() for name in FIELD_NAMES},
                "required": list(FIELD_NAMES),
                "additionalProperties": False,
            },
            "assumptions": {"type": "array", "items": {"type": "string"}},
            "risk_flags": {
                "type": "array",
                "items": {"type": "string", "enum": sorted(RISK_FLAGS)},
            },
        },
        "required": ["fields", "assumptions", "risk_flags"],
        "additionalProperties": False,
    }


def schema_sha256() -> str:
    encoded = json.dumps(model_output_schema(), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode()).hexdigest()
