from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

from .clock import today_iso

SUPPORTED_FORMATS = {"image", "video", "carousel", "story"}
APPROVAL_STATUSES = {"approved", "pending", "rejected"}
SUPPORTED_OBJECTIVES = {"awareness", "traffic", "engagement", "leads", "app_promotion", "sales"}
SUPPORTED_PLACEMENTS = {"feed", "story", "reels", "marketplace", "right_column", "search"}
SUPPORTED_POST_ID_TYPES = {"new", "existing", "placeholder"}
PLACEMENTS_BY_FORMAT = {
    "image": {"feed", "story", "marketplace", "right_column", "search"},
    "video": {"feed", "story", "reels"},
    "carousel": {"feed", "marketplace"},
    "story": {"story", "reels"},
}
SYNTHETIC_ASSET_PREFIX = Path("fixtures/fake_agency_creatives/assets")
SYNTHETIC_HOST = "example.invalid"
REQUIRED_MANIFEST_FIELDS = {
    "creative_id",
    "campaign_key",
    "adset_key",
    "format",
    "asset_path",
    "primary_text",
    "headline",
    "destination_url",
    "approval_status",
    "qa_issue",
}
OPTIONAL_MANIFEST_FIELDS = {
    "account_id_alias",
    "objective",
    "placement",
    "asset_hash",
    "variant_group",
    "hook",
    "language",
    "country",
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "utm_content",
    "utm_term",
    "post_id",
    "post_id_type",
    "source_system",
    "source_row_id",
    "reviewer",
    "approved_at",
}
KNOWN_MANIFEST_FIELDS = REQUIRED_MANIFEST_FIELDS | OPTIONAL_MANIFEST_FIELDS

ISSUE_POLICY = {
    "missing_approval": (
        "blocker",
        "Approver",
        "Creative is not approved for launch.",
        "Approve the creative or remove it from the launch batch.",
    ),
    "naming_error": (
        "blocker",
        "Creative Ops Manager",
        "Naming taxonomy does not match the launch convention.",
        "Rename the row using campaign/ad set/creative/format taxonomy.",
    ),
    "duplicate_asset": (
        "warning",
        "Creative Ops Manager",
        "Asset appears to be reused and needs intent confirmed.",
        "Confirm the duplicate is intentional or replace the asset.",
    ),
    "destination_mismatch": (
        "blocker",
        "Media Buyer",
        "Destination URL differs from the dominant URL for this ad set.",
        "Map the row to the correct landing page or move it to the right ad set.",
    ),
    "unsupported_format": (
        "blocker",
        "Creative Ops Manager",
        "Format is not supported by the first offline launch workspace.",
        "Convert to image, video, carousel, or story before export.",
    ),
}


class SyntheticDataError(ValueError):
    """Raised when a default-safe run sees non-synthetic manifest data."""


class ManifestSchemaError(ValueError):
    """Raised when a manifest CSV header does not match the offline contract."""


@dataclass(frozen=True)
class ManifestRow:
    source_row: int
    creative_id: str
    campaign_key: str
    adset_key: str
    format: str
    asset_path: str
    primary_text: str
    headline: str
    destination_url: str
    approval_status: str
    qa_issue: str
    account_id_alias: str = ""
    objective: str = ""
    placement: str = ""
    asset_hash: str = ""
    variant_group: str = ""
    hook: str = ""
    language: str = ""
    country: str = ""
    utm_source: str = ""
    utm_medium: str = ""
    utm_campaign: str = ""
    utm_content: str = ""
    utm_term: str = ""
    post_id: str = ""
    post_id_type: str = ""
    source_system: str = ""
    source_row_id: str = ""
    reviewer: str = ""
    approved_at: str = ""


@dataclass(frozen=True)
class Issue:
    source_row: int
    creative_id: str
    severity: str
    code: str
    owner: str
    message: str
    proposed_fix: str


@dataclass(frozen=True)
class AdCandidate:
    source_row: int
    creative_id: str
    campaign_key: str
    adset_key: str
    format: str
    asset_path: str
    destination_url: str
    account_id_alias: str
    objective: str
    placement: str
    asset_hash: str
    variant_group: str
    hook: str
    language: str
    country: str
    utm_source: str
    utm_medium: str
    utm_campaign: str
    utm_content: str
    utm_term: str
    final_url_preview: str
    post_id: str
    post_id_type: str
    source_system: str
    source_row_id: str
    reviewer: str
    approved_at: str
    name: str
    idempotency_key: str
    operation_intent: str
    batch_state: str
    issue_count: int


@dataclass(frozen=True)
class LaunchPlan:
    source_manifest: str
    rows: tuple[ManifestRow, ...]
    candidates: tuple[AdCandidate, ...]
    issues: tuple[Issue, ...]
    summary: dict[str, object]


def read_manifest(path: str | Path, *, synthetic_only: bool = True) -> list[ManifestRow]:
    manifest_path = Path(path)
    with manifest_path.open(newline="") as handle:
        reader = csv.DictReader(handle)
        _validate_manifest_header(reader.fieldnames or [], manifest_path)
        rows = [
            ManifestRow(
                source_row=index,
                creative_id=(raw.get("creative_id") or "").strip(),
                campaign_key=(raw.get("campaign_key") or "").strip(),
                adset_key=(raw.get("adset_key") or "").strip(),
                format=(raw.get("format") or "").strip().lower(),
                asset_path=(raw.get("asset_path") or "").strip(),
                primary_text=(raw.get("primary_text") or "").strip(),
                headline=(raw.get("headline") or "").strip(),
                destination_url=(raw.get("destination_url") or "").strip(),
                approval_status=(raw.get("approval_status") or "").strip().lower(),
                qa_issue=(raw.get("qa_issue") or "").strip().lower(),
                account_id_alias=(raw.get("account_id_alias") or "").strip(),
                objective=(raw.get("objective") or "").strip().lower(),
                placement=(raw.get("placement") or "").strip().lower(),
                asset_hash=(raw.get("asset_hash") or "").strip(),
                variant_group=(raw.get("variant_group") or "").strip(),
                hook=(raw.get("hook") or "").strip(),
                language=(raw.get("language") or "").strip().lower(),
                country=(raw.get("country") or "").strip().upper(),
                utm_source=(raw.get("utm_source") or "").strip().lower(),
                utm_medium=(raw.get("utm_medium") or "").strip().lower(),
                utm_campaign=(raw.get("utm_campaign") or "").strip(),
                utm_content=(raw.get("utm_content") or "").strip(),
                utm_term=(raw.get("utm_term") or "").strip(),
                post_id=(raw.get("post_id") or "").strip(),
                post_id_type=(raw.get("post_id_type") or "").strip().lower(),
                source_system=(raw.get("source_system") or "").strip().lower(),
                source_row_id=(raw.get("source_row_id") or "").strip(),
                reviewer=(raw.get("reviewer") or "").strip(),
                approved_at=(raw.get("approved_at") or "").strip(),
            )
            for index, raw in enumerate(reader, start=2)
        ]
    if synthetic_only:
        _assert_synthetic(rows)
    return rows


def _validate_manifest_header(fieldnames: list[str], manifest_path: Path) -> None:
    normalized = {field.strip() for field in fieldnames if field is not None}
    missing = sorted(REQUIRED_MANIFEST_FIELDS - normalized)
    unknown = sorted(normalized - KNOWN_MANIFEST_FIELDS)
    if not missing and not unknown:
        return
    messages = []
    if missing:
        messages.append(f"missing required column(s): {', '.join(missing)}")
    if unknown:
        messages.append(f"unknown column(s): {', '.join(unknown)}")
    messages.append(
        "allowed columns: " + ", ".join(sorted(KNOWN_MANIFEST_FIELDS))
    )
    raise ManifestSchemaError(f"{manifest_path}: " + "; ".join(messages))


def build_launch_plan(rows: list[ManifestRow], *, source_manifest: str = "") -> LaunchPlan:
    issues = _validate_rows(rows)
    issues_by_row: dict[int, list[Issue]] = defaultdict(list)
    for issue in issues:
        issues_by_row[issue.source_row].append(issue)

    candidates = tuple(_candidate_for(row, issues_by_row[row.source_row]) for row in rows)
    summary = _summarize(rows, candidates, issues)
    return LaunchPlan(
        source_manifest=source_manifest,
        rows=tuple(rows),
        candidates=candidates,
        issues=tuple(issues),
        summary=summary,
    )


def export_plan_dict(plan: LaunchPlan) -> dict[str, object]:
    return {
        "product": "Launch Control",
        "mode": "offline_dry_run_only",
        "contract_version": "offline_launch_plan.v2",
        "contract_status": "local_adapter_draft",
        "generated_at": today_iso(),
        "source_manifest_sha256": _source_manifest_sha256(plan.source_manifest),
        "data_classification": _data_classification(plan.rows),
        "mutation_allowed": False,
        "meta_api_compatibility": "not_claimed",
        "guardrails": [
            "No Meta API calls are made.",
            "No credentials, OAuth tokens, or live ad account identifiers are loaded.",
            "The export is a review artifact, not a live publish action.",
            "Live Meta mutation requires explicit HITL approval and separate platform proof.",
        ],
        "source_manifest": plan.source_manifest,
        "summary": plan.summary,
        "ads": [
            {
                "operation": "dry_run_create_ad_candidate",
                "operation_intent": candidate.operation_intent,
                "operation_contract": {
                    "intent": candidate.operation_intent,
                    "object_type": "ad_candidate",
                    "mutation_allowed": False,
                    "execution_status": "not_executable",
                },
                "source_row": candidate.source_row,
                "creative_id": candidate.creative_id,
                "campaign_key": candidate.campaign_key,
                "adset_key": candidate.adset_key,
                "format": candidate.format,
                "destination_url": candidate.destination_url,
                "name": candidate.name,
                "idempotency_key": candidate.idempotency_key,
                "idempotency": {
                    "key": candidate.idempotency_key,
                    "namespace": "offline_launch_plan.v2",
                    "scope": "account_alias_campaign_adset_creative_asset_destination_placement_post",
                    "key_components": [
                        "account_id_alias",
                        "campaign_key",
                        "adset_key",
                        "creative_id",
                        "asset_path",
                        "destination_url",
                        "placement",
                        "post_id",
                    ],
                    "collision_policy": "block_unless_explicit_reuse_intent",
                },
                "batch_state": candidate.batch_state,
                "issue_count": candidate.issue_count,
                "account_mapping": {
                    "account_id_alias": candidate.account_id_alias,
                },
                "placement_mapping": {
                    "campaign_key": candidate.campaign_key,
                    "adset_key": candidate.adset_key,
                    "objective": candidate.objective,
                    "placement": candidate.placement,
                    "language": candidate.language,
                    "country": candidate.country,
                },
                "creative": {
                    "format": candidate.format,
                    "asset_path": candidate.asset_path,
                    "asset_hash": candidate.asset_hash,
                    "variant_group": candidate.variant_group,
                    "hook": candidate.hook,
                    "primary_text": _row_by_source(plan.rows, candidate.source_row).primary_text,
                    "headline": _row_by_source(plan.rows, candidate.source_row).headline,
                },
                "tracking": {
                    "destination_url": candidate.destination_url,
                    "final_url_preview": candidate.final_url_preview,
                    "utm_source": candidate.utm_source,
                    "utm_medium": candidate.utm_medium,
                    "utm_campaign": candidate.utm_campaign,
                    "utm_content": candidate.utm_content,
                    "utm_term": candidate.utm_term,
                },
                "post_lineage": {
                    "post_id": candidate.post_id,
                    "post_id_type": candidate.post_id_type,
                    "operation_intent": candidate.operation_intent,
                },
                "source_lineage": {
                    "source_manifest": plan.source_manifest,
                    "source_row": candidate.source_row,
                    "source_system": candidate.source_system,
                    "source_row_id": candidate.source_row_id,
                    "asset_path": candidate.asset_path,
                    "asset_hash": candidate.asset_hash,
                },
                "approval_record": {
                    "reviewer": candidate.reviewer,
                    "approved_at": candidate.approved_at,
                },
                "preflight": {
                    "utm_checks": _preflight_checks_for(candidate, plan.issues, "utm"),
                    "placement_checks": _preflight_checks_for(candidate, plan.issues, "placement"),
                    "post_ref_checks": _preflight_checks_for(candidate, plan.issues, "post"),
                    "source_lineage_checks": _preflight_checks_for(candidate, plan.issues, "source"),
                },
            }
            for candidate in plan.candidates
        ],
        "fix_queue": [
            {
                "source_row": issue.source_row,
                "creative_id": issue.creative_id,
                "severity": issue.severity,
                "code": issue.code,
                "owner": issue.owner,
                "message": issue.message,
                "proposed_fix": issue.proposed_fix,
            }
            for issue in plan.issues
        ],
    }


