from __future__ import annotations

import json
from dataclasses import dataclass
from html.parser import HTMLParser

from .html_quality import audit_workspace_html


@dataclass(frozen=True)
class BrowserQACheck:
    code: str
    passed: bool
    message: str


def audit_workspace_browser_contract(html: str) -> dict[str, object]:
    workspace_data = _workspace_data(html)
    static_audit = audit_workspace_html(html)
    checks = [
        BrowserQACheck(
            "static_accessibility_contract",
            static_audit["status"] == "pass",
            "Static workspace audit must pass before browser-behavior checks are trusted.",
        ),
        BrowserQACheck(
            "filter_counts_match_batch_states",
            _filter_counts_match(workspace_data),
            "Filter counts must match batch-state summary counts.",
        ),
        BrowserQACheck(
            "owner_filter_has_all_issue_owners",
            _owner_filter_has_all_issue_owners(workspace_data),
            "Owner filter must be able to expose every owner in the seeded review rows.",
        ),
        BrowserQACheck(
            "search_can_find_known_creative",
            _search_can_find_known_creative(workspace_data),
            "Search simulation must find a known creative id.",
        ),
        BrowserQACheck(
            "keyboard_selection_hook_present",
            'event.key === "Enter"' in html and 'event.key === " "' in html,
            "Keyboard selection must support Enter and Space.",
        ),
        BrowserQACheck(
            "empty_state_present",
            "No rows match the current filters." in html,
            "Filtered-empty state must be visible to operators and screen readers.",
        ),
        BrowserQACheck(
            "persistence_error_state_present",
            "Saved browser state could not be read" in html,
            "Corrupt browser state must fall back safely with a visible status.",
        ),
        BrowserQACheck(
            "export_controls_confirm_local_state",
            _export_controls_confirm_local_state(html, workspace_data),
            "Export controls must prepare/copy local state without enabling mutation.",
        ),
        BrowserQACheck(
            "bulk_actions_preserve_visible_scope",
            _bulk_actions_preserve_visible_scope(html, workspace_data),
            "Bulk actions must apply only to filtered visible rows and preserve local-only state.",
        ),
        BrowserQACheck(
            "state_import_has_batch_and_guardrail_checks",
            _state_import_has_batch_and_guardrail_checks(html),
            "State import must reject mismatched batches and mutation-capable payloads.",
        ),
        BrowserQACheck(
            "review_progress_present",
            "review-progress" in html and "updateProgress" in html,
            "Workspace must expose review progress to operators.",
        ),
        BrowserQACheck(
            "decision_patch_preserves_guardrails",
            _decision_patch_preserves_guardrails(workspace_data),
            "A simulated row decision must keep mutation disabled and append local audit state.",
        ),
        BrowserQACheck(
            "screen_reader_proxy_contract",
            _screen_reader_proxy_contract(static_audit),
            "Review table, filter state, and detail panel need screen-reader-oriented affordances.",
        ),
    ]
    issues = [
        {"code": check.code, "severity": "blocker", "message": check.message}
        for check in checks
        if not check.passed
    ]
    batch_states = workspace_data.get("summary", {}).get("batch_states", {})
    return {
        "contract_version": "workspace_browser_qa.v1",
        "status": "pass" if not issues else "blocked",
        "check_count": len(checks),
        "passed_count": sum(1 for check in checks if check.passed),
        "issues": issues,
        "checks": {check.code: check.passed for check in checks},
        "batch_id": workspace_data.get("batch_id", ""),
        "row_count": len(workspace_data.get("review_statuses", [])),
        "filter_counts": {
            "all": len(workspace_data.get("review_statuses", [])),
            "launch_ready": batch_states.get("launch_ready", 0),
            "needs_review": batch_states.get("needs_review", 0),
            "blocked": batch_states.get("blocked", 0),
        },
        "data_classification": workspace_data.get("data_classification", ""),
        "mutation_allowed": workspace_data.get("mutation_allowed", None),
        "meta_api_compatibility": workspace_data.get("meta_api_compatibility", ""),
    }


def _workspace_data(html: str) -> dict[str, object]:
    parser = _WorkspaceDataParser()
    parser.feed(html)
    if not parser.workspace_json:
        raise ValueError("workspace-data script tag not found")
    return json.loads(parser.workspace_json)


def _filter_counts_match(workspace_data: dict[str, object]) -> bool:
    rows = workspace_data.get("review_statuses", [])
    summary = workspace_data.get("summary", {})
    batch_states = summary.get("batch_states", {}) if isinstance(summary, dict) else {}
    if not isinstance(rows, list) or not isinstance(batch_states, dict):
        return False
    actual = {
        "launch_ready": sum(1 for row in rows if row.get("batch_state") == "launch_ready"),
        "needs_review": sum(1 for row in rows if row.get("batch_state") == "needs_review"),
        "blocked": sum(1 for row in rows if row.get("batch_state") == "blocked"),
    }
    return all(actual[state] == batch_states.get(state, 0) for state in actual)


def _owner_filter_has_all_issue_owners(workspace_data: dict[str, object]) -> bool:
    rows = workspace_data.get("review_statuses", [])
    if not isinstance(rows, list):
        return False
    owners = {owner for row in rows for owner in row.get("owners", [])}
    return {"Approver", "Creative Ops Manager", "Media Buyer"}.issubset(owners)


def _search_can_find_known_creative(workspace_data: dict[str, object]) -> bool:
    rows = workspace_data.get("review_statuses", [])
    if not isinstance(rows, list) or not rows:
        return False
    target = next(
        (str(row.get("creative_id", "")).lower() for row in rows if row.get("creative_id")),
        "",
    )
    haystacks = [
        " ".join(
            [
                str(row.get("creative_id", "")),
                str(row.get("campaign_key", "")),
                str(row.get("adset_key", "")),
                str(row.get("account_id_alias", "")),
                " ".join(row.get("issue_codes", [])),
                str(row.get("proposed_fix", "")),
            ]
        ).lower()
        for row in rows
    ]
    return bool(target) and any(target in haystack for haystack in haystacks)


def _export_controls_confirm_local_state(html: str, workspace_data: dict[str, object]) -> bool:
    export_policy = workspace_data.get("export_policy", {})
    if not isinstance(export_policy, dict):
        return False
    return all(
        token in html
        for token in ("download-state", "copy-state", "reset-state", "State export prepared.")
    ) and export_policy.get("requires_human_export_confirmation") is True


def _bulk_actions_preserve_visible_scope(html: str, workspace_data: dict[str, object]) -> bool:
    rows = workspace_data.get("review_statuses", [])
    if not isinstance(rows, list):
        return False
    blocked_rows = [row for row in rows if row.get("batch_state") == "blocked"]
    simulated_patches = {
        str(row["source_row"]): {
            "review_status": "blocked",
            "decision": "bulk_blocked_from_export",
        }
        for row in blocked_rows
    }
    return (
        all(token in html for token in ("bulk-ready", "bulk-fix", "bulk-blocked"))
        and "filteredRows()" in html
        and "targetRows.forEach" in html
        and len(simulated_patches)
        == workspace_data.get("summary", {}).get("batch_states", {}).get("blocked", -1)
        and workspace_data.get("mutation_allowed") is False
    )


def _state_import_has_batch_and_guardrail_checks(html: str) -> bool:
    required = [
        "state-import",
        "payload.batch_id !== workspaceData.batch_id",
        "payload.mutation_allowed !== false",
        'payload.meta_api_compatibility !== "not_claimed"',
        "Imported state belongs to a different batch.",
        "Imported state failed structural validation.",
        "validateRowPatches",
    ]
    return all(token in html for token in required)


def _decision_patch_preserves_guardrails(workspace_data: dict[str, object]) -> bool:
    rows = workspace_data.get("review_statuses", [])
    audit = workspace_data.get("audit_events", [])
    if not isinstance(rows, list) or not rows or not isinstance(audit, list):
        return False
    first = rows[0]
    patch = {
        "review_status": "confirmed_ready",
        "decision": "approved_for_dry_run_export",
        "note": "QA simulation",
        "updated_by_role": "QA / Evidence Lead",
        "updated_at": "2026-07-06T00:00:00Z",
    }
    patched_rows = {str(first["source_row"]): {**first, **patch}}
    exported = {
        "product": workspace_data.get("product"),
        "mode": workspace_data.get("mode"),
        "contract_version": workspace_data.get("contract_version"),
        "batch_id": workspace_data.get("batch_id"),
        "mutation_allowed": False,
        "meta_api_compatibility": "not_claimed",
        "rows": patched_rows,
        "audit": [
            {
                "event_type": "row_decision_updated",
                "source_row": first["source_row"],
                "creative_id": first["creative_id"],
                "decision": patch["decision"],
            },
            *audit,
        ],
    }
    return (
        exported["mutation_allowed"] is False
        and exported["meta_api_compatibility"] == "not_claimed"
        and exported["audit"][0]["event_type"] == "row_decision_updated"
        and str(first["source_row"]) in exported["rows"]
    )


def _screen_reader_proxy_contract(static_audit: dict[str, object]) -> bool:
    checks = static_audit.get("checks", {})
    if not isinstance(checks, dict):
        return False
    required = [
        "has_aria_live_region",
        "filter_buttons_have_aria_pressed",
        "has_table_caption",
        "has_labelled_controls",
        "has_empty_filter_state",
    ]
    return all(checks.get(item) is True for item in required)


class _WorkspaceDataParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._in_workspace_data = False
        self.workspace_json = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {key: value or "" for key, value in attrs}
        self._in_workspace_data = tag == "script" and attr_map.get("id") == "workspace-data"

    def handle_data(self, data: str) -> None:
        if self._in_workspace_data:
            self.workspace_json += data

    def handle_endtag(self, tag: str) -> None:
        if tag == "script":
            self._in_workspace_data = False
