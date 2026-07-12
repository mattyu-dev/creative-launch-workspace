#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from meta_importer.ai.contracts import FIELD_NAMES
from meta_importer.ai.evaluation import evaluate, load_cases
from meta_importer.ai.evidence_page import render_evidence_page
from meta_importer.ai.materialize import review_and_materialize
from meta_importer.ai.orchestration import propose_brief
from meta_importer.ai.providers import DeterministicBaselineProvider

EVIDENCE = ROOT / "docs/evidence"


def write_json(name: str, payload: dict[str, object]) -> None:
    (EVIDENCE / name).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def main() -> int:
    cases = load_cases(ROOT / "evals/brief_mapping/dataset_v1.jsonl")
    report = evaluate(cases, DeterministicBaselineProvider)
    if not report["passed"]:
        raise SystemExit("brief mapping baseline eval failed")

    brief = (ROOT / "fixtures/synthetic_campaign_brief.txt").read_text()
    proposal = propose_brief(brief, DeterministicBaselineProvider())
    receipt, materialization = review_and_materialize(
        proposal,
        brief=brief,
        reviewer="Synthetic Approver",
        decisions={name: "accepted" for name in FIELD_NAMES},
        template=ROOT / "fixtures/synthetic_creative_template.csv",
        output=EVIDENCE / "reviewed-manifest-example.csv",
    )

    write_json("brief-mapping-baseline-eval.json", report)
    write_json("brief-proposal-example.json", proposal)
    write_json("brief-review-example.json", receipt)
    write_json("reviewed-manifest-validation.json", materialization)
    (ROOT / "docs/brief-evidence.html").write_text(
        render_evidence_page(
            brief=brief,
            proposal=proposal,
            receipt=receipt,
            materialization=materialization,
        )
    )
    print("Rebuilt AI proposal, review, manifest validation, and 36-case baseline evidence")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
