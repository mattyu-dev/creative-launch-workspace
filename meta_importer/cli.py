from __future__ import annotations

import argparse
import json
from pathlib import Path

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
from .sales_readiness import write_start_selling_report
from .sqlite_store import SQLiteWorkspaceStore
from .workspace_state import export_workspace_state_dict


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Meta Importer offline launch workspace")
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

    readiness = sub.add_parser(
        "sales-readiness",
        help="Write a start-selling readiness report without external calls",
    )
    readiness.add_argument("--out", type=Path, help="Write readiness report JSON")
    readiness.add_argument("--markdown", type=Path, help="Write readiness report Markdown")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "plan":
        return _plan(args)
    if args.command == "sales-readiness":
        return _sales_readiness(args)
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


def _sales_readiness(args: argparse.Namespace) -> int:
    report = write_start_selling_report(out_path=args.out, markdown_path=args.markdown)
    summary = report["summary"]
    print(
        "Built start-selling readiness report: "
        f"{summary['local_started_count']}/{summary['track_count']} tracks locally started; "
        f"allowed motion is {report['can_sell_now']}"
    )
    if args.out:
        print(f"Wrote {args.out}")
    if args.markdown:
        print(f"Wrote {args.markdown}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
