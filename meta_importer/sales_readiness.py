from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path


CONTRACT_VERSION = "start_selling_readiness.v1"
DEFAULT_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class ReadinessTrack:
    id: str
    title: str
    owner_role: str
    local_start_paths: tuple[str, ...]
    evidence_paths: tuple[str, ...]
    missing_before_selling: tuple[str, ...]
    blocked_by: tuple[str, ...]
    promotion_trigger: str


READINESS_TRACKS = (
    ReadinessTrack(
        id="positioning_and_icp",
        title="Positioning, ICP, and buyer proof",
        owner_role="Customer Discovery / GTM Lead",
        local_start_paths=(
            "docs/product/start_selling_readiness_plan.md",
            "docs/gtm/pilot_offer_and_sales_motion.md",
            "docs/research/market_and_competitor_scan_2026-07-06.md",
        ),
        evidence_paths=(
            "docs/research/market_and_competitor_scan_2026-07-06.md",
            "docs/product/agency_importer_product_baseline.md",
        ),
        missing_before_selling=(
            "three agency operator rehearsals",
            "buyer-role confirmation",
            "willingness-to-pay range",
            "safe-export value proof",
        ),
        blocked_by=(
            "external agency conversations",
            "current competitor pricing proof",
        ),
        promotion_trigger="Two of three target operators say the synthetic workflow would materially reduce launch-prep or QA time.",
    ),
    ReadinessTrack(
        id="demo_product",
        title="Demo product and rehearsal surface",
        owner_role="Product & Agency Workflow Lead",
        local_start_paths=(
            "docs/product/start_selling_readiness_plan.md",
            "docs/gtm/pilot_offer_and_sales_motion.md",
            "docs/ops/pilot_onboarding_support_runbook.md",
        ),
        evidence_paths=(
            "docs/product/sellable_saas_foundation.md",
            "docs/product/offline_launch_workspace_implementation.md",
            "docs/qa/browser_quality_gate.md",
        ),
        missing_before_selling=(
            "demo script timed against the 100-row synthetic batch",
            "first-run friction capture",
            "preview-quality creative inspection",
        ),
        blocked_by=(
            "external usability rehearsal for paid-pilot confidence",
        ),
        promotion_trigger="A target operator can complete the synthetic rehearsal without reading implementation docs.",
    ),
    ReadinessTrack(
        id="pilot_offer",
        title="Pilot offer, pricing, and acceptance criteria",
        owner_role="GTM / Customer Success Lead",
        local_start_paths=(
            "docs/gtm/pilot_offer_and_sales_motion.md",
            "docs/ops/pilot_onboarding_support_runbook.md",
        ),
        evidence_paths=(
            "docs/research/agency_workflow_rehearsal_plan.md",
            "docs/product/project_gap_map_big_tech_audit.md",
            "docs/product/leaderboard_missing_systems_review.md",
        ),
        missing_before_selling=(
            "paid pilot scope",
            "success metric",
            "budget owner",
            "LOI or payment signal",
            "kill/pivot review after discovery",
        ),
        blocked_by=(
            "external buyer conversations",
            "operator approval for outreach targets",
        ),
        promotion_trigger="One qualified buyer agrees to a paid synthetic rehearsal or signs an LOI with a clear success metric.",
    ),
    ReadinessTrack(
        id="trust_legal_privacy",
        title="Trust, legal, privacy, and approval packet",
        owner_role="Security / Secrets Officer",
        local_start_paths=(
            "docs/security/customer_data_trust_gates.md",
            "docs/security/pilot_privacy_and_approval_packet.md",
        ),
        evidence_paths=(
            "docs/security/trust_architecture_v1.md",
            "docs/security/customer_data_trust_gates.md",
        ),
        missing_before_selling=(
            "G1 customer-data approval artifact",
            "retention and deletion decision",
            "redaction plan",
            "DPA/privacy posture",
            "tenant isolation model before production rollout",
        ),
        blocked_by=(
            "HITL approval before customer data",
            "legal/privacy review",
        ),
        promotion_trigger="A gate-specific approval artifact exists before any real agency manifest or creative data enters the workflow.",
    ),
    ReadinessTrack(
        id="meta_platform_access",
        title="Meta platform, sandbox, and access-tier path",
        owner_role="Meta Ads API / Platform Lead",
        local_start_paths=(
            "docs/platform/meta_marketing_api_contract_mapping.md",
            "docs/platform/meta_app_review_sandbox_readiness.md",
            "docs/platform/meta_native_asset_handoff.md",
        ),
        evidence_paths=(
            "docs/platform/meta_marketing_api_contract_mapping.md",
            "docs/platform/platform_payload_preview.md",
            "docs/platform/meta_native_asset_handoff.md",
        ),
        missing_before_selling=(
            "G2 credential/OAuth design",
            "G3 sandbox/read-only proof",
            "Business Creative Asset Management folder proof",
            "G4 upload proof",
            "G5 validate-only execution proof",
            "G6 live-mutation approval",
        ),
        blocked_by=(
            "HITL approval",
            "Meta app setup and access tier",
            "credential handling decision",
        ),
        promotion_trigger="Platform and Security approve a scoped sandbox/read-only proof with redacted evidence and no customer data.",
    ),
    ReadinessTrack(
        id="production_engineering",
        title="Production engineering, persistence, and observability",
        owner_role="CTO / Architect",
        local_start_paths=(
            "docs/product/local_batch_store_backend.md",
            "docs/product/start_selling_readiness_plan.md",
        ),
        evidence_paths=(
            "docs/architecture/rfc_0001_launch_workspace_app_architecture.md",
            "docs/product/local_batch_store_backend.md",
            "meta_importer/sqlite_store.py",
        ),
        missing_before_selling=(
            "production database decision beyond local SQLite proof",
            "browser row-level app-to-backend sync",
            "auth and tenant isolation",
            "structured logging and support diagnostics",
            "migrations and release process",
        ),
        blocked_by=(
            "production deployment decision",
            "tenant-data approval before private data",
        ),
        promotion_trigger="Local app persistence has row-level sync and audit history without customer data, then a production storage RFC is approved.",
    ),
    ReadinessTrack(
        id="qa_accessibility",
        title="QA, accessibility, and evidence gates",
        owner_role="QA / Evidence Lead",
        local_start_paths=(
            "docs/qa/fixture_matrix_and_quality_gates.md",
            "docs/qa/browser_quality_gate.md",
        ),
        evidence_paths=(
            "docs/qa/fixture_matrix_and_quality_gates.md",
            "docs/qa/browser_quality_gate.md",
            "fixtures/fake_agency_creatives/golden_edge_summary.json",
            "fixtures/fake_agency_creatives/asset_metadata.csv",
        ),
        missing_before_selling=(
            "real axe or screen-reader pass",
            "browser-runtime save/resume proof",
            "property-style manifest fuzzing",
        ),
        blocked_by=(
            "runtime tooling choice for deeper accessibility proof",
        ),
        promotion_trigger="A real browser runtime proves reload persistence and an accessibility tool or manual screen-reader pass is captured.",
    ),
    ReadinessTrack(
        id="onboarding_support_ops",
        title="Onboarding, support, and operating cadence",
        owner_role="Implementation / Customer Success Lead",
        local_start_paths=(
            "docs/ops/company_operating_cadence.md",
            "docs/ops/pilot_onboarding_support_runbook.md",
        ),
        evidence_paths=(
            "docs/ops/company_operating_cadence.md",
            "docs/ops/pilot_onboarding_support_runbook.md",
        ),
        missing_before_selling=(
            "pilot onboarding checklist rehearsed with an operator",
            "support response path",
            "incident/deletion runbook for customer data after G1",
            "weekly feedback loop",
        ),
        blocked_by=(
            "external customer schedule",
            "customer-data gate before private artifacts",
        ),
        promotion_trigger="A synthetic onboarding rehearsal produces a completed checklist and one support-loop improvement.",
    ),
)