def render_markdown_review(plan: LaunchPlan) -> str:
    summary = plan.summary
    owner_queue = summary["owner_queue"]
    batch_states = summary["batch_states"]
    issue_codes = summary["issue_codes"]
    lines = [
        "# Launch Control - 100 Row Review",
        "",
        "> [!warning]",
        "> Offline dry run only. This report does not call Meta, load credentials, publish ads, change budgets, or prove live Marketing API compatibility.",
        "",
        "## Batch State",
        "",
        f"- Rows: {summary['row_count']}",
        f"- Launch ready: {batch_states.get('launch_ready', 0)}",
        f"- Needs review: {batch_states.get('needs_review', 0)}",
        f"- Blocked: {batch_states.get('blocked', 0)}",
        f"- Campaigns: {summary['campaign_count']}",
        f"- Ad sets: {summary['adset_count']}",
        f"- Formats: {', '.join(summary['formats'])}",
        f"- Account aliases: {summary['launch_contract']['account_alias_rows']}",
        f"- Placement mapped: {summary['launch_contract']['placement_rows']}",
        f"- UTM mapped: {summary['launch_contract']['utm_rows']}",
        f"- Post ID lineage: {summary['launch_contract']['post_id_rows']}",
        f"- Source lineage: {summary['launch_contract']['source_lineage_rows']}",
        "",
        "## Owner Queue",
        "",
        "| Owner | Issues |",
        "| --- | ---: |",
    ]
    for owner, count in sorted(owner_queue.items()):
        lines.append(f"| {owner} | {count} |")

    lines.extend(["", "## Issue Mix", "", "| Issue | Count |", "| --- | ---: |"])
    for code, count in sorted(issue_codes.items()):
        lines.append(f"| {code} | {count} |")

    lines.extend(
        [
            "",
            "## First 20 Fixes",
            "",
            "| Row | Creative | Severity | Owner | Issue | Proposed Fix |",
            "| ---: | --- | --- | --- | --- | --- |",
        ]
    )
    for issue in plan.issues[:20]:
        lines.append(
            f"| {issue.source_row} | {issue.creative_id} | {issue.severity} | {issue.owner} | {issue.code} | {issue.proposed_fix} |"
        )

    lines.extend(
        [
            "",
        "## Export Contract",
        "",
        "- Every ad candidate has a deterministic idempotency key.",
        "- Optional v2 contract fields are exported under account, placement, tracking, post, source, approval, idempotency, and preflight blocks.",
        "- Blocked rows stay in the dry-run export for review but are not launch-ready.",
        "- Warning-only rows are marked `needs_review` so duplicates can be confirmed without stopping the whole batch.",
            "- Live publish, OAuth setup, access-token handling, and real customer data import are outside this prototype.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def render_html_workspace(plan: LaunchPlan) -> str:
    from .workspace_state import export_workspace_state_dict

    summary = plan.summary
    states = summary["batch_states"]
    owner_queue = summary["owner_queue"]
    issue_codes = summary["issue_codes"]
    state_payload = export_workspace_state_dict(plan)
    data_classification = str(state_payload["data_classification"])
    is_synthetic = data_classification == "synthetic_fixture_only"
    data_badge = "Synthetic fixture" if is_synthetic else "Operator supplied"
    data_scope_guardrail = (
        "No customer assets" if is_synthetic else "Operator-supplied rows stay local"
    )

    template = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="design-system" content="Creative Launch Product UI v3">
  <meta name="description" content="Review a 100-row synthetic Meta creative batch, inspect routed launch issues and record local human decisions.">
  <link rel="canonical" href="https://mattyu-dev.github.io/creative-launch-workspace/workspace.html">
  <meta property="og:type" content="website">
  <meta property="og:title" content="Interactive review workspace · Launch Control">
  <meta property="og:description" content="A task-first review queue for approval, destination, placement, mapping and duplicate issues.">
  <meta property="og:image" content="https://mattyu-dev.github.io/creative-launch-workspace/assets/social-card-v5.png">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2032%2032%22%3E%3Crect%20width%3D%2232%22%20height%3D%2232%22%20rx%3D%227%22%20fill%3D%22%2324142b%22%2F%3E%3C%2Fsvg%3E" type="image/svg+xml">
  <title>Launch Control · Creative launch workspace for Meta Ads</title>
  <style>
    :root {
      color-scheme: light;
      --canvas: #ECEDEE;
      --surface: #ffffff;
      --surface-soft: #F7F7F5;
      --ink: #232427;
      --body: #55575C;
      --muted: #6B6D72;
      --line: #DCDDDC;
      --line-strong: #BFC1C0;
      --orange: #E34A32;
      --action: #171719;
      --action-hover: #2C2C30;
      --action-pressed: #09090A;
      --focus: #E34A32;
      --oxide: #E34A32;
      --brand: #171719;
      --brand-soft: #FFF0EC;
      --paper: #F7F7F5;
      --peach: #F58B78;
      --ready: #166347;
      --ready-soft: #e6f1eb;
      --review: #805800;
      --review-soft: #fbefd2;
      --blocked: #a1362d;
      --blocked-soft: #f7e7e4;
      --info: #285f8f;
      --selection: #FFF0EC;
    }
    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body {
      margin: 0;
      background: var(--canvas);
      color: var(--ink);
      font: 400 14px/1.45 Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      -webkit-font-smoothing: antialiased;
    }
    button, input, select, textarea { font: inherit; }
    button, input, select, textarea, tr[tabindex] { -webkit-tap-highlight-color: transparent; }
    .skip-link {
      position: fixed;
      left: 16px;
      top: -80px;
      z-index: 20;
      padding: 10px 14px;
      color: #fff;
      background: var(--action);
      border-radius: 6px;
    }
    .skip-link:focus { top: 12px; }
    header {
      min-height: 56px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 20px;
      padding: 8px 20px;
      border-bottom: 1px solid var(--line);
      background: rgba(251, 251, 247, .96);
      position: sticky;
      top: 0;
      z-index: 8;
    }
    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
      min-width: 0;
      color: inherit;
      text-decoration: none;
    }
    .brand-mark {
      width: 30px;
      height: 30px;
      position: relative;
      flex: 0 0 auto;
    }
    .brand-mark::before, .brand-mark::after {
      content: "";
      position: absolute;
      top: 6px;
      width: 18px;
      height: 18px;
      border-radius: 50%;
    }
    .brand-mark::before { left: 0; background: var(--brand); }
    .brand-mark::after { left: 11px; background: var(--orange); }
    .brand-mark span { display:none; }
    h1 {
      margin: 0;
      font-size: 16px;
      font-weight: 500;
      line-height: 1.2;
      letter-spacing: -.01em;
    }
    .batch-line {
      margin-top: 2px;
      color: var(--muted);
      font-size: 11px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .header-status {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .local-signal {
      display: inline-flex;
      align-items: center;
      gap: 7px;
      color: var(--muted);
      font-size: 12px;
    }
    .local-signal::before {
      content: "";
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: var(--muted);
    }
    .badge {
      border: 1px solid #d2c7b4;
      border-radius: 999px;
      padding: 5px 9px;
      color: var(--body);
      background: var(--paper);
      font-size: 11px;
      font-weight: 600;
      white-space: nowrap;
    }
    .subtle { color: var(--muted); }
    main {
      min-width: 0;
      width: min(100%, 1480px);
      margin: 0 auto;
      padding: 16px 20px 28px;
      display: grid;
      gap: 16px;
    }
    .evidence-link { color: var(--brand); font-size: 12px; font-weight: 650; white-space: nowrap; }
    .header-proof {
      color: var(--brand);
      font-size: 12px;
      font-weight: 650;
      text-decoration: none;
      white-space: nowrap;
    }
    .header-proof:hover { text-decoration: underline; text-underline-offset: 3px; }
    .focus-panel {
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      align-items: center;
      gap: 20px 28px;
      padding: 24px 26px;
      border: 1px solid #343437;
      border-radius: 12px;
      color: #fff;
      background: var(--brand);
    }
    .focus-copy { max-width: 720px; }
    .focus-copy .focus-title {
      display: block;
      margin-top: 6px;
      color: inherit;
      font-size: clamp(24px, 3vw, 36px);
      font-weight: 400;
      line-height: 1.08;
      letter-spacing: -.035em;
      text-transform: none;
    }
    .focus-copy p { margin: 10px 0 0; color: rgba(255, 255, 255, .88); font-size: 13px; }
    .focus-actions { display: flex; align-items: center; gap: 8px; }
    .focus-actions button { min-height: 44px; padding-inline: 15px; }
    .focus-actions .button-primary { color: #fff; border-color: var(--action); background: var(--action); }
    .focus-actions .button-primary:hover { color: #fff; border-color: var(--action-hover); background: var(--action-hover); }
    .focus-actions .button-secondary { color: #fff; border-color: rgba(255, 255, 255, .38); background: transparent; }
    .focus-actions .button-secondary:hover { border-color: #fff; }
    .status-legend {
      grid-column: 1 / -1;
      display: flex;
      align-items: center;
      gap: 8px;
      padding-top: 16px;
      border-top: 1px solid rgba(255, 255, 255, .16);
    }
    .status-chip {
      display: inline-flex;
      align-items: center;
      gap: 7px;
      color: rgba(255, 255, 255, .88);
      font-size: 11px;
    }
    .status-chip strong { color: #fff; font-size: 13px; font-weight: 600; }
    .status-chip + .status-chip::before { content: ""; width: 1px; height: 16px; margin-right: 1px; background: rgba(255, 255, 255, .18); }
    .batch-disclosure {
      border: 1px solid var(--line);
      border-radius: 10px;
      background: var(--surface);
    }
    .batch-disclosure > summary,
    .secondary-actions > summary,
    .detail-disclosure > summary {
      cursor: pointer;
      list-style: none;
      color: var(--body);
      font-size: 12px;
      font-weight: 600;
    }
    .batch-disclosure > summary::-webkit-details-marker,
    .secondary-actions > summary::-webkit-details-marker,
    .detail-disclosure > summary::-webkit-details-marker { display: none; }
    .batch-disclosure > summary { padding: 13px 16px; }
    .batch-disclosure > summary::after,
    .secondary-actions > summary::after,
    .detail-disclosure > summary::after { content: "+"; float: right; color: var(--muted); }
    .batch-disclosure[open] > summary::after,
    .secondary-actions[open] > summary::after,
    .detail-disclosure[open] > summary::after { content: "−"; }
    .batch-context-grid {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      border-top: 1px solid var(--line);
    }
    .context-block { min-width: 0; padding: 16px; border-right: 1px solid var(--line); }
    .context-block:last-child { border-right: 0; }
    .context-block p { margin: 0 0 10px; color: var(--muted); font-size: 11px; }
    .context-block .evidence-link { display: inline-block; margin-top: 8px; }
    .eyebrow {
      color: rgba(255, 255, 255, .68);
      font-size: 11px;
      font-weight: 500;
      letter-spacing: .08em;
      text-transform: uppercase;
    }
    .workspace {
      display: grid;
      grid-template-areas: "queue detail";
      grid-template-columns: minmax(560px, 1fr) minmax(340px, 400px);
      align-items: start;
      border: 1px solid var(--line);
      border-radius: 10px;
      overflow: clip;
      background: var(--surface);
    }
    .table-shell, .detail-shell { min-width: 0; background: var(--surface); }
    .table-shell { grid-area: queue; border-right: 1px solid var(--line); }
    .detail-shell {
      grid-area: detail;
      max-height: calc(100vh - 88px);
      padding: 18px;
      overflow: auto;
      position: sticky;
      top: 72px;
    }
    h2 {
      margin: 0 0 10px;
      color: var(--muted);
      font-size: 11px;
      font-weight: 600;
      line-height: 1.25;
      letter-spacing: .07em;
      text-transform: uppercase;
    }
    h3, .detail-title {
      margin: 0;
      font-size: 18px;
      font-weight: 500;
      line-height: 1.25;
      letter-spacing: -.015em;
    }
    .queue { display: grid; }
    .queue-row {
      display: flex;
      justify-content: space-between;
      gap: 10px;
      padding: 8px 0;
      border-bottom: 1px solid var(--line);
      color: var(--body);
      font-size: 12px;
    }
    .queue-row strong { color: var(--ink); font-weight: 550; }
    .guardrails {
      margin: 0;
      padding: 12px 0 0;
      border-top: 1px solid var(--line);
      list-style: none;
    }
    .guardrails li {
      position: relative;
      padding: 4px 0 4px 14px;
      color: var(--muted);
      font-size: 11px;
    }
    .guardrails li::before {
      content: "";
      position: absolute;
      left: 0;
      top: 10px;
      width: 5px;
      height: 5px;
      background: var(--oxide);
      transform: rotate(45deg);
    }
    .toolbar {
      min-height: 58px;
      display: flex;
      align-items: flex-end;
      flex-wrap: wrap;
      gap: 8px;
      padding: 10px 12px;
      border-bottom: 1px solid var(--line);
      background: var(--surface);
    }
    .filter-set {
      display: flex;
      align-items: center;
      gap: 2px;
      padding-right: 8px;
      margin-right: auto;
    }
    .filter-set button {
      border-color: transparent;
      background: transparent;
      color: var(--muted);
    }
    .filter-set button.active,
    .filter-set button[aria-pressed="true"] {
      border-color: var(--ink);
      color: var(--ink);
      background: var(--surface-soft);
      font-weight: 550;
    }
    .toolbar label, .bulkbar label, .detail-shell label {
      display: grid;
      gap: 4px;
      color: var(--muted);
      font-size: 11px;
      font-weight: 500;
    }
    .toolbar label { width: min(190px, 100%); }
    .mobile-filters, .filter-controls { display: contents; }
    .mobile-filters > summary { display: none; }
    input, select, textarea {
      min-height: 38px;
      border: 1px solid var(--line-strong);
      border-radius: 6px;
      padding: 7px 9px;
      color: var(--ink);
      background: var(--surface);
    }
    input::placeholder { color: #8b908b; }
    textarea {
      width: 100%;
      min-height: 88px;
      resize: vertical;
    }
    button {
      min-height: 38px;
      border: 1px solid var(--line-strong);
      border-radius: 6px;
      padding: 7px 10px;
      color: var(--ink);
      background: var(--surface);
      font-weight: 500;
      cursor: pointer;
    }
    button:hover { border-color: var(--ink); }
    button:active { background: var(--surface-soft); transform: translateY(1px); }
    button:focus-visible, input:focus-visible, select:focus-visible, textarea:focus-visible, tr:focus-visible {
      outline: 2px solid var(--focus);
      outline-offset: 2px;
    }
    .button-primary { color: #fff; border-color: var(--action); background: var(--action); }
    .button-primary:hover { border-color: var(--action-hover); background: var(--action-hover); }
    .button-primary:active { border-color: var(--action-pressed); background: var(--action-pressed); }
    .bulkbar {
      min-height: 48px;
      display: flex;
      align-items: center;
      flex-wrap: wrap;
      gap: 7px;
      padding: 7px 12px;
      border-bottom: 1px solid var(--line);
      background: var(--paper);
    }
    .bulkbar .grow { flex: 1 1 190px; min-height: 20px; }
    .secondary-actions { margin-left: auto; }
    .secondary-actions > summary {
      min-height: 38px;
      display: inline-flex;
      align-items: center;
      gap: 12px;
      padding: 7px 10px;
      border: 1px solid var(--line-strong);
      border-radius: 6px;
      background: rgba(255, 255, 255, .55);
    }
    .secondary-action-grid {
      display: flex;
      flex-wrap: wrap;
      gap: 7px;
      margin-top: 8px;
    }
    .file-label {
      min-height: 38px;
      display: inline-flex !important;
      align-items: center;
      padding: 7px 10px;
      border: 1px solid var(--line-strong);
      border-radius: 6px;
      color: var(--ink) !important;
      background: rgba(255, 255, 255, .55);
      cursor: pointer;
    }
    .file-label input { position: absolute; width: 1px; height: 1px; opacity: 0; pointer-events: none; }
    .file-label:focus-within { outline: 2px solid var(--focus); outline-offset: 2px; }
    .confirm-panel {
      width: min(520px, calc(100% - 24px));
      position: fixed;
      left: 50%;
      bottom: 20px;
      z-index: 30;
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 12px;
      border: 2px solid var(--ink);
      background: var(--paper);
      transform: translateX(-50%);
    }
    .confirm-panel:not([open]) { display: none; }
    .confirm-panel::backdrop { background: rgba(28, 33, 30, .38); }
    .confirm-panel span { flex: 1 1 auto; color: var(--body); font-size: 12px; }
    .guided-dialog {
      width: min(660px, calc(100% - 28px));
      max-height: min(760px, calc(100vh - 28px));
      padding: 0;
      overflow: hidden;
      border: 1px solid var(--line-strong);
      border-radius: 10px;
      color: var(--ink);
      background: var(--surface);
    }
    .guided-dialog[open] {
      display: flex;
      flex-direction: column;
    }
    .guided-dialog:not([open]) { display: none; }
    .guided-dialog [hidden] { display: none !important; }
    .guided-dialog::backdrop { background: rgba(29, 31, 28, .68); }
    .guided-head {
      position: sticky;
      top: 0;
      z-index: 2;
      flex: 0 0 auto;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      padding: 15px 18px;
      color: #fff;
      background: var(--brand);
    }
    .guided-progress {
      font: 700 10px/1.3 ui-monospace, SFMono-Regular, Menlo, monospace;
      letter-spacing: .08em;
      text-transform: uppercase;
    }
    .guided-close { color: #fff; border-color: rgba(255, 255, 255, .4); background: transparent; }
    .guided-close:hover { border-color: #fff; }
    .guided-body {
      min-height: 0;
      padding: 24px;
      overflow-y: auto;
      overscroll-behavior: contain;
    }
    .guided-title {
      margin: 0 0 8px;
      color: var(--ink);
      font-size: clamp(25px, 4vw, 34px);
      font-weight: 450;
      line-height: 1.08;
      letter-spacing: -.035em;
      text-transform: none;
    }
    .guided-title:focus {
      margin-left: -14px;
      padding-left: 10px;
      border-left: 4px solid var(--focus);
      outline: none;
    }
    .guided-copy { margin: 0 0 20px; color: var(--body); }
    .guided-case {
      display: grid;
      grid-template-columns: 1fr 1fr;
      margin: 18px 0;
      border: 1px solid var(--line);
      background: var(--surface-soft);
    }
    .guided-case > div { min-width: 0; padding: 13px 14px; border-bottom: 1px solid var(--line); }
    .guided-case > div:nth-child(odd) { border-right: 1px solid var(--line); }
    .guided-case > div:nth-last-child(-n+2) { border-bottom: 0; }
    .guided-case span { display: block; margin-bottom: 4px; color: var(--muted); font-size: 10px; font-weight: 650; letter-spacing: .05em; text-transform: uppercase; }
    .guided-case strong { display: block; overflow-wrap: anywhere; font-size: 13px; }
    .guided-actions { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 20px; }
    .guided-actions button, .guided-return { min-height: 44px; }
    .guided-actions .button-primary { flex: 1 1 180px; }
    .guided-return {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 7px 10px;
      border: 1px solid var(--line-strong);
      border-radius: 6px;
      color: var(--ink);
      background: var(--surface);
      text-decoration: none;
      font-weight: 500;
    }
    .guided-return:hover { border-color: var(--ink); }
    .guided-proof {
      display: grid;
      grid-template-columns: 1fr 1fr;
      margin: 18px 0 0;
      border: 1px solid #bfd7c9;
      background: var(--ready-soft);
    }
    .guided-proof div { min-width: 0; padding: 12px 13px; border-bottom: 1px solid #bfd7c9; }
    .guided-proof div:nth-child(odd) { border-right: 1px solid #bfd7c9; }
    .guided-proof div:last-child { grid-column: 1 / -1; border-right: 0; border-bottom: 0; }
    .guided-proof dt { color: var(--muted); font-size: 10px; font-weight: 650; text-transform: uppercase; }
    .guided-proof dd { margin: 4px 0 0; overflow-wrap: anywhere; font: 600 12px/1.4 ui-monospace, SFMono-Regular, Menlo, monospace; }
    .guided-highlight { outline: 3px solid var(--oxide); outline-offset: 3px; }
    .table-wrap { max-height: calc(100vh - 262px); overflow: auto; }
    table { width: 100%; min-width: 620px; border-collapse: collapse; }
    caption {
      position: absolute;
      width: 1px;
      height: 1px;
      overflow: hidden;
      clip: rect(0 0 0 0);
      white-space: nowrap;
    }
    th, td {
      padding: 10px 9px;
      border-bottom: 1px solid var(--line);
      text-align: left;
      vertical-align: middle;
      font-size: 12px;
    }
    th {
      position: sticky;
      top: 0;
      z-index: 2;
      height: 38px;
      color: var(--muted);
      background: var(--surface-soft);
      font-size: 10px;
      font-weight: 600;
      letter-spacing: .055em;
      text-transform: uppercase;
    }
    th:first-child, td:first-child { padding-left: 12px; }
    tr[tabindex] {
      cursor: pointer;
      border-left: 3px solid transparent;
    }
    tr[tabindex]:hover { background: #fafbf8; }
    tr.selected { border-left-color: var(--oxide); background: var(--selection); }
    tr[aria-selected="true"] td { border-bottom-color: #cbd1c8; }
    .creative-cell {
      min-width: 145px;
      display: grid;
      grid-template-columns: 44px minmax(0, 1fr);
      align-items: center;
      gap: 9px;
    }
    .creative-thumb {
      width: 44px;
      aspect-ratio: 4 / 5;
      position: relative;
      display: grid;
      place-items: end start;
      overflow: hidden;
      padding: 5px;
      border: 1px solid rgba(28, 33, 30, .18);
      border-radius: 4px;
      color: rgba(28, 33, 30, .72);
      background: var(--paper);
      font: 600 8px/1 ui-monospace, SFMono-Regular, Menlo, monospace;
      letter-spacing: .03em;
    }
    .creative-thumb::before, .creative-thumb::after {
      content: "";
      position: absolute;
      width: 12px;
      height: 12px;
      border-color: rgba(28, 33, 30, .45);
    }
    .creative-thumb::before { left: 4px; top: 4px; border-left: 1px solid; border-top: 1px solid; }
    .creative-thumb::after { right: 4px; bottom: 4px; border-right: 1px solid; border-bottom: 1px solid; }
    .creative-thumb span { position: relative; z-index: 2; }
    .creative-thumb i {
      position: absolute;
      right: 8px;
      top: 11px;
      width: 18px;
      height: 24px;
      border: 1px solid currentColor;
      background: rgba(255, 255, 255, .42);
      transform: rotate(5deg);
    }
    .creative-thumb.format-video i, .creative-thumb.format-story i { width: 13px; height: 30px; right: 10px; top: 8px; transform: none; }
    .creative-thumb.format-carousel i { width: 19px; border-right: 5px double currentColor; }
    .creative-thumb.format-collection i { width: 18px; height: 24px; border-bottom: 8px double currentColor; transform: none; }
    .tone-0 { background: var(--peach); }
    .tone-1 { background: var(--brand-soft); }
    .tone-2 { background: var(--paper); }
    .tone-3 { color: #fff; background: var(--brand); }
    .creative-meta { min-width: 0; }
    .creative-meta strong {
      display: block;
      overflow: hidden;
      color: var(--ink);
      font-size: 12px;
      font-weight: 550;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    .creative-meta span { display: block; margin-top: 3px; color: var(--muted); font-size: 10px; }
    .mapping-cell { min-width: 112px; }
    .mapping-cell strong { display: block; font-weight: 500; }
    .mapping-cell span { display: block; margin-top: 2px; color: var(--muted); font-size: 11.5px; }
    .delivery-cell strong { display: block; font-weight: 500; }
    .delivery-cell span { display: block; margin-top: 2px; color: var(--muted); font-size: 11.5px; }
    .issue-cell { min-width: 240px; max-width: 380px; }
    .issue-cell strong { display: block; font-weight: 500; }
    .issue-cell span { display: block; margin-top: 3px; color: var(--muted); font-size: 11.5px; line-height: 1.4; }
    .state, .review-status {
      display: inline-flex;
      align-items: center;
      min-height: 24px;
      border: 1px solid transparent;
      border-radius: 999px;
      padding: 3px 7px;
      font-size: 10px;
      font-weight: 600;
      line-height: 1.2;
      white-space: nowrap;
    }
    .state::before {
      content: "";
      width: 5px;
      height: 5px;
      margin-right: 5px;
      border-radius: 50%;
      background: currentColor;
    }
    .launch_ready, .confirmed_ready { border-color: #bfd7c9; color: var(--ready); background: var(--ready-soft); }
    .ready_to_review { border-color: var(--line-strong); color: var(--body); background: var(--surface-soft); }
    .needs_review, .needs_confirmation { border-color: #ead49b; color: var(--review); background: var(--review-soft); }
    .blocked, .needs_fix { border-color: #e0bbb5; color: var(--blocked); background: var(--blocked-soft); }
    .mono {
      overflow-wrap: anywhere;
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
      font-size: 11px;
    }
    .detail-heading {
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 14px;
      padding-bottom: 14px;
      border-bottom: 1px solid var(--line);
    }
    .detail-heading .detail-title { margin: 0; color: var(--ink); font-size: 18px; font-weight: 500; letter-spacing: -.015em; text-transform: none; }
    .detail-close { display: none; }
    .detail-kicker { color: var(--muted); font-size: 10px; letter-spacing: .06em; text-transform: uppercase; }
    .detail-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 0 14px;
      margin: 10px 0 18px;
      border-top: 1px solid var(--line);
    }
    .decision-card {
      margin: 0 0 16px;
      padding: 14px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--surface-soft);
    }
    .decision-card h2 { margin-bottom: 8px; color: var(--ink); font-size: 12px; letter-spacing: 0; text-transform: none; }
    .detail-disclosure { border-top: 1px solid var(--line); }
    .detail-disclosure > summary { padding: 13px 0; }
    .detail-disclosure-content { padding: 0 0 16px; }
    .field {
      min-width: 0;
      padding: 9px 0;
      border-bottom: 1px solid var(--line);
    }
    .field span { display: block; margin-bottom: 3px; color: var(--muted); font-size: 10px; }
    .proof {
      position: relative;
      margin: 10px 0 18px;
      padding: 12px;
      border: 1px solid #d2c3aa;
      background: var(--paper);
    }
    .proof::before, .proof::after {
      content: "";
      position: absolute;
      width: 14px;
      height: 14px;
      border-color: var(--oxide);
    }
    .proof::before { left: 5px; top: 5px; border-left: 1px solid; border-top: 1px solid; }
    .proof::after { right: 5px; bottom: 5px; border-right: 1px solid; border-bottom: 1px solid; }
    .proof-label {
      margin-bottom: 22px;
      color: var(--oxide);
      font: 600 9px/1 ui-monospace, SFMono-Regular, Menlo, monospace;
      letter-spacing: .08em;
      text-transform: uppercase;
    }
    .proof p { margin: 0 0 8px; color: var(--body); line-height: 1.5; }
    .proof strong { display: block; margin-bottom: 8px; font-size: 17px; font-weight: 500; line-height: 1.25; }
    .proof .mono { padding-top: 8px; border-top: 1px solid rgba(28, 33, 30, .15); color: var(--muted); }
    .proof-visual {
      min-height: 148px;
      position: relative;
      margin: 0 0 14px;
      overflow: hidden;
      border: 1px solid rgba(28, 33, 30, .18);
      background: var(--peach);
    }
    .proof-visual span {
      position: absolute;
      left: 12px;
      top: 12px;
      z-index: 2;
      padding: 4px 6px;
      color: var(--ink);
      background: rgba(255, 255, 255, .72);
      font: 600 9px/1 ui-monospace, SFMono-Regular, Menlo, monospace;
      letter-spacing: .06em;
      text-transform: uppercase;
    }
    .proof-visual i, .proof-visual b {
      position: absolute;
      display: block;
      content: "";
    }
    .proof-visual i { width: 46%; height: 74%; right: 9%; top: 14%; border: 1px solid rgba(28, 33, 30, .34); background: var(--paper); transform: rotate(3deg); }
    .proof-visual b { width: 32%; height: 42%; right: 32%; bottom: -5%; background: var(--oxide); transform: rotate(-9deg); }
    .proof-visual.format-video, .proof-visual.format-story { background: var(--brand); }
    .proof-visual.format-video i, .proof-visual.format-story i { width: 31%; right: 18%; background: var(--brand-soft); transform: none; }
    .proof-visual.format-video b, .proof-visual.format-story b { width: 0; height: 0; right: 29%; bottom: 39%; border-top: 12px solid transparent; border-bottom: 12px solid transparent; border-left: 19px solid #fff; background: transparent; transform: none; }
    .proof-visual.format-carousel { background: var(--brand-soft); }
    .proof-visual.format-carousel i { width: 34%; right: 28%; transform: rotate(-2deg); }
    .proof-visual.format-carousel b { width: 34%; height: 74%; right: 6%; bottom: 7%; border: 1px solid rgba(28, 33, 30, .28); background: var(--peach); transform: rotate(4deg); }
    .proof-visual.format-collection { background: var(--paper); }
    .proof-visual.format-collection i { width: 38%; height: 38%; right: 8%; top: 11%; background: var(--peach); transform: none; }
    .proof-visual.format-collection b { width: 38%; height: 38%; right: 8%; bottom: 9%; background: var(--brand-soft); transform: none; }
    .issue-list { display: grid; gap: 7px; margin: 10px 0 18px; }
    .issue {
      padding: 10px 11px;
      border-left: 3px solid var(--oxide);
      background: #fbf6f2;
    }
    .issue.clean { border-left-color: var(--ready); background: var(--ready-soft); }
    .issue strong { display: block; margin-bottom: 3px; font-size: 11px; font-weight: 600; }
    .issue div { font-size: 11px; }
    .review-form { display: grid; gap: 10px; }
    .actions {
      display: grid;
      grid-template-columns: 1.15fr 1fr 1fr;
      gap: 7px;
      margin: 12px 0 20px;
    }
    .export-panel {
      padding-top: 16px;
      border-top: 1px solid var(--line);
    }
    .export-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 7px; }
    .danger { color: var(--blocked); }
    .status-line { min-height: 20px; padding-top: 7px; color: var(--muted); font-size: 11px; }
    @media (max-width: 1300px) {
      .workspace { grid-template-columns: minmax(520px, 1fr) 360px; }
    }
    @media (max-width: 1080px) {
      .workspace { grid-template-areas: "queue" "detail"; grid-template-columns: minmax(0, 1fr); overflow: visible; }
      .table-shell { border-right: 0; }
      .detail-shell { max-height: none; position: static; border-top: 1px solid var(--line); }
      .table-wrap { max-height: 620px; }
      .batch-context-grid { grid-template-columns: 1fr 1fr; }
      .context-block:nth-child(2) { border-right: 0; }
      .context-block:nth-child(-n+2) { border-bottom: 1px solid var(--line); }
    }
    @media (max-width: 1023px) {
      header { gap: 8px; position: static; padding: 9px 12px; }
      .brand { gap: 8px; flex: 1 1 auto; }
      .brand-mark { width: 30px; height: 30px; }
      h1 { max-width: 220px; overflow: hidden; font-size: 14px; text-overflow: ellipsis; white-space: nowrap; }
      .batch-line { max-width: 220px; }
      .header-status { flex: 0 0 auto; }
      .badge { padding-inline: 7px; font-size: 10px; }
      .local-signal { display: none; }
      main { grid-template-columns: minmax(0, 1fr); padding: 10px 0 86px; gap: 10px; }
      .header-proof { display: none; }
      .focus-panel { margin: 0 10px; grid-template-columns:minmax(0,1fr) auto; gap: 10px 14px; padding: 14px 16px; border-radius: 10px; }
      .focus-copy .eyebrow,.focus-copy p,.status-legend { display:none; }
      .focus-copy .focus-title { margin:0; font-size:21px; }
      .focus-actions { align-items:center; flex-direction:row; }
      .focus-actions button { min-height:40px; width:auto; padding-inline:11px; font-size:12px; }
      .batch-disclosure { margin: 0 10px; }
      .batch-context-grid { grid-template-columns: 1fr; }
      .context-block { border-right: 0; border-bottom: 1px solid var(--line); }
      .context-block:last-child { border-bottom: 0; }
      .workspace { width: 100%; min-width: 0; display: flex; flex-direction: column; margin: 0; border-left: 0; border-right: 0; border-radius: 0; }
      .table-shell { order: 1; width: 100%; }
      .detail-shell {
        width: 100%;
        max-height: none;
        position: fixed;
        inset: 0;
        z-index: 12;
        padding: 16px 14px 24px;
        overflow: auto;
        border-top: 1px solid var(--line-strong);
        background: var(--canvas);
        opacity: 0;
        visibility: hidden;
        pointer-events: none;
        transform: translateY(100%);
        transition: transform 180ms ease, opacity 180ms ease;
      }
      .detail-shell.open { opacity: 1; visibility: visible; pointer-events: auto; transform: translateY(0); }
      .detail-close { display: inline-flex; margin-left: auto; }
      body.detail-open { overflow: hidden; }
      .toolbar { min-width:0; display:grid; grid-template-columns:minmax(0,1fr) auto; align-items:center; padding:6px 10px; position:sticky; top:0; z-index:7; }
      .filter-set { width:auto; min-width:0; max-width:100%; padding:0; margin:0; overflow-x:auto; }
      .filter-set button { min-width: max-content; min-height: 44px; }
      .mobile-filters { display:block; position:relative; }
      .mobile-filters > summary { min-height:38px; display:inline-flex; align-items:center; padding:7px 9px; border:1px solid var(--line-strong); border-radius:6px; cursor:pointer; list-style:none; font-size:12px; font-weight:600; }
      .mobile-filters > summary::-webkit-details-marker { display:none; }
      .mobile-filters > summary::after { content:" +"; margin-left:5px; color:var(--muted); }
      .mobile-filters[open] > summary::after { content:" −"; }
      .filter-controls { min-width:250px; display:grid; grid-template-columns:1fr; gap:8px; position:absolute; right:0; top:44px; z-index:10; padding:12px; border:1px solid var(--line-strong); background:var(--surface); }
      .toolbar label { width:auto; min-width:0; }
      .toolbar input, .toolbar select { width: 100%; min-width: 0; }
      input, select, button, .file-label { min-height: 44px; }
      .bulkbar { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); padding: 8px 10px; }
      .bulkbar .grow, .secondary-actions, .file-label, .confirm-panel { grid-column: 1 / -1; }
      .secondary-actions > summary { width: 100%; justify-content: space-between; }
      .secondary-action-grid { display: grid; grid-template-columns: 1fr 1fr; }
      #bulk-blocked { grid-column: 1 / -1; }
      .file-label { width: 100%; justify-content: center; }
      .table-wrap { max-height: none; overflow: visible; }
      table, tbody { display: block; width: 100%; min-width: 0; }
      thead { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); }
      caption { display: block; }
      tbody tr {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 8px 12px;
        margin: 0;
        padding: 12px 10px;
        border-left-width: 4px;
        border-bottom: 1px solid var(--line);
      }
      tbody tr.selected { background: var(--selection); }
      tbody td { display: block; padding: 0; border: 0; min-width: 0; max-width: none; }
      tbody td::before {
        content: attr(data-label);
        display: block;
        margin-bottom: 3px;
        color: var(--muted);
        font-size: 9px;
        font-weight: 600;
        letter-spacing: .05em;
        text-transform: uppercase;
      }
      tbody td:first-child { grid-column: 1 / -1; padding: 0; }
      tbody td:first-child::before { content: none; }
      tbody td:nth-child(2) { grid-column: 1 / -1; }
      .creative-cell { grid-template-columns: 52px minmax(0, 1fr); }
      .creative-thumb { width: 52px; }
      .issue-cell { grid-column: 1 / -1; }
      .actions {
        position: sticky;
        bottom: 0;
        z-index: 6;
        margin: 12px -14px 18px;
        padding: 9px 10px;
        border-top: 1px solid var(--line);
        border-bottom: 1px solid var(--line);
        background: rgba(251, 251, 247, .97);
      }
      .detail-grid, .export-grid { grid-template-columns: 1fr 1fr; }
      .guided-dialog { max-height: calc(100vh - 18px); }
      .guided-body { padding: 20px 16px; }
    }
    @media (max-width: 480px) {
      .focus-panel { grid-template-columns:1fr; }
      .focus-actions button { flex:1 1 0; }
      .confirm-panel { align-items: stretch; flex-direction: column; }
      .confirm-panel button { width: 100%; }
      .guided-case, .guided-proof { grid-template-columns: 1fr; }
      .guided-case > div, .guided-case > div:nth-child(odd),
      .guided-proof div, .guided-proof div:nth-child(odd), .guided-proof div:nth-last-child(-n+2) {
        grid-column: auto;
        border-right: 0;
        border-bottom: 1px solid var(--line);
      }
      .guided-case > div:last-child, .guided-proof div:last-child { border-bottom: 0; }
      .guided-actions { display: grid; grid-template-columns: 1fr; }
    }
    @media (max-width: 360px) {
      header { padding-inline: 8px; }
      .brand-mark { width: 26px; height: 26px; }
      h1, .batch-line { max-width: 140px; }
      .header-status .badge { max-width: 74px; overflow: hidden; text-overflow: ellipsis; }
      .actions { grid-template-columns: 1fr; }
    }
    @media (prefers-reduced-motion: reduce) {
      html { scroll-behavior: auto; }
      button:active { transform: none; }
    }
  </style>
</head>
<body>
  <a class="skip-link" href="#review-workspace">Skip to review queue</a>
  <header>
    <a class="brand" href="index.html">
      <div class="brand-mark" aria-hidden="true"><span></span></div>
      <div>
        <h1>Launch Control</h1>
        <div class="batch-line" title="Batch __BATCH_ID__ &middot; __DATA_CLASSIFICATION__">__DATA_BADGE__ &middot; batch __BATCH_SHORT__</div>
      </div>
    </a>
    <div class="header-status">
      <a class="header-proof" href="brief-evidence.html">See the import evidence</a>
      <span class="local-signal">Stored locally</span>
      <span class="badge">Dry run only</span>
    </div>
  </header>
  <main>
    <section class="focus-panel" aria-labelledby="focus-title">
      <div class="focus-copy">
        <div class="eyebrow">Review session</div>
        <h2 class="focus-title" id="focus-title">__REVIEW_COUNT__ creatives need a human decision.</h2>
        <p>Start with the ambiguous rows. Creatives that pass offline checks need no exception review; blocked creatives return to their owners with a specific fix.</p>
      </div>
      <div class="focus-actions">
        <button class="button-primary" id="start-guided" data-quick-filter="needs_review">Start guided review</button>
        <button class="button-secondary" data-quick-filter="blocked">Inspect __BLOCKED_COUNT__ blockers</button>
      </div>
      <div class="status-legend" role="group" aria-label="Batch status">
        <span class="status-chip"><strong>__LAUNCH_READY__</strong> pass offline checks</span>
        <span class="status-chip"><strong>__REVIEW_COUNT__</strong> need your decision</span>
        <span class="status-chip"><strong>__BLOCKED_COUNT__</strong> routed for fixes</span>
      </div>
    </section>
    <dialog class="guided-dialog" id="guided-dialog" aria-labelledby="guided-title">
      <div class="guided-head">
        <span class="guided-progress" id="guided-progress" aria-live="polite">1 of 3 · Detect</span>
        <button class="guided-close" id="guided-close" type="button" aria-label="Close guided review">Close</button>
      </div>
      <div class="guided-body">
        <h2 class="guided-title" id="guided-title" tabindex="-1">Find the ambiguous row.</h2>
        <p class="guided-copy" id="guided-copy">The workflow has separated a possible duplicate from the rows that can pass or must return for fixes.</p>
        <div class="guided-actions" id="guided-step-two" hidden>
          <button class="button-primary" id="guided-confirm" type="button">Confirm reuse for dry-run export</button>
          <button id="guided-fix-action" type="button">Return for fix</button>
          <button class="danger" id="guided-block" type="button">Block from dry-run export</button>
        </div>
        <div class="guided-case" id="guided-case">
          <div><span>Creative</span><strong id="guided-creative"></strong></div>
          <div><span>Issue</span><strong id="guided-issue"></strong></div>
          <div><span>Owner</span><strong id="guided-owner"></strong></div>
          <div><span>Proposed fix</span><strong id="guided-fix"></strong></div>
        </div>
        <div class="guided-actions" id="guided-step-one">
          <button class="button-primary" id="guided-next" type="button">Make a human decision</button>
        </div>
        <div id="guided-step-three" hidden>
          <div class="guided-actions" id="guided-step-three-actions">
            <button class="button-primary" id="guided-explore" type="button">Explore the full queue</button>
            <a class="guided-return" id="guided-product-builder" href="https://github.com/mattyu-dev/creative-launch-workspace/blob/main/docs/architecture/system.md">View the architecture</a>
            <a class="guided-return" id="guided-return" href="index.html">Back to the overview</a>
            <button id="guided-replay" type="button">Review another case</button>
          </div>
          <dl class="guided-proof">
            <div><dt>Local state</dt><dd id="guided-result-state"></dd></div>
            <div><dt>Reviewer role</dt><dd id="guided-result-role"></dd></div>
            <div><dt>Audit event</dt><dd id="guided-result-event"></dd></div>
            <div><dt>Creative</dt><dd id="guided-result-creative"></dd></div>
            <div><dt>Occurred at</dt><dd id="guided-result-time"></dd></div>
          </dl>
          <p class="guided-copy" id="guided-result-copy"></p>
        </div>
      </div>
    </dialog>
    <details class="batch-disclosure">
      <summary>Batch details, ownership and guardrails</summary>
      <div class="batch-context-grid">
        <section class="context-block">
          <h2>Owner queue</h2>
          <div class="queue">__OWNER_QUEUE__</div>
        </section>
        <section class="context-block">
          <h2>Issue mix</h2>
          <div class="queue">__ISSUE_QUEUE__</div>
        </section>
        <section class="context-block">
          <h2>Guardrails</h2>
          <ul class="guardrails">
            <li>No Meta API calls</li>
            <li>No credentials or OAuth tokens</li>
            <li>__DATA_SCOPE_GUARDRAIL__</li>
            <li>No publish or budget mutation</li>
          </ul>
        </section>
        <section class="context-block">
          <h2>AI intake proof</h2>
          <p>8 grounded fields, policy checks, mandatory human decisions and deterministic launch QA. No model runs in this browser.</p>
          <a class="evidence-link" href="brief-evidence.html">Inspect the evidence &rarr;</a>
        </section>
      </div>
    </details>
    <div class="workspace" id="review-workspace" tabindex="-1">
      <section class="table-shell" aria-label="Creative review queue">
        <div class="toolbar" role="group" aria-label="Batch filters">
          <div class="filter-set" role="group" aria-label="Readiness filter">
            <button class="active" data-filter="needs_review" aria-pressed="true">To review</button>
            <button data-filter="blocked" aria-pressed="false">Blocked</button>
            <button data-filter="launch_ready" aria-pressed="false">Passes offline checks</button>
            <button data-filter="all" aria-pressed="false">All rows</button>
          </div>
          <details class="mobile-filters" id="filter-disclosure" open>
            <summary>Filters</summary>
            <div class="filter-controls">
              <label>
                Search
                <input id="search" type="search" autocomplete="off" placeholder="Creative, campaign, issue">
              </label>
              <label>
                Owner
                <select id="owner-filter"></select>
              </label>
            </div>
          </details>
        </div>
        <div class="bulkbar">
          <span id="visible-count" class="subtle grow" aria-live="polite"></span>
          <details class="secondary-actions">
            <summary>Batch actions</summary>
            <div class="secondary-action-grid">
              <button id="bulk-ready">Confirm visible for dry-run export</button>
              <button id="bulk-fix">Return visible for fix</button>
              <button id="bulk-blocked" class="danger">Block visible from dry-run export</button>
              <label class="file-label">
                Import state
                <input id="state-import" type="file" accept="application/json">
              </label>
            </div>
          </details>
          <dialog class="confirm-panel" id="confirm-panel" aria-labelledby="confirm-copy">
            <span id="confirm-copy"></span>
            <button id="confirm-action" class="button-primary">Confirm</button>
            <button id="cancel-action">Cancel</button>
          </dialog>
        </div>
        <div class="table-wrap">
          <table>
            <caption id="table-caption">__ROW_COUNT__ review rows</caption>
            <thead>
              <tr>
                <th>Creative</th>
                <th>Status</th>
                <th>What needs attention</th>
                <th>Decision</th>
              </tr>
            </thead>
            <tbody id="review-rows"></tbody>
          </table>
        </div>
      </section>
      <section class="detail-shell" aria-labelledby="detail-title">
        <div class="detail-heading">
          <div>
            <div class="detail-kicker">Decision workspace</div>
            <h2 class="detail-title" id="detail-title">No row selected</h2>
          </div>
          <button class="detail-close" id="close-detail" type="button" aria-label="Close row detail">Close</button>
          <span class="badge">__DATA_BADGE__</span>
        </div>
        <div class="decision-card">
          <h2>What needs attention</h2>
          <div class="issue-list" id="issue-list"></div>
        </div>
        <div class="review-form">
          <label>
            Reviewer role
            <select id="reviewer-role"></select>
          </label>
          <label>
            Review note
            <textarea id="review-note" placeholder="What should the next operator know?"></textarea>
          </label>
        </div>
        <div class="actions">
          <button id="mark-ready" class="button-primary">Confirm for dry-run export</button>
          <button id="mark-fix">Return for fix</button>
          <button id="mark-blocked" class="danger">Block from dry-run export</button>
        </div>
        <details class="detail-disclosure">
          <summary>Creative preview</summary>
          <div class="detail-disclosure-content">
            <div class="proof">
              <div class="proof-label">Creative proof &middot; not final media</div>
              <div class="proof-visual" id="preview-art" role="img" aria-label="Synthetic creative preview">
                <span id="preview-format"></span><i></i><b></b>
              </div>
              <p id="preview-text"></p>
              <strong id="preview-headline"></strong>
              <div class="mono" id="preview-url"></div>
            </div>
          </div>
        </details>
        <details class="detail-disclosure">
          <summary>Technical mapping</summary>
          <div class="detail-disclosure-content">
            <div class="detail-grid" id="detail-grid"></div>
          </div>
        </details>
        <details class="detail-disclosure export-panel">
          <summary>Local state and export</summary>
          <div class="detail-disclosure-content">
            <div class="status-line" id="review-progress"></div>
            <div class="export-grid">
              <button id="download-state">Download state</button>
              <button id="copy-state">Copy JSON</button>
              <button id="reset-state" class="danger">Reset state</button>
              <button id="undo-action" disabled>Undo last change</button>
            </div>
          </div>
        </details>
        <div class="status-line" id="status-line" role="status"></div>
      </section>
    </div>
  </main>
  <script id="workspace-data" type="application/json">__WORKSPACE_DATA__</script>
  <script>
    const workspaceData = JSON.parse(document.getElementById("workspace-data").textContent);
    const storageKey = workspaceData.local_storage_key;
    const tbody = document.getElementById("review-rows");
    const searchInput = document.getElementById("search");
    const ownerFilter = document.getElementById("owner-filter");
    const reviewerRole = document.getElementById("reviewer-role");
    const reviewNote = document.getElementById("review-note");
    const statusLine = document.getElementById("status-line");
    const detailTitle = document.getElementById("detail-title");
    const detailGrid = document.getElementById("detail-grid");
    const issueList = document.getElementById("issue-list");
    const previewText = document.getElementById("preview-text");
    const previewHeadline = document.getElementById("preview-headline");
    const previewUrl = document.getElementById("preview-url");
    const previewArt = document.getElementById("preview-art");
    const previewFormat = document.getElementById("preview-format");
    const visibleCount = document.getElementById("visible-count");
    const reviewProgress = document.getElementById("review-progress");
    const stateImport = document.getElementById("state-import");
    const detailShell = document.querySelector(".detail-shell");
    const detailClose = document.getElementById("close-detail");
    const confirmPanel = document.getElementById("confirm-panel");
    const confirmCopy = document.getElementById("confirm-copy");
    const undoButton = document.getElementById("undo-action");
    const approveButton = document.getElementById("mark-ready");
    const fixButton = document.getElementById("mark-fix");
    const blockButton = document.getElementById("mark-blocked");
    const filterDisclosure = document.getElementById("filter-disclosure");
    const guidedDialog = document.getElementById("guided-dialog");
    const guidedTitle = document.getElementById("guided-title");
    const guidedProgress = document.getElementById("guided-progress");
    const guidedCopy = document.getElementById("guided-copy");
    const guidedCase = document.getElementById("guided-case");
    const guidedStepOne = document.getElementById("guided-step-one");
    const guidedStepTwo = document.getElementById("guided-step-two");
    const guidedStepThree = document.getElementById("guided-step-three");
    const filterButtons = Array.from(document.querySelectorAll("button[data-filter]"));
    const quickFilterButtons = Array.from(document.querySelectorAll("button[data-quick-filter]:not(#start-guided)"));
    const workspaceRowsBySource = new Map(workspaceData.review_statuses.map((row) => [String(row.source_row), row]));
    const knownSourceRows = new Set(workspaceRowsBySource.keys());
    const allowedReviewStatuses = new Set(["ready_to_review", "needs_confirmation", "confirmed_ready", "needs_fix", "blocked"]);
    const allowedPatchKeys = new Set(["review_status", "decision", "note", "updated_by_role", "updated_at"]);
    const allowedAuditKeys = new Set(["event_id", "event_type", "actor_role", "message", "occurred_at", "source_row", "creative_id", "decision"]);
    const reviewerRoles = new Set(workspaceData.roles.map((item) => item.role));
    let persistedLoadError = false;
    let persisted = loadPersistedState();
    let rows = mergeRows();
    let activeFilter = "needs_review";
    let activeRow = rows.find((row) => row.batch_state === "needs_review")?.source_row
      || (rows.length ? rows[0].source_row : null);
    let lastFocusedRow = activeRow;
    let pendingAction = null;
    let undoSnapshot = null;
    let guidedActive = false;
    let guidedStep = 0;
    let guidedSourceRow = null;
    let guidedDecisionLocked = false;
    let confirmTrigger = null;

    function isPlainObject(value) {
      return Boolean(value) && typeof value === "object" && !Array.isArray(value) && Object.getPrototypeOf(value) === Object.prototype;
    }

    function syncFilterDisclosure() {
      if (window.matchMedia("(max-width: 1023px)").matches) {
        if (!filterDisclosure.dataset.mobileInitialized) filterDisclosure.removeAttribute("open");
        filterDisclosure.dataset.mobileInitialized = "true";
      } else {
        filterDisclosure.setAttribute("open", "");
        delete filterDisclosure.dataset.mobileInitialized;
      }
    }

    function validString(value, maxLength) {
      return typeof value === "string" && value.length <= maxLength;
    }

    function validateRowPatches(candidate) {
      if (!isPlainObject(candidate)) return false;
      return Object.entries(candidate).every(([sourceRow, patch]) => {
        if (!knownSourceRows.has(sourceRow) || !isPlainObject(patch)) return false;
        if (Object.keys(patch).some((key) => !allowedPatchKeys.has(key))) return false;
        if (patch.review_status !== undefined && !allowedReviewStatuses.has(patch.review_status)) return false;
        if (patch.review_status === "confirmed_ready" && workspaceRowsBySource.get(sourceRow).batch_state === "blocked") return false;
        if (patch.decision !== undefined && !validString(patch.decision, 128)) return false;
        if (patch.note !== undefined && !validString(patch.note, 4000)) return false;
        if (patch.updated_by_role !== undefined && patch.updated_by_role !== "" && !reviewerRoles.has(patch.updated_by_role)) return false;
        if (patch.updated_at !== undefined && !validString(patch.updated_at, 64)) return false;
        return true;
      });
    }

    function validateAudit(candidate) {
      if (!Array.isArray(candidate) || candidate.length > 5000) return false;
      return candidate.every((event) => {
        if (!isPlainObject(event) || Object.keys(event).some((key) => !allowedAuditKeys.has(key))) return false;
        return Object.entries(event).every(([_key, value]) => {
          return typeof value === "number" || typeof value === "boolean" || validString(value, 4000);
        });
      });
    }

    function validatedPersistedState(payload) {
      if (!isPlainObject(payload)) return null;
      if (payload.batch_id !== workspaceData.batch_id) return null;
      if (payload.contract_version !== workspaceData.contract_version) return null;
      if (payload.data_classification !== workspaceData.data_classification) return null;
      if (payload.source_manifest_sha256 !== workspaceData.source_manifest_sha256) return null;
      if (payload.mutation_allowed !== false || payload.meta_api_compatibility !== "not_claimed") return null;
      if (!validateRowPatches(payload.rows)) return null;
      if (!validateAudit(payload.audit)) return null;
      return { rows: payload.rows, audit: payload.audit };
    }

    function loadPersistedState() {
      try {
        const saved = localStorage.getItem(storageKey);
        if (!saved) {
          return { rows: {}, audit: workspaceData.audit_events.slice() };
        }
        const parsed = validatedPersistedState(JSON.parse(saved));
        if (!parsed) throw new Error("invalid persisted state");
        return parsed;
      } catch (_error) {
        persistedLoadError = true;
        return { rows: {}, audit: workspaceData.audit_events.slice() };
      }
    }

    function mergeRows() {
      return workspaceData.review_statuses.map((row) => {
        return Object.assign({}, row, persisted.rows[row.source_row] || {});
      });
    }

    function saveState() {
      const payload = exportState();
      localStorage.setItem(storageKey, JSON.stringify(payload, null, 2));
      rows = mergeRows();
    }

    function exportState() {
      const currentRows = workspaceData.review_statuses.map((row) => {
        return Object.assign({}, row, persisted.rows[row.source_row] || {});
      });
      return {
        product: workspaceData.product,
        mode: workspaceData.mode,
        contract_version: workspaceData.contract_version,
        batch_id: workspaceData.batch_id,
        source_manifest: workspaceData.source_manifest,
        source_manifest_sha256: workspaceData.source_manifest_sha256,
        data_classification: workspaceData.data_classification,
        mutation_allowed: false,
        meta_api_compatibility: "not_claimed",
        rows: persisted.rows,
        review_statuses: currentRows,
        audit: persisted.audit,
        exported_at: new Date().toISOString()
      };
    }

    function renderOwnerOptions() {
      const owners = Array.from(new Set(rows.flatMap((row) => row.owners))).sort();
      ownerFilter.replaceChildren(option("all", "All owners"), ...owners.map((owner) => option(owner, owner)));
      reviewerRole.replaceChildren(...workspaceData.roles.map((role) => option(role.role, role.role)));
    }

    function option(value, label) {
      const item = document.createElement("option");
      item.value = value;
      item.textContent = label;
      return item;
    }

    function filteredRows() {
      const query = searchInput.value.trim().toLowerCase();
      const owner = ownerFilter.value || "all";
      return rows.filter((row) => {
        const matchesState = activeFilter === "all" || row.batch_state === activeFilter;
        const matchesOwner = owner === "all" || row.owners.includes(owner);
        const haystack = [
          row.creative_id,
          row.campaign_key,
          row.adset_key,
          row.account_id_alias,
          row.issue_codes.join(" "),
          row.proposed_fix
        ].join(" ").toLowerCase();
        return matchesState && matchesOwner && (!query || haystack.includes(query));
      });
    }

    function batchStateLabel(value) {
      return {
        launch_ready: "Passes offline checks",
        needs_review: "Human decision required",
        blocked: "Blocked by offline checks"
      }[value] || value.replaceAll("_", " ");
    }

    function reviewStatusLabel(value) {
      return {
        ready_to_review: "No exception review",
        needs_confirmation: "Decision required",
        confirmed_ready: "Confirmed for dry-run export",
        needs_fix: "Return for fix",
        blocked: "Blocked from dry-run export"
      }[value] || value.replaceAll("_", " ");
    }

    function humanizeCode(value) {
      const labels = {
        missing_approval: "Approval missing",
        pending_approval: "Approval pending",
        rejected_approval: "Approval rejected",
        destination_mismatch: "Destination mismatch",
        adset_destination_mismatch: "Ad set destination mismatch",
        duplicate_asset: "Possible duplicate",
        duplicate_asset_detected: "Possible duplicate",
        naming_error: "Name does not match the batch",
        unsupported_format: "Format not supported",
        format_placement_mismatch: "Format and placement mismatch"
      };
      if (labels[value]) return labels[value];
      const label = String(value || "").replaceAll("_", " ");
      return label ? label.charAt(0).toUpperCase() + label.slice(1) : "No issue found";
    }

    function campaignTone(value) {
      let total = 0;
      for (const character of String(value || "")) total = (total + character.charCodeAt(0)) % 4;
      return total;
    }

    function normalizedFormat(value) {
      const format = String(value || "image").toLowerCase();
      if (format.includes("video")) return "video";
      if (format.includes("story")) return "story";
      if (format.includes("carousel")) return "carousel";
      if (format.includes("collection")) return "collection";
      return "image";
    }

    function handleRowKeydown(event, row) {
      const visibleRows = filteredRows();
      const index = visibleRows.findIndex((item) => item.source_row === row.source_row);
      let nextIndex = index;
      if (event.key === "ArrowDown") nextIndex = Math.min(index + 1, visibleRows.length - 1);
      if (event.key === "ArrowUp") nextIndex = Math.max(index - 1, 0);
      if (event.key === "Home") nextIndex = 0;
      if (event.key === "End") nextIndex = visibleRows.length - 1;
      if ([ "ArrowDown", "ArrowUp", "Home", "End" ].includes(event.key)) {
        event.preventDefault();
        selectRow(visibleRows[nextIndex].source_row, false, true);
        return;
      }
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        selectRow(row.source_row, true, false);
      }
    }

    function reconcileSelection() {
      const visibleRows = filteredRows();
      if (!visibleRows.length) {
        activeRow = null;
        detailTitle.textContent = "No row selected";
        clearDetail();
        renderRows();
        return;
      }
      if (!visibleRows.some((row) => row.source_row === activeRow)) {
        selectRow(visibleRows[0].source_row, false, false);
        return;
      }
      renderRows();
    }

    function clearDetail() {
      detailGrid.replaceChildren();
      issueList.replaceChildren();
      previewText.textContent = "Change the filters or search to bring review rows back into view.";
      previewHeadline.textContent = "No row selected";
      previewUrl.textContent = "";
      previewArt.className = "proof-visual";
      previewFormat.textContent = "empty review state";
      reviewNote.value = "";
      approveButton.disabled = true;
      fixButton.disabled = true;
      blockButton.disabled = true;
    }

    function renderRows() {
      const visibleRows = filteredRows();
      tbody.replaceChildren();
      if (!visibleRows.length) {
        const tr = document.createElement("tr");
        const td = document.createElement("td");
        td.colSpan = 4;
        td.className = "subtle";
        td.textContent = "No rows match the current filters.";
        tr.appendChild(td);
        tbody.appendChild(tr);
        document.getElementById("table-caption").textContent = "0 creatives in this view";
        updateProgress(visibleRows);
        return;
      }
      for (const row of visibleRows) {
        const tr = document.createElement("tr");
        tr.dataset.state = row.batch_state;
        tr.dataset.sourceRow = String(row.source_row);
        tr.tabIndex = row.source_row === activeRow ? 0 : -1;
        tr.setAttribute("aria-label", row.creative_id + ", " + batchStateLabel(row.batch_state) + ", row " + row.source_row);
        tr.setAttribute("aria-selected", String(row.source_row === activeRow));
        if (row.source_row === activeRow) tr.classList.add("selected");
        tr.addEventListener("click", () => selectRow(row.source_row, true, false));
        tr.addEventListener("keydown", (event) => handleRowKeydown(event, row));
        addCreativeCell(tr, row);
        addPillCell(tr, row.batch_state, batchStateLabel(row.batch_state), "Status");
        addStackCell(
          tr,
          row.issue_codes.length ? row.issue_codes.map(humanizeCode).join(", ") : "No action needed",
          (row.owners.join(", ") || "No owner") + " · " + (row.proposed_fix || "No fix required"),
          "issue-cell",
          "What needs attention"
        );
        addPillCell(tr, row.review_status, reviewStatusLabel(row.review_status), "Decision");
        tbody.appendChild(tr);
      }
      document.getElementById("table-caption").textContent = `${visibleRows.length} creatives in this view`;
      updateProgress(visibleRows);
    }

    function addCreativeCell(tr, row) {
      const td = document.createElement("td");
      td.dataset.label = "Creative";
      const wrap = document.createElement("div");
      wrap.className = "creative-cell";
      const thumb = document.createElement("div");
      thumb.className = "creative-thumb format-" + normalizedFormat(row.format) + " tone-" + campaignTone(row.campaign_key);
      thumb.setAttribute("aria-hidden", "true");
      const thumbLabel = document.createElement("span");
      thumbLabel.textContent = row.format.slice(0, 3).toUpperCase();
      const thumbShape = document.createElement("i");
      thumb.append(thumbLabel, thumbShape);
      const meta = document.createElement("div");
      meta.className = "creative-meta";
      const name = document.createElement("strong");
      name.className = "mono";
      name.textContent = row.creative_id;
      const detail = document.createElement("span");
      detail.textContent = "row " + row.source_row + " · " + row.account_id_alias;
      meta.append(name, detail);
      wrap.append(thumb, meta);
      td.appendChild(wrap);
      tr.appendChild(td);
    }

    function addCell(tr, value, className, label) {
      const td = document.createElement("td");
      td.textContent = value || "";
      td.dataset.label = label || "";
      if (className) td.className = className;
      tr.appendChild(td);
    }

    function addStackCell(tr, primary, secondary, className, label) {
      const td = document.createElement("td");
      td.dataset.label = label || "";
      if (className) td.className = className;
      const strong = document.createElement("strong");
      strong.textContent = primary || "";
      const sub = document.createElement("span");
      sub.textContent = secondary || "";
      td.append(strong, sub);
      tr.appendChild(td);
    }

    function addPillCell(tr, value, label, dataLabel) {
      const td = document.createElement("td");
      td.dataset.label = dataLabel || "";
      const span = document.createElement("span");
      span.className = `state ${value}`;
      span.textContent = label;
      td.appendChild(span);
      tr.appendChild(td);
    }

    function selectRow(sourceRow, openDetail, restoreFocus) {
      activeRow = sourceRow;
      const row = rows.find((item) => item.source_row === sourceRow);
      if (!row) return;
      lastFocusedRow = row.source_row;
      detailTitle.textContent = row.creative_id + " · row " + row.source_row;
      approveButton.disabled = row.batch_state === "blocked";
      approveButton.title = row.batch_state === "blocked" ? "Resolve offline blockers before dry-run export confirmation." : "Confirm this row for dry-run export in local review state.";
      approveButton.textContent = row.batch_state === "blocked"
        ? "Resolve blocker first"
        : row.issue_codes.includes("duplicate_asset")
          ? "Confirm reuse for dry-run export"
          : "Confirm for dry-run export";
      fixButton.disabled = false;
      blockButton.disabled = false;
      reviewNote.value = row.note || "";
      if (row.updated_by_role) {
        reviewerRole.value = row.updated_by_role;
      } else if (row.owners.length && reviewerRoles.has(row.owners[0])) {
        reviewerRole.value = row.owners[0];
      }
      detailGrid.replaceChildren();
      [
        ["Campaign", row.campaign_key],
        ["Ad Set", row.adset_key],
        ["Account", row.account_id_alias],
        ["Placement", row.placement],
        ["Format", row.format],
        ["UTM Campaign", row.utm_campaign],
        ["UTM Status", row.utm_status],
        ["Post ID", row.post_id],
        ["Intent", row.operation_intent],
        ["Idempotency", row.idempotency_key],
        ["Source", row.source_lineage],
        ["Destination", row.destination_url]
      ].forEach(([label, value]) => addField(label, value));
      previewText.textContent = row.primary_text;
      previewHeadline.textContent = row.headline;
      previewUrl.textContent = row.final_url_preview;
      previewArt.className = "proof-visual format-" + normalizedFormat(row.format) + " tone-" + campaignTone(row.campaign_key);
      previewFormat.textContent = row.format + " · synthetic proof";
      issueList.replaceChildren();
      if (!row.issues.length) {
        const clean = document.createElement("div");
        clean.className = "issue clean";
        clean.textContent = "No issues detected by the offline checks.";
        issueList.appendChild(clean);
      } else {
        for (const issue of row.issues) {
          const item = document.createElement("div");
          item.className = "issue";
          const title = document.createElement("strong");
          title.textContent = humanizeCode(issue.code) + " · " + issue.owner;
          const message = document.createElement("div");
          message.textContent = issue.message;
          const fix = document.createElement("div");
          fix.className = "subtle";
          fix.textContent = issue.proposed_fix;
          item.append(title, message, fix);
          issueList.appendChild(item);
        }
      }
      renderRows();
      if (restoreFocus) {
        const active = tbody.querySelector('tr[data-source-row="' + row.source_row + '"]');
        if (active) active.focus();
      }
      if (openDetail && window.matchMedia("(max-width: 1023px)").matches) {
        detailShell.inert = false;
        detailShell.removeAttribute("aria-hidden");
        detailShell.classList.add("open");
        detailShell.setAttribute("role", "dialog");
        detailShell.setAttribute("aria-modal", "true");
        document.body.classList.add("detail-open");
        detailClose.focus();
      }
    }

    function closeRowDetail() {
      detailShell.classList.remove("open");
      detailShell.removeAttribute("role");
      detailShell.removeAttribute("aria-modal");
      document.body.classList.remove("detail-open");
      const row = tbody.querySelector('tr[data-source-row="' + lastFocusedRow + '"]');
      if (row) row.focus();
      if (window.matchMedia("(max-width: 1023px)").matches) {
        detailShell.inert = true;
        detailShell.setAttribute("aria-hidden", "true");
      }
    }

    function syncDetailInteractivity() {
      const compact = window.matchMedia("(max-width: 1023px)").matches;
      if (compact && !detailShell.classList.contains("open")) {
        detailShell.inert = true;
        detailShell.setAttribute("aria-hidden", "true");
      } else if (!compact) {
        detailShell.inert = false;
        detailShell.removeAttribute("aria-hidden");
        detailShell.classList.remove("open");
        document.body.classList.remove("detail-open");
      }
    }

    function trapDetailFocus(event) {
      if (event.key !== "Tab" || confirmPanel.open || !detailShell.classList.contains("open")) return;
      const focusable = Array.from(detailShell.querySelectorAll("button, select, textarea, input, [href]")).filter((item) => !item.disabled);
      if (!focusable.length) return;
      const first = focusable[0];
      const last = focusable[focusable.length - 1];
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    }

    function addField(label, value) {
      const field = document.createElement("div");
      field.className = "field";
      const name = document.createElement("span");
      name.textContent = label;
      const content = document.createElement("div");
      content.className = "mono";
      content.textContent = value || "";
      field.append(name, content);
      detailGrid.appendChild(field);
    }

    function findGuidedRow() {
      return rows.find((row) =>
        row.batch_state === "needs_review"
        && row.issue_codes.includes("duplicate_asset")
        && row.review_status === "needs_confirmation"
      ) || rows.find((row) =>
        row.batch_state === "needs_review" && row.review_status === "needs_confirmation"
      ) || rows.find((row) =>
        row.batch_state === "needs_review" && row.issue_codes.includes("duplicate_asset")
      ) || rows.find((row) => row.batch_state === "needs_review") || null;
    }

    function guidedIssueFor(row) {
      return row.issues.find((issue) => issue.code.includes("duplicate_asset"))
        || row.issues[0]
        || { code: "human_review", owner: row.owners[0] || "Reviewer", proposed_fix: row.proposed_fix || "Record an explicit decision." };
    }

    function renderGuidedStep() {
      const row = rows.find((item) => item.source_row === guidedSourceRow);
      guidedCase.hidden = guidedStep === 3 || !row;
      guidedStepOne.hidden = guidedStep !== 1;
      guidedStepTwo.hidden = guidedStep !== 2;
      guidedStepThree.hidden = guidedStep !== 3;
      guidedCase.classList.toggle("guided-highlight", guidedStep === 1);
      guidedDecisionLocked = guidedStep === 3;
      guidedStepTwo.querySelectorAll("button").forEach((button) => { button.disabled = guidedDecisionLocked; });
      if (guidedStep === 1) {
        guidedProgress.textContent = "1 of 3 · Detect";
        guidedTitle.textContent = "Find the ambiguous row.";
        guidedCopy.textContent = "The workflow separated a possible duplicate from rows that can pass or must return for fixes.";
      } else if (guidedStep === 2) {
        guidedProgress.textContent = "2 of 3 · Decide";
        guidedTitle.textContent = "Make the human decision.";
        guidedCopy.textContent = "Confirm intentional reuse for dry-run export, return it for a fix or block it from the dry-run export.";
      } else {
        guidedProgress.textContent = "3 of 3 · Prove";
        guidedTitle.textContent = row ? "Inspect what changed." : "No ambiguous case exists in this batch.";
        guidedCopy.textContent = row
          ? "The decision and audit event are now inspectable."
          : "The guided path could not find a row that requires a human decision. You can still explore the full queue.";
      }
      guidedTitle.focus();
    }

    function startGuidedDemo() {
      const row = findGuidedRow();
      guidedActive = true;
      guidedDecisionLocked = false;
      if (!row) {
        guidedSourceRow = null;
        guidedStep = 3;
        document.getElementById("guided-result-state").textContent = "no pending decision";
        document.getElementById("guided-result-role").textContent = "not applicable";
        document.getElementById("guided-result-event").textContent = "none";
        document.getElementById("guided-result-creative").textContent = "none";
        document.getElementById("guided-result-time").textContent = "not applicable";
        document.getElementById("guided-result-copy").textContent = "No ambiguous case exists in this batch.";
      } else {
        const issue = guidedIssueFor(row);
        guidedSourceRow = row.source_row;
        guidedStep = 1;
        searchInput.value = "";
        ownerFilter.value = "all";
        setActiveFilter("needs_review");
        selectRow(row.source_row, false, false);
        document.getElementById("guided-creative").textContent = row.creative_id + " · row " + row.source_row;
        document.getElementById("guided-issue").textContent = humanizeCode(issue.code);
        document.getElementById("guided-owner").textContent = issue.owner;
        document.getElementById("guided-fix").textContent = issue.proposed_fix;
      }
      if (!guidedDialog.open) guidedDialog.showModal();
      renderGuidedStep();
    }

    function advanceGuidedDemo() {
      if (!guidedActive || guidedStep !== 1 || guidedSourceRow === null) return;
      guidedStep = 2;
      renderGuidedStep();
    }

    function makeGuidedDecision(status, decision) {
      if (!guidedActive || guidedStep !== 2 || guidedDecisionLocked) return;
      const row = rows.find((item) => item.source_row === guidedSourceRow);
      if (!row) return;
      guidedDecisionLocked = true;
      guidedStepTwo.querySelectorAll("button").forEach((button) => { button.disabled = true; });
      activeRow = row.source_row;
      updateReview(status, decision);
    }

    function completeGuidedDemo(row, event) {
      guidedStep = 3;
      document.getElementById("guided-result-state").textContent = reviewStatusLabel(row.review_status);
      document.getElementById("guided-result-role").textContent = event.actor_role;
      document.getElementById("guided-result-event").textContent = event.event_type;
      document.getElementById("guided-result-creative").textContent = event.creative_id;
      document.getElementById("guided-result-time").textContent = event.occurred_at;
      document.getElementById("guided-result-copy").textContent = "Decision recorded in browser-local state. No external system was changed. Technical receipt: mutation_allowed:false.";
      renderGuidedStep();
    }

    function exitGuidedDemo() {
      guidedActive = false;
      guidedStep = 0;
      guidedSourceRow = null;
      guidedDecisionLocked = false;
      guidedCase.classList.remove("guided-highlight");
      if (guidedDialog.open) guidedDialog.close();
      const nextUrl = new URL(window.location.href);
      nextUrl.searchParams.delete("guided");
      history.replaceState(null, "", nextUrl.pathname + nextUrl.search + nextUrl.hash);
      if (detailShell.classList.contains("open")) closeRowDetail();
      setActiveFilter("all");
      const selectedRow = tbody.querySelector('tr[data-source-row="' + activeRow + '"]');
      if (selectedRow) {
        selectedRow.focus();
      } else {
        document.getElementById("review-workspace").focus();
      }
    }

    function patchRowDecision(row, status, decision, eventType) {
      const patch = {
        review_status: status,
        decision,
        note: reviewNote.value.trim(),
        updated_by_role: reviewerRole.value,
        updated_at: new Date().toISOString()
      };
      persisted.rows[row.source_row] = Object.assign({}, persisted.rows[row.source_row] || {}, patch);
      const event = {
        event_id: `evt_local_${Date.now()}_${row.source_row}`,
        event_type: eventType,
        actor_role: reviewerRole.value,
        source_row: row.source_row,
        creative_id: row.creative_id,
        decision,
        occurred_at: patch.updated_at
      };
      persisted.audit.unshift(event);
      return event;
    }

    function updateReview(status, decision) {
      const row = rows.find((item) => item.source_row === activeRow);
      if (!row) return;
      if (status === "confirmed_ready" && row.batch_state === "blocked") {
        statusLine.textContent = "Resolve offline blockers before dry-run export confirmation.";
        return;
      }
      rememberUndo();
      const event = patchRowDecision(row, status, decision, "row_decision_updated");
      saveState();
      statusLine.textContent = "Saved row " + row.source_row + " as " + reviewStatusLabel(status).toLowerCase() + ".";
      selectRow(row.source_row, !guidedActive, false);
      if (guidedActive && guidedStep === 2 && row.source_row === guidedSourceRow) {
        completeGuidedDemo(rows.find((item) => item.source_row === row.source_row) || row, event);
      }
    }

    function rememberUndo() {
      undoSnapshot = JSON.parse(JSON.stringify(persisted));
      undoButton.disabled = false;
    }

    function requestBulkUpdate(status, decision) {
      const visibleRows = filteredRows();
      if (!visibleRows.length) {
        statusLine.textContent = "No visible rows to update.";
        return;
      }
      const targetRows = status === "confirmed_ready"
        ? visibleRows.filter((row) => row.batch_state !== "blocked")
        : visibleRows;
      const skipped = visibleRows.length - targetRows.length;
      if (!targetRows.length) {
        statusLine.textContent = "No visible rows are eligible for dry-run export confirmation.";
        return;
      }
      confirmTrigger = document.activeElement;
      pendingAction = {
        kind: "bulk",
        status,
        decision,
        sourceRows: targetRows.map((row) => row.source_row)
      };
      const targetLabel = targetRows.length + " visible row" + (targetRows.length === 1 ? "" : "s");
      const question = status === "confirmed_ready"
        ? "Confirm " + targetLabel + " for dry-run export? "
        : status === "needs_fix"
          ? "Return " + targetLabel + " for fix? "
          : "Block " + targetLabel + " from dry-run export? ";
      confirmCopy.textContent = question
        + (skipped ? skipped + " blocked rows will stay unchanged. " : "")
        + "This only changes local review state.";
      confirmPanel.showModal();
      document.getElementById("confirm-action").focus();
    }

    function updateVisibleRows(status, decision, sourceRows) {
      const targetRows = rows.filter((row) => sourceRows.includes(row.source_row));
      rememberUndo();
      targetRows.forEach((row) => patchRowDecision(row, status, decision, "bulk_row_decision_updated"));
      saveState();
      statusLine.textContent = "Saved " + targetRows.length + " rows as " + reviewStatusLabel(status).toLowerCase() + ".";
      reconcileSelection();
    }

    function requestReset() {
      confirmTrigger = document.activeElement;
      pendingAction = { kind: "reset" };
      confirmCopy.textContent = "Reset every local review decision for this batch?";
      confirmPanel.showModal();
      document.getElementById("confirm-action").focus();
    }

    function confirmPendingAction() {
      if (!pendingAction) return;
      const action = pendingAction;
      pendingAction = null;
      confirmPanel.close();
      if (action.kind === "bulk") {
        updateVisibleRows(action.status, action.decision, action.sourceRows);
      } else if (action.kind === "reset") {
        performReset();
      }
      if (confirmTrigger && document.contains(confirmTrigger)) confirmTrigger.focus();
      confirmTrigger = null;
    }

    function cancelPendingAction() {
      pendingAction = null;
      confirmPanel.close();
      statusLine.textContent = "No changes made.";
      if (confirmTrigger && document.contains(confirmTrigger)) confirmTrigger.focus();
      confirmTrigger = null;
    }

    function undoLastAction() {
      if (!undoSnapshot) return;
      persisted = undoSnapshot;
      undoSnapshot = null;
      undoButton.disabled = true;
      saveState();
      statusLine.textContent = "Restored the previous local review state.";
      renderOwnerOptions();
      reconcileSelection();
    }

    function updateProgress(visibleRows) {
      const counts = rows.reduce((acc, row) => {
        acc[row.review_status] = (acc[row.review_status] || 0) + 1;
        return acc;
      }, {});
      const confirmed = counts.confirmed_ready || 0;
      const needsFix = counts.needs_fix || 0;
      const blocked = counts.blocked || 0;
      const total = rows.length;
      visibleCount.textContent = `${visibleRows.length} visible of ${total} rows`;
      reviewProgress.textContent = `${confirmed} confirmed for dry-run export, ${needsFix} returned for fix, ${blocked} blocked from dry-run export`;
    }

    function downloadState() {
      const blob = new Blob([JSON.stringify(exportState(), null, 2)], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `meta-importer-${workspaceData.batch_id}-review-state.json`;
      link.click();
      URL.revokeObjectURL(url);
      statusLine.textContent = "State export prepared.";
    }

    async function copyState() {
      await navigator.clipboard.writeText(JSON.stringify(exportState(), null, 2));
      statusLine.textContent = "State JSON copied.";
    }

    function performReset() {
      rememberUndo();
      localStorage.removeItem(storageKey);
      persisted = { rows: {}, audit: workspaceData.audit_events.slice() };
      rows = mergeRows();
      statusLine.textContent = "Browser review state reset.";
      renderOwnerOptions();
      selectRow(filteredRows().length ? filteredRows()[0].source_row : null, false, false);
    }

    function importStatePayload(payload) {
      if (!payload || payload.batch_id !== workspaceData.batch_id) {
        statusLine.textContent = "Imported state belongs to a different batch.";
        return;
      }
      if (payload.mutation_allowed !== false || payload.meta_api_compatibility !== "not_claimed") {
        statusLine.textContent = "Imported state failed the local-only guardrail.";
        return;
      }
      const validated = validatedPersistedState(payload);
      if (!validated) {
        statusLine.textContent = "Imported state failed structural validation.";
        return;
      }
      rememberUndo();
      persisted = validated;
      saveState();
      statusLine.textContent = "Imported local review state.";
      renderOwnerOptions();
      selectRow(filteredRows().length ? filteredRows()[0].source_row : null, false, false);
    }

    function setActiveFilter(value) {
      activeFilter = value;
      filterButtons.forEach((item) => {
        const active = item.dataset.filter === value;
        item.classList.toggle("active", active);
        item.setAttribute("aria-pressed", String(active));
      });
      reconcileSelection();
      document.getElementById("review-workspace").scrollIntoView({ block: "start" });
    }

    filterButtons.forEach((button) => {
      button.addEventListener("click", () => setActiveFilter(button.dataset.filter));
    });
    quickFilterButtons.forEach((button) => {
      button.addEventListener("click", () => setActiveFilter(button.dataset.quickFilter));
    });
    document.getElementById("start-guided").addEventListener("click", startGuidedDemo);
    document.getElementById("guided-next").addEventListener("click", advanceGuidedDemo);
    document.getElementById("guided-confirm").addEventListener("click", () => makeGuidedDecision("confirmed_ready", "approved_for_dry_run_export"));
    document.getElementById("guided-fix-action").addEventListener("click", () => makeGuidedDecision("needs_fix", "requires_fix"));
    document.getElementById("guided-block").addEventListener("click", () => makeGuidedDecision("blocked", "blocked_from_export"));
    document.getElementById("guided-close").addEventListener("click", exitGuidedDemo);
    document.getElementById("guided-explore").addEventListener("click", exitGuidedDemo);
    document.getElementById("guided-replay").addEventListener("click", startGuidedDemo);
    guidedDialog.addEventListener("cancel", (event) => {
      event.preventDefault();
      exitGuidedDemo();
    });
    searchInput.addEventListener("input", reconcileSelection);
    ownerFilter.addEventListener("change", reconcileSelection);
    approveButton.addEventListener("click", () => updateReview("confirmed_ready", "approved_for_dry_run_export"));
    fixButton.addEventListener("click", () => updateReview("needs_fix", "requires_fix"));
    blockButton.addEventListener("click", () => updateReview("blocked", "blocked_from_export"));
    document.getElementById("bulk-ready").addEventListener("click", () => requestBulkUpdate("confirmed_ready", "bulk_approved_for_dry_run_export"));
    document.getElementById("bulk-fix").addEventListener("click", () => requestBulkUpdate("needs_fix", "bulk_requires_fix"));
    document.getElementById("bulk-blocked").addEventListener("click", () => requestBulkUpdate("blocked", "bulk_blocked_from_export"));
    document.getElementById("confirm-action").addEventListener("click", confirmPendingAction);
    document.getElementById("cancel-action").addEventListener("click", cancelPendingAction);
    confirmPanel.addEventListener("cancel", (event) => {
      event.preventDefault();
      cancelPendingAction();
    });
    document.getElementById("download-state").addEventListener("click", downloadState);
    document.getElementById("copy-state").addEventListener("click", () => copyState().catch(() => {
      statusLine.textContent = "Clipboard unavailable.";
    }));
    document.getElementById("reset-state").addEventListener("click", requestReset);
    undoButton.addEventListener("click", undoLastAction);
    detailClose.addEventListener("click", closeRowDetail);
    document.addEventListener("keydown", (event) => {
      trapDetailFocus(event);
      if (event.key === "Escape" && !confirmPanel.open && detailShell.classList.contains("open")) closeRowDetail();
    });
    window.addEventListener("resize", () => { syncDetailInteractivity(); syncFilterDisclosure(); });
    stateImport.addEventListener("change", () => {
      const file = stateImport.files && stateImport.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = () => {
        try {
          importStatePayload(JSON.parse(String(reader.result || "{}")));
        } catch (_error) {
          statusLine.textContent = "Imported state is not valid JSON.";
        }
      };
      reader.readAsText(file);
      stateImport.value = "";
    });

    renderOwnerOptions();
    syncFilterDisclosure();
    syncDetailInteractivity();
    if (persistedLoadError) {
      statusLine.textContent = "Saved browser state could not be read; using seeded review state.";
    }
    selectRow(activeRow, false, false);
    if (new URLSearchParams(window.location.search).get("guided") === "1") {
      startGuidedDemo();
    }
  </script>
</body>
</html>
"""
    return (
        template.replace("__WORKSPACE_DATA__", _json_script(state_payload))
        .replace("__BATCH_ID__", _escape_html(str(state_payload["batch_id"])))
        .replace("__BATCH_SHORT__", _escape_html(str(state_payload["batch_id"])[:8]))
        .replace("__DATA_CLASSIFICATION__", _escape_html(str(state_payload["data_classification"])))
        .replace("__DATA_BADGE__", _escape_html(data_badge))
        .replace("__DATA_SCOPE_GUARDRAIL__", _escape_html(data_scope_guardrail))
        .replace("__ROW_COUNT__", str(summary["row_count"]))
        .replace("__LAUNCH_READY__", str(states.get("launch_ready", 0)))
        .replace("__REVIEW_COUNT__", str(states.get("needs_review", 0)))
        .replace("__BLOCKED_COUNT__", str(states.get("blocked", 0)))
        .replace("__OWNER_QUEUE__", _html_queue(owner_queue))
        .replace("__ISSUE_QUEUE__", _html_queue(issue_codes, humanize_labels=True))
    )


def _validate_rows(rows: list[ManifestRow]) -> tuple[Issue, ...]:
    issues: list[Issue] = []
    destinations_by_adset: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        if row.adset_key and row.destination_url:
            destinations_by_adset[row.adset_key][row.destination_url] += 1

    dominant_destination_by_adset = {
        adset: counts.most_common(1)[0][0]
        for adset, counts in destinations_by_adset.items()
        if counts
    }

    for row in rows:
        issues.extend(_required_field_issues(row))

        if row.approval_status not in APPROVAL_STATUSES:
            issues.append(
                Issue(
                    row.source_row,
                    row.creative_id,
                    "blocker",
                    "invalid_approval_status",
                    "Creative Ops Manager",
                    "Approval status is not recognized.",
                    "Use approved, pending, or rejected.",
                )
            )
        elif row.approval_status != "approved" and row.qa_issue != "missing_approval":
            issues.append(
                Issue(
                    row.source_row,
                    row.creative_id,
                    "blocker",
                    f"{row.approval_status}_approval",
                    "Approver",
                    f"Creative is {row.approval_status}, not approved.",
                    "Approve the creative or remove it from this launch batch.",
                )
            )

        if row.format and row.format not in SUPPORTED_FORMATS and row.qa_issue != "unsupported_format":
            issues.append(_policy_issue(row, "unsupported_format"))

        if row.qa_issue:
            issues.append(_policy_issue(row, row.qa_issue))

        issues.extend(_launch_contract_issues(row))

        if row.asset_path and row.qa_issue != "duplicate_asset" and _is_later_duplicate(row, rows):
            issues.append(
                Issue(
                    row.source_row,
                    row.creative_id,
                    "warning",
                    "duplicate_asset_detected",
                    "Creative Ops Manager",
                    "The same asset path appears in multiple rows.",
                    "Confirm reuse is intentional or replace one duplicate.",
                )
            )

        dominant_destination = dominant_destination_by_adset.get(row.adset_key)
        if (
            dominant_destination
            and row.destination_url
            and row.destination_url != dominant_destination
            and row.qa_issue != "destination_mismatch"
        ):
            issues.append(
                Issue(
                    row.source_row,
                    row.creative_id,
                    "blocker",
                    "adset_destination_mismatch",
                    "Media Buyer",
                    "Destination URL differs from the dominant URL for this ad set.",
                    "Correct the destination or move the creative to the intended ad set.",
                )
            )

    issues.extend(_idempotency_collision_issues(rows))
    return tuple(issues)


def _launch_contract_issues(row: ManifestRow) -> list[Issue]:
    issues: list[Issue] = []
    if row.objective and row.objective not in SUPPORTED_OBJECTIVES:
        issues.append(
            Issue(
                row.source_row,
                row.creative_id,
                "blocker",
                "unsupported_objective",
                "Media Buyer",
                "Objective is not supported by the offline launch contract.",
                "Use one of the supported objective aliases before export.",
            )
        )
    if row.placement:
        if row.placement not in SUPPORTED_PLACEMENTS:
            issues.append(
                Issue(
                    row.source_row,
                    row.creative_id,
                    "blocker",
                    "unsupported_placement",
                    "Media Buyer",
                    "Placement is not supported by the offline launch contract.",
                    "Map the row to a supported placement before export.",
                )
            )
        elif row.format in PLACEMENTS_BY_FORMAT and row.placement not in PLACEMENTS_BY_FORMAT[row.format]:
            issues.append(
                Issue(
                    row.source_row,
                    row.creative_id,
                    "blocker",
                    "format_placement_mismatch",
                    "Media Buyer",
                    "Format and placement are not compatible in the launch contract.",
                    "Move the creative to a compatible placement or replace the asset format.",
                )
            )
    if row.utm_campaign and row.utm_campaign != row.campaign_key:
        issues.append(
            Issue(
                row.source_row,
                row.creative_id,
                "blocker",
                "utm_campaign_mismatch",
                "Media Buyer",
                "UTM campaign does not match the mapped campaign key.",
                "Set `utm_campaign` to the campaign key or remap the row.",
            )
        )
    utm_values = [row.utm_source, row.utm_medium, row.utm_campaign, row.utm_content, row.utm_term]
    if any(utm_values) and not all([row.utm_source, row.utm_medium, row.utm_campaign, row.utm_content]):
        issues.append(
            Issue(
                row.source_row,
                row.creative_id,
                "warning",
                "partial_utm_mapping",
                "Media Buyer",
                "UTM mapping is partially filled.",
                "Fill source, medium, campaign, and content so tracking is reviewable.",
            )
        )
    has_utm_creative_lineage = bool(row.creative_id and row.creative_id in row.utm_content)
    has_utm_variant_lineage = bool(row.variant_group and row.variant_group in row.utm_content)
    if row.utm_content and not (has_utm_creative_lineage or has_utm_variant_lineage):
        issues.append(
            Issue(
                row.source_row,
                row.creative_id,
                "warning",
                "utm_content_lineage_missing",
                "Media Buyer",
                "UTM content does not include the creative or variant lineage.",
                "Include the creative ID or variant group in `utm_content`.",
            )
        )
    if row.post_id_type and row.post_id_type not in SUPPORTED_POST_ID_TYPES:
        issues.append(
            Issue(
                row.source_row,
                row.creative_id,
                "blocker",
                "unsupported_post_id_type",
                "Media Buyer",
                "Post ID type is not supported by the offline launch contract.",
                "Use new, existing, or placeholder.",
            )
        )
    if row.post_id and not row.post_id_type:
        issues.append(
            Issue(
                row.source_row,
                row.creative_id,
                "warning",
                "post_id_type_missing",
                "Media Buyer",
                "Post ID is set without a post_id_type.",
                "Set post_id_type so reuse/new-post intent is explicit.",
            )
        )
    if row.post_id_type == "existing" and not row.post_id:
        issues.append(
            Issue(
                row.source_row,
                row.creative_id,
                "blocker",
                "existing_post_id_missing",
                "Media Buyer",
                "Existing post lineage is declared but post_id is missing.",
                "Provide the post ID alias or change post_id_type.",
            )
        )
    if bool(row.source_system) != bool(row.source_row_id):
        issues.append(
            Issue(
                row.source_row,
                row.creative_id,
                "blocker",
                "incomplete_source_lineage",
                "Creative Ops Manager",
                "Source lineage requires both source_system and source_row_id.",
                "Provide both source fields or leave both blank.",
            )
        )
    if row.reviewer and not row.approved_at:
        issues.append(
            Issue(
                row.source_row,
                row.creative_id,
                "warning",
                "reviewer_without_approved_at",
                "Approver",
                "Reviewer is set but approved_at is missing.",
                "Add the approval timestamp or clear the reviewer.",
            )
        )
    return issues


def _idempotency_collision_issues(rows: list[ManifestRow]) -> list[Issue]:
    keyed_rows: dict[str, list[ManifestRow]] = defaultdict(list)
    for row in rows:
        keyed_rows[_idempotency_key_for(row)].append(row)

    issues: list[Issue] = []
    for _key, matching in keyed_rows.items():
        if len(matching) < 2:
            continue
        explicit_reuse = all(
            row.post_id_type in {"existing", "placeholder"} or row.qa_issue == "duplicate_asset"
            for row in matching
        )
        if explicit_reuse:
            continue
        for row in matching:
            issues.append(
                Issue(
                    row.source_row,
                    row.creative_id,
                    "blocker",
                    "idempotency_collision",
                    "Data Model / Import Pipeline Lead",
                    "Two rows resolve to the same dry-run idempotency key without explicit reuse intent.",
                    "Change the creative mapping or mark explicit reuse intent before export.",
                )
            )
    return issues


def _is_later_duplicate(row: ManifestRow, rows: list[ManifestRow]) -> bool:
    matching = [item for item in rows if item.asset_path and item.asset_path == row.asset_path]
    if len(matching) < 2:
        return False
    return row.source_row != min(item.source_row for item in matching)


def _required_field_issues(row: ManifestRow) -> list[Issue]:
    issues: list[Issue] = []
    required = {
        "creative_id": row.creative_id,
        "campaign_key": row.campaign_key,
        "adset_key": row.adset_key,
        "format": row.format,
        "asset_path": row.asset_path,
        "primary_text": row.primary_text,
        "headline": row.headline,
        "destination_url": row.destination_url,
        "approval_status": row.approval_status,
    }
    for field, value in required.items():
        if not value:
            issues.append(
                Issue(
                    row.source_row,
                    row.creative_id,
                    "blocker",
                    f"missing_{field}",
                    "Creative Ops Manager",
                    f"Required manifest field `{field}` is missing.",
                    f"Fill `{field}` before export.",
                )
            )

    if row.destination_url and not _is_valid_http_url(row.destination_url):
        issues.append(
            Issue(
                row.source_row,
                row.creative_id,
                "blocker",
                "invalid_destination_url",
                "Media Buyer",
                "Destination URL is not a valid HTTP(S) URL.",
                "Use a valid landing-page URL.",
            )
        )
    return issues


def _policy_issue(row: ManifestRow, code: str) -> Issue:
    policy = ISSUE_POLICY.get(code)
    if not policy:
        return Issue(
            row.source_row,
            row.creative_id,
            "warning",
            "unknown_fixture_issue",
            "Creative Ops Manager",
            f"Fixture issue `{code}` is not recognized by the prototype.",
            "Map the issue to a supported launch-workspace rule.",
        )
    severity, owner, message, fix = policy
    return Issue(row.source_row, row.creative_id, severity, code, owner, message, fix)


def _candidate_for(row: ManifestRow, row_issues: list[Issue]) -> AdCandidate:
    issue_count = len(row_issues)
    has_blocker = any(issue.severity == "blocker" for issue in row_issues)
    batch_state = "blocked" if has_blocker else "needs_review" if issue_count else "launch_ready"
    name = f"{row.campaign_key}::{row.adset_key}::{row.creative_id}::{row.format}"
    idempotency_key = _idempotency_key_for(row)
    operation_intent = (
        "reuse_existing_post"
        if row.post_id_type == "existing" and row.post_id
        else "create_new_ad"
    )
    final_url_preview = _final_url_preview(row)
    return AdCandidate(
        source_row=row.source_row,
        creative_id=row.creative_id,
        campaign_key=row.campaign_key,
        adset_key=row.adset_key,
        format=row.format,
        asset_path=row.asset_path,
        destination_url=row.destination_url,
        account_id_alias=row.account_id_alias,
        objective=row.objective,
        placement=row.placement,
        asset_hash=row.asset_hash,
        variant_group=row.variant_group,
        hook=row.hook,
        language=row.language,
        country=row.country,
        utm_source=row.utm_source,
        utm_medium=row.utm_medium,
        utm_campaign=row.utm_campaign,
        utm_content=row.utm_content,
        utm_term=row.utm_term,
        final_url_preview=final_url_preview,
        post_id=row.post_id,
        post_id_type=row.post_id_type,
        source_system=row.source_system,
        source_row_id=row.source_row_id,
        reviewer=row.reviewer,
        approved_at=row.approved_at,
        name=name,
        idempotency_key=idempotency_key,
        operation_intent=operation_intent,
        batch_state=batch_state,
        issue_count=issue_count,
    )


def _idempotency_key_for(row: ManifestRow) -> str:
    key_source = "|".join(
        [
            row.account_id_alias,
            row.campaign_key,
            row.adset_key,
            row.creative_id,
            row.asset_path,
            row.destination_url,
            row.placement,
            row.post_id,
        ]
    )
    return hashlib.sha256(key_source.encode()).hexdigest()[:16]


def _summarize(
    rows: list[ManifestRow], candidates: tuple[AdCandidate, ...], issues: tuple[Issue, ...]
) -> dict[str, object]:
    return {
        "row_count": len(rows),
        "campaign_count": len({row.campaign_key for row in rows if row.campaign_key}),
        "adset_count": len({row.adset_key for row in rows if row.adset_key}),
        "formats": sorted({row.format for row in rows if row.format}),
        "batch_states": dict(Counter(candidate.batch_state for candidate in candidates)),
        "issue_severity": dict(Counter(issue.severity for issue in issues)),
        "issue_codes": dict(Counter(issue.code for issue in issues)),
        "owner_queue": dict(Counter(issue.owner for issue in issues)),
        "launch_contract": {
            "account_alias_rows": sum(1 for row in rows if row.account_id_alias),
            "placement_rows": sum(1 for row in rows if row.placement),
            "utm_rows": sum(
                1
                for row in rows
                if any([row.utm_source, row.utm_medium, row.utm_campaign, row.utm_content, row.utm_term])
            ),
            "post_id_rows": sum(1 for row in rows if row.post_id),
            "post_decision_rows": sum(1 for row in rows if row.post_id_type),
            "source_lineage_rows": sum(1 for row in rows if row.source_system and row.source_row_id),
        },
    }


def _assert_synthetic(rows: list[ManifestRow]) -> None:
    for row in rows:
        violation = _synthetic_row_violation(row)
        if violation:
            raise SyntheticDataError(violation)


def _synthetic_row_violation(row: ManifestRow) -> str:
    host = urlparse(row.destination_url).hostname
    asset = Path(row.asset_path)
    if host != SYNTHETIC_HOST:
        return (
            f"row {row.source_row} uses non-synthetic destination host `{host}`; "
            "pass --allow-real-data only after a privacy decision"
        )
    if asset.is_absolute() or ".." in asset.parts:
        return (
            f"row {row.source_row} uses asset path outside `{SYNTHETIC_ASSET_PREFIX}`; "
            "pass --allow-real-data only after a privacy decision"
        )
    try:
        resolved_prefix = SYNTHETIC_ASSET_PREFIX.resolve(strict=True)
        resolved_asset = asset.resolve(strict=False)
    except (OSError, RuntimeError):
        return f"row {row.source_row} uses missing or invalid synthetic asset path `{asset}`"
    if not _is_relative_to(resolved_asset, resolved_prefix):
        return (
            f"row {row.source_row} uses asset path outside `{SYNTHETIC_ASSET_PREFIX}`; "
            "pass --allow-real-data only after a privacy decision"
        )
    if row.account_id_alias and _looks_like_live_meta_account(row.account_id_alias):
        return (
            f"row {row.source_row} uses live-looking account alias `{row.account_id_alias}`; "
            "use a fixture alias such as acct_demo_001"
        )
    if row.post_id and row.post_id.isdigit():
        return (
            f"row {row.source_row} uses live-looking numeric post_id; "
            "use a fixture alias such as post_demo_001"
        )
    return ""


def _is_relative_to(path: Path, prefix: Path) -> bool:
    try:
        path.relative_to(prefix)
    except ValueError:
        return False
    return True


def _is_valid_http_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def _looks_like_live_meta_account(value: str) -> bool:
    lowered = value.lower()
    return lowered.startswith("act_") or value.isdigit()


def _final_url_preview(row: ManifestRow) -> str:
    utms = {
        "utm_source": row.utm_source,
        "utm_medium": row.utm_medium,
        "utm_campaign": row.utm_campaign,
        "utm_content": row.utm_content,
        "utm_term": row.utm_term,
    }
    if not any(utms.values()):
        return row.destination_url
    parsed = urlparse(row.destination_url)
    query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    for key, value in utms.items():
        if value:
            query[key] = value
    return urlunparse(parsed._replace(query=urlencode(query)))


def _source_manifest_sha256(source_manifest: str) -> str:
    if not source_manifest:
        return ""
    path = Path(source_manifest)
    if not path.exists() or not path.is_file():
        return ""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _data_classification(rows: tuple[ManifestRow, ...]) -> str:
    if all(not _synthetic_row_violation(row) for row in rows):
        return "synthetic_fixture_only"
    return "operator_supplied_manifest_no_live_mutation"


def _row_by_source(rows: tuple[ManifestRow, ...], source_row: int) -> ManifestRow:
    for row in rows:
        if row.source_row == source_row:
            return row
    raise KeyError(source_row)


def _preflight_checks_for(candidate: AdCandidate, issues: tuple[Issue, ...], prefix: str) -> dict[str, object]:
    matching = [
        issue
        for issue in issues
        if issue.source_row == candidate.source_row and prefix in issue.code
    ]
    return {
        "status": "pass" if not matching else "blocked" if any(issue.severity == "blocker" for issue in matching) else "warning",
        "codes": [issue.code for issue in matching],
    }


def _json_script(payload: dict[str, object]) -> str:
    return (
        json.dumps(payload, sort_keys=True)
        .replace("&", "\\u0026")
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
    )


def _html_queue(items: dict[str, int], *, humanize_labels: bool = False) -> str:
    if not items:
        return '<div class="queue-row"><span>None</span><strong>0</strong></div>'
    return "\n".join(
        f'<div class="queue-row"><span>{_escape_html(_humanize_issue_code(str(label)) if humanize_labels else str(label))}</span><strong>{count}</strong></div>'
        for label, count in sorted(items.items())
    )


def _humanize_issue_code(code: str) -> str:
    labels = {
        "destination_mismatch": "Destination mismatch",
        "duplicate_asset": "Possible duplicate",
        "missing_approval": "Approval missing",
        "naming_error": "Name does not match batch",
        "unsupported_format": "Format not supported",
    }
    return labels.get(code, code.replace("_", " ").capitalize())


def _html_rows(rows: list[dict[str, str]]) -> str:
    rendered = []
    for row in rows:
        state = _escape_html(row["state"])
        rendered.append(
            "<tr data-state=\"{state}\">"
            "<td><span class=\"state {state}\">{state_label}</span></td>"
            "<td class=\"mono\">{source_row}</td>"
            "<td class=\"mono\">{creative}</td>"
            "<td>{account}</td>"
            "<td>{campaign}</td>"
            "<td>{adset}</td>"
            "<td>{placement}</td>"
            "<td>{format}</td>"
            "<td class=\"mono\">{utm_campaign}</td>"
            "<td>{utm_status}</td>"
            "<td class=\"mono\">{post_id}</td>"
            "<td class=\"mono\">{source}</td>"
            "<td>{owner}</td>"
            "<td>{issue}</td>"
            "<td>{fix}</td>"
            "<td class=\"mono\">{destination}</td>"
            "</tr>".format(
                state=state,
                state_label=_escape_html(row["state"].replace("_", " ").title()),
                source_row=_escape_html(row["row"]),
                creative=_escape_html(row["creative"]),
                account=_escape_html(row["account"]),
                campaign=_escape_html(row["campaign"]),
                adset=_escape_html(row["adset"]),
                placement=_escape_html(row["placement"]),
                format=_escape_html(row["format"]),
                utm_campaign=_escape_html(row["utm_campaign"]),
                utm_status=_escape_html(row["utm_status"]),
                post_id=_escape_html(row["post_id"]),
                source=_escape_html(row["source"]),
                owner=_escape_html(row["owner"]),
                issue=_escape_html(row["issue"]),
                fix=_escape_html(row["fix"]),
                destination=_escape_html(row["destination"]),
            )
        )
    return "\n".join(rendered)


def _escape_html(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )
