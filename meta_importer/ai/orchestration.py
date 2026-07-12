from __future__ import annotations

import hashlib
import json
import time
from typing import Any, Protocol, cast

from .contracts import CONTRACT_VERSION, PROMPT_VERSION, schema_sha256
from .policy import (
    detect_input_risks,
    has_synthetic_declaration,
    release_decision,
    validate_model_output,
)


class ProposalProvider(Protocol):
    name: str
    model: str

    def propose(self, brief: str) -> dict[str, object]: ...


def propose_brief(brief: str, provider: ProposalProvider) -> dict[str, Any]:
    if not 1 <= len(brief) <= 20_000:
        raise ValueError("brief must contain between 1 and 20,000 characters")
    input_risks = detect_input_risks(brief)
    started = time.monotonic()
    model_output = provider.propose(brief)
    validate_model_output(model_output, brief)
    fields = cast(dict[str, dict[str, Any]], model_output["fields"])
    provider_risks = cast(list[str], model_output["risk_flags"])
    risk_flags = sorted(set(provider_risks) | set(input_risks))
    brief_hash = hashlib.sha256(brief.encode()).hexdigest()
    schema_hash = schema_sha256()
    prompt_hash = str(
        getattr(
            provider,
            "prompt_sha256",
            hashlib.sha256(PROMPT_VERSION.encode()).hexdigest(),
        )
    )
    effective_output = {
        "fields": fields,
        "assumptions": model_output["assumptions"],
        "risk_flags": risk_flags,
    }
    output_hash = hashlib.sha256(
        json.dumps(effective_output, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    proposal_id = hashlib.sha256(
        (
            f"{brief_hash}|{schema_hash}|{prompt_hash}|{provider.name}|"
            f"{provider.model}|{output_hash}"
        ).encode()
    ).hexdigest()[:20]
    latency_ms = (
        0.0
        if provider.name == "deterministic_baseline"
        else round((time.monotonic() - started) * 1_000, 2)
    )
    return {
        "contract_version": CONTRACT_VERSION,
        "proposal_id": f"proposal_{proposal_id}",
        "status": release_decision(fields, risk_flags),
        "prompt_version": PROMPT_VERSION,
        "prompt_sha256": prompt_hash,
        "provider": provider.name,
        "model": provider.model,
        "provider_response_id": getattr(provider, "response_id", ""),
        "brief_sha256": brief_hash,
        "schema_sha256": schema_hash,
        "output_sha256": output_hash,
        "data_classification": (
            "synthetic_fixture_only"
            if has_synthetic_declaration(brief)
            and not set(risk_flags)
            & {
                "credential_or_account_identifier",
                "customer_data_signal",
                "non_synthetic_destination",
            }
            else "unverified_or_blocked_input"
        ),
        "fields": fields,
        "assumptions": model_output["assumptions"],
        "risk_flags": risk_flags,
        "latency_ms": latency_ms,
        "usage": getattr(provider, "usage", {}),
        "mutation_allowed": False,
        "human_review_required": True,
        "deterministic_validation_required": True,
        "confidence_claim": "uncalibrated_band_only",
        "guardrails": [
            "The proposal cannot call Meta or any external tool.",
            "Every field remains pending until a human accepts or rejects it.",
            "Deterministic manifest validators remain the final authority.",
            "Any provider, schema, policy, or evidence failure abstains closed.",
        ],
    }
