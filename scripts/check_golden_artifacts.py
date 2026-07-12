#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from meta_importer.launch_workspace import build_launch_plan, read_manifest


EDGE_FIXTURE = ROOT / "fixtures/fake_agency_creatives/manifest_edge_cases.csv"
EDGE_GOLDEN = ROOT / "fixtures/fake_agency_creatives/golden_edge_summary.json"


def main() -> int:
    plan = build_launch_plan(read_manifest(EDGE_FIXTURE), source_manifest=str(EDGE_FIXTURE))
    actual = _golden_summary(plan)
    expected = json.loads(EDGE_GOLDEN.read_text())
    if actual != expected:
        print("# Golden artifact check")
        print("- FAIL: edge fixture summary changed")
        print(json.dumps({"expected": expected, "actual": actual}, indent=2, sort_keys=True))
        return 1
    print("# Golden artifact check")
    print("PASS: edge fixture summary matches golden artifact")
    return 0


def _golden_summary(plan) -> dict[str, object]:
    return {
        "contract_version": "edge_fixture_summary.v1",
        "row_count": plan.summary["row_count"],
        "batch_states": plan.summary["batch_states"],
        "issue_severity": plan.summary["issue_severity"],
        "issue_codes": plan.summary["issue_codes"],
        "owner_queue": plan.summary["owner_queue"],
        "mutation_allowed": False,
        "meta_api_compatibility": "not_claimed",
    }


if __name__ == "__main__":
    raise SystemExit(main())
