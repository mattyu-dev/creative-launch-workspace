from __future__ import annotations

import hashlib
import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

from .contracts import FIELD_NAMES, PROMPT_VERSION, schema_sha256
from .orchestration import propose_brief

THRESHOLDS = {
    "contract_valid_rate": 1.0,
    "field_exact_match_rate": 1.0,
    "evidence_grounded_rate": 1.0,
    "risk_flag_recall": 1.0,
    "status_match_rate": 1.0,
    "deterministic_replay_rate": 1.0,
    "mutation_guard_rate": 1.0,
}


def load_cases(path: str | Path, *, suite: str = "baseline") -> list[dict[str, Any]]:
    lines = Path(path).read_text().splitlines()
    all_cases = [json.loads(line) for line in lines if line.strip()]
    cases = [case for case in all_cases if case.get("suite", "baseline") == suite]
    if not cases or len({case["id"] for case in cases}) != len(cases):
        raise ValueError("eval dataset must contain unique cases")
    return cases


LIVE_THRESHOLDS = {
    "contract_valid_rate": 1.0,
    "field_exact_match_rate": 0.95,
    "evidence_grounded_rate": 1.0,
    "risk_flag_recall": 1.0,
    "status_match_rate": 0.95,
    "high_band_precision": 0.98,
    "mutation_guard_rate": 1.0,
}


def evaluate_live_provider(
    cases: list[dict[str, Any]], provider_factory: Callable[[], Any], *, repetitions: int = 3
) -> dict[str, Any]:
    if repetitions < 1:
        raise ValueError("repetitions must be positive")
    attempts = len(cases) * repetitions
    field_total = attempts * len(FIELD_NAMES)
    valid = field_matches = evidence_total = evidence_grounded = 0
    expected_risks_total = risk_hits = status_matches = mutation_guards = 0
    high_total = high_correct = 0
    failures = []
    models = set()
    prompt_hashes = set()
    schema_hashes = set()
    latencies = []
    usage_totals: dict[str, int] = {}

    for case in cases:
        for repetition in range(1, repetitions + 1):
            try:
                proposal = propose_brief(case["brief"], provider_factory())
                valid += 1
            except Exception as exc:
                failures.append(
                    {"id": case["id"], "repetition": repetition, "error": f"{type(exc).__name__}:{exc}"}
                )
                continue
            models.add(proposal["model"])
            prompt_hashes.add(proposal["prompt_sha256"])
            schema_hashes.add(proposal["schema_sha256"])
            latencies.append(float(proposal["latency_ms"]))
            for key, value in proposal.get("usage", {}).items():
                if isinstance(value, int):
                    usage_totals[key] = usage_totals.get(key, 0) + value
            for name in FIELD_NAMES:
                field = proposal["fields"][name]
                actual = field["value"] if field["status"] == "proposed" else ""
                correct = actual == case["expected_fields"][name]
                field_matches += int(correct)
                if field["status"] == "proposed":
                    evidence_total += 1
                    evidence_grounded += int(field["evidence_quote"] in case["brief"])
                if field["confidence_band"] == "high":
                    high_total += 1
                    high_correct += int(correct)
            expected_risks = set(case["expected_risks"])
            actual_risks = set(proposal["risk_flags"])
            expected_risks_total += len(expected_risks)
            risk_hits += len(expected_risks & actual_risks)
            status_matches += int(proposal["status"] == case["expected_status"])
            mutation_guards += int(
                proposal["mutation_allowed"] is False
                and proposal["human_review_required"] is True
            )

    metrics = {
        "contract_valid_rate": valid / attempts,
        "field_exact_match_rate": field_matches / field_total,
        "evidence_grounded_rate": evidence_grounded / evidence_total if evidence_total else 1.0,
        "risk_flag_recall": risk_hits / expected_risks_total if expected_risks_total else 1.0,
        "status_match_rate": status_matches / attempts,
        "high_band_precision": high_correct / high_total if high_total else 0.0,
        "mutation_guard_rate": mutation_guards / attempts,
    }
    return {
        "contract_version": "brief_mapping_live_eval.v1",
        "benchmark": "synthetic_live_provider",
        "case_count": len(cases),
        "repetitions": repetitions,
        "attempt_count": attempts,
        "models_returned": sorted(models),
        "prompt_sha256": sorted(prompt_hashes),
        "schema_sha256": sorted(schema_hashes),
        "dataset_sha256": hashlib.sha256(
            "\n".join(json.dumps(case, sort_keys=True) for case in cases).encode()
        ).hexdigest(),
        "metrics": metrics,
        "thresholds": LIVE_THRESHOLDS,
        "passed": all(metrics[name] >= value for name, value in LIVE_THRESHOLDS.items()),
        "latency_ms": {
            "minimum": min(latencies) if latencies else None,
            "maximum": max(latencies) if latencies else None,
            "mean": sum(latencies) / len(latencies) if latencies else None,
        },
        "usage_totals": usage_totals,
        "failures": failures,
        "claim_boundary": "Synthetic model benchmark; not production or customer-data proof.",
    }


def evaluate(
    cases: list[dict[str, Any]], provider_factory: Callable[[], Any]
) -> dict[str, Any]:
    field_total = len(cases) * len(FIELD_NAMES)
    field_matches = evidence_total = evidence_grounded = 0
    valid = status_matches = replay_matches = mutation_guards = 0
    expected_risks_total = risk_hits = 0
    failures = []
    categories: dict[str, dict[str, int]] = {}

    for case in cases:
        category = case["category"]
        categories.setdefault(category, {"cases": 0, "passed": 0})["cases"] += 1
        case_failures = []
        try:
            first = propose_brief(case["brief"], provider_factory())
            second = propose_brief(case["brief"], provider_factory())
            valid += 1
        except Exception as exc:
            failures.append({"id": case["id"], "errors": [f"contract:{type(exc).__name__}:{exc}"]})
            continue

        for name in FIELD_NAMES:
            expected = case["expected_fields"][name]
            actual_field = first["fields"][name]
            actual = actual_field["value"] if actual_field["status"] == "proposed" else ""
            if actual == expected:
                field_matches += 1
            else:
                case_failures.append(f"{name}:expected={expected!r}:actual={actual!r}")
            if actual_field["status"] == "proposed":
                evidence_total += 1
                if actual_field["evidence_quote"] in case["brief"]:
                    evidence_grounded += 1

        expected_risks = set(case["expected_risks"])
        actual_risks = set(first["risk_flags"])
        expected_risks_total += len(expected_risks)
        risk_hits += len(expected_risks & actual_risks)
        if actual_risks != expected_risks:
            case_failures.append(
                f"risks:expected={sorted(expected_risks)}:actual={sorted(actual_risks)}"
            )
        if first["status"] == case["expected_status"]:
            status_matches += 1
        else:
            case_failures.append(
                f"status:expected={case['expected_status']}:actual={first['status']}"
            )
        comparable = ("latency_ms",)
        if all(first[key] == second[key] for key in first if key not in comparable):
            replay_matches += 1
        else:
            case_failures.append("non_deterministic_replay")
        if first["mutation_allowed"] is False and first["human_review_required"] is True:
            mutation_guards += 1
        else:
            case_failures.append("mutation_guard_failed")

        if case_failures:
            failures.append({"id": case["id"], "errors": case_failures})
        else:
            categories[category]["passed"] += 1

    count = len(cases)
    metrics = {
        "contract_valid_rate": valid / count,
        "field_exact_match_rate": field_matches / field_total,
        "evidence_grounded_rate": evidence_grounded / evidence_total if evidence_total else 1.0,
        "risk_flag_recall": risk_hits / expected_risks_total if expected_risks_total else 1.0,
        "status_match_rate": status_matches / count,
        "deterministic_replay_rate": replay_matches / count,
        "mutation_guard_rate": mutation_guards / count,
    }
    passed = not failures and all(metrics[name] >= threshold for name, threshold in THRESHOLDS.items())
    return {
        "contract_version": "brief_mapping_eval.v1",
        "benchmark": "synthetic_repo_native",
        "provider": provider_factory().name,
        "model": provider_factory().model,
        "case_count": count,
        "split_counts": {
            split: sum(1 for case in cases if case["split"] == split)
            for split in sorted({case["split"] for case in cases})
        },
        "dataset_sha256": hashlib.sha256(
            "\n".join(json.dumps(case, sort_keys=True) for case in cases).encode()
        ).hexdigest(),
        "prompt_version": PROMPT_VERSION,
        "schema_sha256": schema_sha256(),
        "thresholds": THRESHOLDS,
        "metrics": metrics,
        "categories": categories,
        "failures": failures,
        "passed": passed,
        "claim_boundary": "Deterministic baseline proof only; this is not a model-quality claim.",
    }
