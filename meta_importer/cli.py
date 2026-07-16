from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from .ai.evaluation import evaluate, evaluate_live_provider, load_cases
from .ai.materialize import review_and_materialize
from .ai.orchestration import propose_brief
from .ai.providers import DeterministicBaselineProvider
from .ai.review import review_proposal
from .html_quality import audit_workspace_html
from .launch_workspace import (
    ManifestSchemaError,
    SyntheticDataError,
    build_launch_plan,
    export_plan_dict,
    read_manifest,
    render_html_workspace,
    render_markdown_review,
)
from .local_store import write_batch_store
from .platform_payload_preview import build_platform_payload_preview
from .sqlite_store import SQLiteWorkspaceStore
from .workspace_state import export_workspace_state_dict


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Launch Control offline review system")
    sub = parser.add_subparsers(dest="command", required=True)

    plan = sub.add_parser("plan", help="Build a dry-run launch plan from a manifest CSV")
    plan.add_argument("manifest", type=Path)
    plan.add_argument("--out", type=Path, required=True, help="Write dry-run plan JSON")
    plan.add_argument("--review", type=Path, required=True, help="Write markdown review packet")
    plan.add_argument("--html", type=Path, help="Write a static HTML workspace")
    plan.add_argument("--html-audit", type=Path, help="Write static HTML accessibility/workflow audit JSON")
    plan.add_argument("--state", type=Path, help="Write local review-state JSON")
    plan.add_argument("--store-dir", type=Path, help="Write local filesystem batch store")
    plan.add_argument("--sqlite-db", type=Path, help="Write local SQLite workspace store")
    plan.add_argument(
        "--tenant-id",
        default="tenant_fixture_default",
        help="Synthetic fixture tenant id for --sqlite-db",
    )
    plan.add_argument("--platform-preview", type=Path, help="Write non-executable Meta-shaped payload preview JSON")
    plan.add_argument(
        "--asset-metadata",
        type=Path,
        help="Synthetic asset metadata CSV for local asset validation",
    )
    plan.add_argument(
        "--allow-real-data",
        action="store_true",
        help="Allow non-fixture data. This still does not call Meta or publish anything.",
    )

    brief_propose = sub.add_parser(
        "brief-propose",
        help="Turn a synthetic unstructured brief into a review-only mapping proposal",
    )
    brief_propose.add_argument("brief", type=Path)
    brief_propose.add_argument("--out", type=Path, required=True)
    brief_propose.add_argument(
        "--provider", choices=("deterministic", "openai"), default="deterministic"
    )
    brief_propose.add_argument("--model", default="gpt-5.6-terra")
    brief_propose.add_argument(
        "--fixture-registry",
        type=Path,
        default=Path("evals/brief_mapping/manifest.json"),
    )

    brief_eval = sub.add_parser(
        "brief-eval", help="Run the repo-native synthetic brief-mapping benchmark"
    )
    brief_eval.add_argument("--dataset", type=Path, required=True)
    brief_eval.add_argument("--out", type=Path, required=True)
    brief_eval.add_argument(
        "--provider", choices=("deterministic", "openai"), default="deterministic"
    )
    brief_eval.add_argument("--model", default="gpt-5.6-terra")
    brief_eval.add_argument("--repetitions", type=int, default=3)
    brief_eval.add_argument(
        "--fixture-registry",
        type=Path,
        default=Path("evals/brief_mapping/manifest.json"),
    )

    brief_review = sub.add_parser(
        "brief-review", help="Record field-level human decisions for a proposal"
    )
    brief_review.add_argument("proposal", type=Path)
    brief_review.add_argument("--brief", type=Path, required=True)
    brief_review.add_argument("--reviewer", required=True)
    brief_review.add_argument(
        "--decision",
        action="append",
        default=[],
        metavar="FIELD=accepted|rejected",
        help="Repeat once for every proposal field",
    )
    brief_review.add_argument("--out", type=Path, required=True)

    brief_materialize = sub.add_parser(
        "brief-materialize",
        help="Apply an accepted mapping receipt to a synthetic manifest template",
    )
    brief_materialize.add_argument("proposal", type=Path)
    brief_materialize.add_argument("--brief", type=Path, required=True)
    brief_materialize.add_argument("template", type=Path)
    brief_materialize.add_argument("--reviewer", required=True)
    brief_materialize.add_argument(
        "--decision",
        action="append",
        default=[],
        metavar="FIELD=accepted|rejected",
        help="Repeat once for every proposal field",
    )
    brief_materialize.add_argument("--out-receipt", type=Path, required=True)
    brief_materialize.add_argument("--out-manifest", type=Path, required=True)
    brief_materialize.add_argument("--out-plan", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "plan":
        return _plan(args)
    if args.command == "brief-propose":
        return _brief_propose(args)
    if args.command == "brief-eval":
        return _brief_eval(args)
    if args.command == "brief-review":
        return _brief_review(args)
    if args.command == "brief-materialize":
        return _brief_materialize(args)
    raise AssertionError(args.command)


def _plan(args: argparse.Namespace) -> int:
    try:
        rows = read_manifest(args.manifest, synthetic_only=not args.allow_real_data)
    except SyntheticDataError as exc:
        raise SystemExit(f"Blocked by synthetic-data guardrail: {exc}") from exc
    except ManifestSchemaError as exc:
        raise SystemExit(f"Blocked by manifest schema guardrail: {exc}") from exc

    plan = build_launch_plan(rows, source_manifest=str(args.manifest))
    payload = export_plan_dict(plan)
    review = render_markdown_review(plan)
    html = render_html_workspace(plan) if args.html or args.html_audit else None
    state = export_workspace_state_dict(plan) if args.state else None
    platform_preview = build_platform_payload_preview(plan) if args.platform_preview else None
    asset_metadata = args.asset_metadata or _default_asset_metadata(args.manifest)
    if args.asset_metadata and not asset_metadata.exists():
        raise SystemExit(f"Asset metadata not found: {asset_metadata}")
    store_manifest = (
        write_batch_store(
            plan,
            args.store_dir,
            asset_metadata_path=asset_metadata if asset_metadata.exists() else None,
        )
        if args.store_dir
        else None
    )
    sqlite_manifest = None
    if args.sqlite_db:
        sqlite_store = SQLiteWorkspaceStore(args.sqlite_db)
        try:
            sqlite_manifest = sqlite_store.upsert_batch(plan, tenant_id=args.tenant_id)
        finally:
            sqlite_store.close()

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.review.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    args.review.write_text(review)
    if args.html:
        args.html.parent.mkdir(parents=True, exist_ok=True)
        args.html.write_text(html or "")
    if args.html_audit:
        args.html_audit.parent.mkdir(parents=True, exist_ok=True)
        args.html_audit.write_text(
            json.dumps(audit_workspace_html(html or ""), indent=2, sort_keys=True) + "\n"
        )
    if args.state:
        args.state.parent.mkdir(parents=True, exist_ok=True)
        args.state.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")
    if args.platform_preview:
        args.platform_preview.parent.mkdir(parents=True, exist_ok=True)
        args.platform_preview.write_text(json.dumps(platform_preview, indent=2, sort_keys=True) + "\n")

    states = plan.summary["batch_states"]
    blockers = plan.summary["issue_severity"].get("blocker", 0)
    warnings = plan.summary["issue_severity"].get("warning", 0)
    print(
        "Built offline launch plan: "
        f"{plan.summary['row_count']} rows, "
        f"{states.get('launch_ready', 0)} launch-ready, "
        f"{states.get('needs_review', 0)} needs-review, "
        f"{states.get('blocked', 0)} blocked, "
        f"{blockers} blockers, {warnings} warnings"
    )
    print(f"Wrote {args.out}")
    print(f"Wrote {args.review}")
    if args.html:
        print(f"Wrote {args.html}")
    if args.html_audit:
        print(f"Wrote {args.html_audit}")
    if args.state:
        print(f"Wrote {args.state}")
    if args.platform_preview:
        print(f"Wrote {args.platform_preview}")
    if store_manifest:
        print(f"Wrote {store_manifest['root']}")
        print(f"Asset validation: {store_manifest['asset_validation_status']}")
    if sqlite_manifest:
        print(f"Wrote SQLite store {sqlite_manifest['database']}")
        print(f"SQLite batch {sqlite_manifest['batch_id']} for {sqlite_manifest['tenant_id']}")
    return 0


def _default_asset_metadata(manifest: Path) -> Path:
    return manifest.parent / "asset_metadata.csv"


def _brief_propose(args: argparse.Namespace) -> int:
    brief = args.brief.read_text()
    if args.provider == "openai":
        from .ai.providers.openai_responses import OpenAIResponsesProvider

        provider = OpenAIResponsesProvider(
            model=args.model,
            allowed_brief_sha256=_load_fixture_registry(args.fixture_registry),
        )
    else:
        provider = DeterministicBaselineProvider()
    proposal = propose_brief(brief, provider)
    _write_json(args.out, proposal)
    print(
        f"Built {proposal['status']} brief proposal with {proposal['provider']} "
        f"({len(proposal['risk_flags'])} risk flags; human review required)"
    )
    print(f"Wrote {args.out}")
    return 0


def _brief_eval(args: argparse.Namespace) -> int:
    if args.provider == "openai":
        from .ai.providers.openai_responses import OpenAIResponsesProvider

        allowed_hashes = _load_fixture_registry(
            args.fixture_registry, dataset=args.dataset
        )
        report = evaluate_live_provider(
            load_cases(args.dataset, suite="model_live"),
            lambda: OpenAIResponsesProvider(
                model=args.model, allowed_brief_sha256=allowed_hashes
            ),
            repetitions=args.repetitions,
        )
    else:
        report = evaluate(
            load_cases(args.dataset, suite="baseline"), DeterministicBaselineProvider
        )
    _write_json(args.out, report)
    print(
        f"Evaluated {report['case_count']} synthetic cases: "
        f"{'PASS' if report['passed'] else 'FAIL'}"
    )
    print(f"Wrote {args.out}")
    return 0 if report["passed"] else 1


def _brief_review(args: argparse.Namespace) -> int:
    decisions = _parse_decisions(args.decision)
    receipt = review_proposal(
        json.loads(args.proposal.read_text()),
        brief=args.brief.read_text(),
        reviewer=args.reviewer,
        decisions=decisions,
    )
    _write_json(args.out, receipt)
    print(f"Recorded human review: {receipt['status']}")
    print(f"Wrote {args.out}")
    return 0


def _brief_materialize(args: argparse.Namespace) -> int:
    receipt, result = review_and_materialize(
        json.loads(args.proposal.read_text()),
        brief=args.brief.read_text(),
        reviewer=args.reviewer,
        decisions=_parse_decisions(args.decision),
        template=args.template,
        output=args.out_manifest,
    )
    _write_json(args.out_receipt, receipt)
    _write_json(args.out_plan, result)
    print(
        f"Materialized {result['row_count']} synthetic rows and passed deterministic launch QA"
    )
    print(f"Wrote {args.out_manifest}")
    print(f"Wrote {args.out_receipt}")
    print(f"Wrote {args.out_plan}")
    return 0


def _parse_decisions(raw_decisions: list[str]) -> dict[str, str]:
    decisions = {}
    for raw in raw_decisions:
        if "=" not in raw:
            raise SystemExit(
                f"Invalid --decision {raw!r}; expected FIELD=accepted|rejected"
            )
        field, value = raw.split("=", 1)
        decisions[field] = value
    return decisions


def _write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def _load_fixture_registry(
    path: Path, *, dataset: Path | None = None
) -> set[str]:
    registry = json.loads(path.read_text())
    if registry.get("contract_version") != "openai_synthetic_fixture_registry.v1":
        raise SystemExit("Invalid OpenAI synthetic fixture registry contract")
    dataset_path = dataset or path.with_name("dataset_v1.jsonl")
    actual_dataset_hash = hashlib.sha256(dataset_path.read_bytes()).hexdigest()
    if registry.get("dataset_sha256") != actual_dataset_hash:
        raise SystemExit("OpenAI fixture registry does not match the selected dataset")
    allowed = {
        str(item["sha256"])
        for item in registry.get("allowed_briefs", [])
        if isinstance(item, dict) and len(str(item.get("sha256", ""))) == 64
    }
    if not allowed:
        raise SystemExit("OpenAI fixture registry contains no allowed brief hashes")
    return allowed


if __name__ == "__main__":
    raise SystemExit(main())