def build_start_selling_readiness(root: Path | None = None) -> dict[str, object]:
    project_root = root or DEFAULT_ROOT
    tracks = [_track_status(project_root, track) for track in READINESS_TRACKS]
    local_started = sum(1 for track in tracks if track["local_start_status"] == "started")
    blocked_tracks = sum(1 for track in tracks if track["blocked_by"])
    return {
        "product": "Creative Launch Workspace for Meta Ads",
        "contract_version": CONTRACT_VERSION,
        "generated_at": date.today().isoformat(),
        "current_allowed_tier": "G0 synthetic/offline only",
        "can_sell_now": "paid discovery or synthetic rehearsal only",
        "cannot_sell_yet": [
            "customer-data workflow",
            "credentialed Meta integration",
            "sandbox/read-only proof",
            "media upload",
            "validate-only execution",
            "live publishing",
            "production multi-tenant SaaS",
        ],
        "summary": {
            "track_count": len(tracks),
            "local_started_count": local_started,
            "blocked_track_count": blocked_tracks,
            "all_local_starts_present": local_started == len(tracks),
        },
        "tracks": tracks,
    }


def _track_status(root: Path, track: ReadinessTrack) -> dict[str, object]:
    local_paths = [_path_status(root, path) for path in track.local_start_paths]
    evidence_paths = [_path_status(root, path) for path in track.evidence_paths]
    local_started = all(item["exists"] for item in local_paths)
    evidence_present = all(item["exists"] for item in evidence_paths)
    return {
        "id": track.id,
        "title": track.title,
        "owner_role": track.owner_role,
        "local_start_status": "started" if local_started else "missing_local_start",
        "evidence_status": "present" if evidence_present else "missing_evidence",
        "local_start_paths": local_paths,
        "evidence_paths": evidence_paths,
        "missing_before_selling": list(track.missing_before_selling),
        "blocked_by": list(track.blocked_by),
        "promotion_trigger": track.promotion_trigger,
    }


def _path_status(root: Path, relative_path: str) -> dict[str, object]:
    path = root / relative_path
    return {
        "path": relative_path,
        "exists": path.exists(),
    }


def render_start_selling_markdown(report: dict[str, object]) -> str:
    summary = report["summary"]
    lines = [
        "# Start Selling Readiness Report",
        "",
        f"- Contract: `{report['contract_version']}`",
        f"- Generated: {report['generated_at']}",
        f"- Current allowed tier: {report['current_allowed_tier']}",
        f"- Can sell now: {report['can_sell_now']}",
        "",
        "## Summary",
        "",
        f"- Tracks: {summary['track_count']}",
        f"- Local starts present: {summary['local_started_count']}",
        f"- Blocked tracks: {summary['blocked_track_count']}",
        f"- All local starts present: {summary['all_local_starts_present']}",
        "",
        "## Tracks",
        "",
        "| Track | Local start | Evidence | Promotion trigger |",
        "| --- | --- | --- | --- |",
    ]
    for track in report["tracks"]:
        lines.append(
            "| {title} | {local} | {evidence} | {trigger} |".format(
                title=track["title"],
                local=track["local_start_status"],
                evidence=track["evidence_status"],
                trigger=str(track["promotion_trigger"]).replace("|", "/"),
            )
        )
    lines.extend(["", "## Blocked Capabilities", ""])
    for item in report["cannot_sell_yet"]:
        lines.append(f"- {item}")
    return "\n".join(lines).rstrip() + "\n"


def write_start_selling_report(
    out_path: Path | None = None,
    markdown_path: Path | None = None,
    root: Path | None = None,
) -> dict[str, object]:
    report = build_start_selling_readiness(root=root)
    if out_path:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    if markdown_path:
        markdown_path.parent.mkdir(parents=True, exist_ok=True)
        markdown_path.write_text(render_start_selling_markdown(report))
    return report
