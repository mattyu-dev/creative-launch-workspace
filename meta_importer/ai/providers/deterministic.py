from __future__ import annotations

import hashlib
import re
from urllib.parse import urlparse

from ..contracts import FIELD_NAMES
from ..policy import OBJECTIVES, PLACEMENTS, detect_input_risks

ALIASES = {
    "campaign": "campaign_key",
    "campagne": "campaign_key",
    "adset": "adset_key",
    "ensemble": "adset_key",
    "objective": "objective",
    "objectif": "objective",
    "country": "country",
    "pays": "country",
    "language": "language",
    "langue": "language",
    "placement": "placement",
    "destination": "destination_url",
    "url": "destination_url",
    "utm": "utm_campaign",
}


class DeterministicBaselineProvider:
    """A transparent, non-AI contract baseline used by CI and local evals."""

    name = "deterministic_baseline"
    model = "label_parser_v1"
    prompt_sha256 = hashlib.sha256(b"deterministic_baseline_no_prompt").hexdigest()

    def propose(self, brief: str) -> dict[str, object]:
        candidates: dict[str, list[tuple[str, str]]] = {name: [] for name in FIELD_NAMES}
        for line in brief.splitlines():
            match = re.match(r"\s*([A-Za-zÀ-ÿ_ ]+)\s*:\s*(.*?)\s*$", line)
            if not match:
                continue
            alias = match.group(1).strip().lower().replace(" ", "_")
            field_name = ALIASES.get(alias)
            if field_name and match.group(2):
                candidates[field_name].append((match.group(2).strip(), match.group(2).strip()))

        fields = {
            name: self._field(name, candidates[name])
            for name in FIELD_NAMES
        }
        return {
            "fields": fields,
            "assumptions": [],
            "risk_flags": detect_input_risks(brief),
        }

    def _field(self, name: str, values: list[tuple[str, str]]) -> dict[str, object]:
        normalized = [(_normalize(name, value), evidence) for value, evidence in values]
        distinct = {value for value, _ in normalized}
        if not values:
            return _abstention("missing_in_brief", "missing")
        if len(distinct) != 1:
            return _abstention("conflicting_values", "conflict")
        value, evidence = normalized[0]
        if not _allowed(name, value):
            return _abstention("outside_allowlist", "direct")
        return {
            "status": "proposed",
            "value": value,
            "evidence_quote": evidence,
            "evidence_strength": "direct" if value == evidence else "normalized",
            "confidence_band": "high",
            "confidence_calibrated": False,
            "reason_code": "explicit_label",
            "review_status": "pending",
        }


def _normalize(name: str, value: str) -> str:
    value = value.strip()
    if name in {"campaign_key", "adset_key", "objective", "placement", "utm_campaign"}:
        return value.lower().replace(" ", "_")
    if name == "country":
        return value.upper()
    if name == "language":
        return value.lower()
    return value


def _abstention(reason: str, strength: str) -> dict[str, object]:
    return {
        "status": "abstained",
        "value": "",
        "evidence_quote": "",
        "evidence_strength": strength,
        "confidence_band": "abstain",
        "confidence_calibrated": False,
        "reason_code": reason,
        "review_status": "pending",
    }


def _allowed(name: str, value: str) -> bool:
    if name in {"campaign_key", "adset_key", "utm_campaign"}:
        return bool(re.fullmatch(r"[a-z0-9][a-z0-9_-]{1,79}", value))
    if name == "objective":
        return value in OBJECTIVES
    if name == "placement":
        return value in PLACEMENTS
    if name == "country":
        return bool(re.fullmatch(r"[A-Z]{2}", value))
    if name == "language":
        return bool(re.fullmatch(r"[a-z]{2}", value))
    if name == "destination_url":
        parsed = urlparse(value)
        return parsed.scheme == "https" and parsed.hostname == "example.invalid"
    return True
