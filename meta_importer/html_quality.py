from __future__ import annotations

from html.parser import HTMLParser


def audit_workspace_html(html: str) -> dict[str, object]:
    parser = _WorkspaceHTMLParser()
    parser.feed(html)

    filter_buttons = [
        attrs for tag, attrs in parser.start_tags if tag == "button" and attrs.get("data-filter")
    ]
    checks = {
        "has_title": "Creative Launch Workspace for Meta Ads" in html,
        "has_row_detail": "Row detail" in html,
        "has_preview": "Preview" in html,
        "has_export_panel": ">Export<" in html,
        "has_aria_live_region": parser.has_attr("aria-live"),
        "filter_buttons_have_aria_pressed": bool(filter_buttons)
        and all("aria-pressed" in attrs for attrs in filter_buttons),
        "has_table_caption": any(tag == "caption" for tag, _attrs in parser.start_tags),
        "has_labelled_controls": parser.tag_count("label") >= 3,
        "has_keyboard_row_selection": 'event.key === "Enter"' in html and 'event.key === " "' in html,
        "has_local_storage_persistence": "localStorage.getItem" in html and "localStorage.setItem" in html,
        "has_empty_filter_state": "No rows match the current filters." in html,
        "has_persistence_error_state": "Saved browser state could not be read" in html,
        "has_export_confirmation": "State export prepared." in html
        and "requires_human_export_confirmation" in html,
        "has_bulk_review_actions": all(
            token in html
            for token in ("bulk-ready", "bulk-fix", "bulk-blocked", "updateVisibleRows")
        ),
        "has_review_progress": "review-progress" in html and "updateProgress" in html,
        "has_state_import_guard": "state-import" in html
        and "Imported state belongs to a different batch." in html
        and "Imported state failed the local-only guardrail." in html
        and "Imported state failed structural validation." in html
        and "validateRowPatches" in html,
        "has_bulk_confirmation_and_undo": all(
            token in html
            for token in ("confirm-panel", "confirmPendingAction", "Undo last change", "rememberUndo")
        ),
        "has_blocker_approval_invariant": all(
            token in html
            for token in (
                'patch.review_status === "confirmed_ready"',
                'row.batch_state !== "blocked"',
                "Resolve offline blockers before local approval.",
            )
        ),
        "has_native_modal_confirmation": "<dialog" in html
        and "showModal()" in html
        and 'addEventListener("cancel"' in html,
        "has_empty_detail_state": "clearDetail" in html
        and "Change the filters or search to bring review rows back into view." in html,
        "has_mobile_detail_drawer": all(
            token in html
            for token in ("detail-shell.open", "closeRowDetail", "detailClose.focus()")
        ),
        "has_roving_row_keyboard": all(
            token in html
            for token in ("ArrowDown", "ArrowUp", 'tr.tabIndex = row.source_row === activeRow ? 0 : -1')
        ),
        "has_responsive_css": "@media (max-width:" in html,
        "has_design_system_contract": 'content="Editorial Operations v1"' in html,
        "has_ai_assist_trace": all(
            token in html
            for token in (
                "AI-assisted brief intake",
                "Policy checks",
                "Human decision",
                "No model runs in this browser",
            )
        ),
        "has_skip_link": 'class="skip-link"' in html and 'href="#review-workspace"' in html,
        "has_active_row_semantics": 'setAttribute("aria-selected"' in html,
        "has_mobile_row_cards": 'td.dataset.label' in html and 'content: attr(data-label)' in html,
        "has_reduced_motion_support": "@media (prefers-reduced-motion: reduce)" in html,
        "queue_precedes_secondary_context": html.find('class="table-shell"')
        < html.find('aria-label="Batch context"'),
        "no_generic_visual_effects": all(
            token not in html.lower()
            for token in ("linear-gradient", "radial-gradient", "box-shadow:", "backdrop-filter")
        ),
        "no_external_network_calls": all(
            token not in html.lower()
            for token in ("fetch(", "xmlhttprequest", "graph.facebook.com", "access_token")
        ),
    }
    issues = [
        {"code": code, "severity": "blocker", "message": message}
        for code, passed, message in _check_messages(checks)
        if not passed
    ]
    return {
        "contract_version": "workspace_html_static_audit.v1",
        "status": "pass" if not issues else "blocked",
        "check_count": len(checks),
        "passed_count": sum(1 for passed in checks.values() if passed),
        "issues": issues,
        "checks": checks,
        "browser_runtime": "not_available_in_static_audit",
    }


def _check_messages(checks: dict[str, bool]) -> list[tuple[str, bool, str]]:
    return [
        ("has_title", checks["has_title"], "Workspace title is missing."),
        ("has_row_detail", checks["has_row_detail"], "Row detail panel is missing."),
        ("has_preview", checks["has_preview"], "Creative preview panel is missing."),
        ("has_export_panel", checks["has_export_panel"], "Export panel is missing."),
        ("has_aria_live_region", checks["has_aria_live_region"], "Detail panel lacks aria-live."),
        (
            "filter_buttons_have_aria_pressed",
            checks["filter_buttons_have_aria_pressed"],
            "Filter buttons lack aria-pressed state.",
        ),
        ("has_table_caption", checks["has_table_caption"], "Review table lacks a caption."),
        ("has_labelled_controls", checks["has_labelled_controls"], "Expected labelled controls are missing."),
        (
            "has_keyboard_row_selection",
            checks["has_keyboard_row_selection"],
            "Row selection keyboard handling is missing.",
        ),
        (
            "has_local_storage_persistence",
            checks["has_local_storage_persistence"],
            "Browser persistence hooks are missing.",
        ),
        ("has_empty_filter_state", checks["has_empty_filter_state"], "Empty filter state is missing."),
        (
            "has_persistence_error_state",
            checks["has_persistence_error_state"],
            "Persistence error state is missing.",
        ),
        (
            "has_export_confirmation",
            checks["has_export_confirmation"],
            "Export confirmation state is missing.",
        ),
        (
            "has_bulk_review_actions",
            checks["has_bulk_review_actions"],
            "Bulk review actions are missing.",
        ),
        (
            "has_review_progress",
            checks["has_review_progress"],
            "Review progress indicator is missing.",
        ),
        (
            "has_state_import_guard",
            checks["has_state_import_guard"],
            "State import guard is missing.",
        ),
        (
            "has_bulk_confirmation_and_undo",
            checks["has_bulk_confirmation_and_undo"],
            "Bulk and reset actions need explicit confirmation plus local undo.",
        ),
        (
            "has_blocker_approval_invariant",
            checks["has_blocker_approval_invariant"],
            "Rows with offline blockers must not be approved locally.",
        ),
        (
            "has_native_modal_confirmation",
            checks["has_native_modal_confirmation"],
            "Bulk and reset confirmation must use a real modal lifecycle.",
        ),
        (
            "has_empty_detail_state",
            checks["has_empty_detail_state"],
            "A zero-result filter must clear stale inspector content.",
        ),
        (
            "has_mobile_detail_drawer",
            checks["has_mobile_detail_drawer"],
            "Mobile row selection does not expose an immediate decision drawer.",
        ),
        (
            "has_roving_row_keyboard",
            checks["has_roving_row_keyboard"],
            "Review rows lack roving tabindex and arrow-key navigation.",
        ),
        ("has_responsive_css", checks["has_responsive_css"], "Responsive CSS is missing."),
        (
            "has_design_system_contract",
            checks["has_design_system_contract"],
            "Editorial Operations design-system metadata is missing.",
        ),
        (
            "has_ai_assist_trace",
            checks["has_ai_assist_trace"],
            "The bounded AI-to-human decision path is not visible.",
        ),
        ("has_skip_link", checks["has_skip_link"], "Skip-to-queue navigation is missing."),
        (
            "has_active_row_semantics",
            checks["has_active_row_semantics"],
            "Selected review rows do not expose aria-selected state.",
        ),
        (
            "has_mobile_row_cards",
            checks["has_mobile_row_cards"],
            "Mobile rows do not expose structured field labels.",
        ),
        (
            "has_reduced_motion_support",
            checks["has_reduced_motion_support"],
            "Reduced-motion styling is missing.",
        ),
        (
            "queue_precedes_secondary_context",
            checks["queue_precedes_secondary_context"],
            "Review queue must precede secondary context in DOM order.",
        ),
        (
            "no_generic_visual_effects",
            checks["no_generic_visual_effects"],
            "Workspace contains prohibited generic gradient, glass, or card-shadow effects.",
        ),
        (
            "no_external_network_calls",
            checks["no_external_network_calls"],
            "Workspace contains external network-call tokens.",
        ),
    ]


class _WorkspaceHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.start_tags: list[tuple[str, dict[str, str]]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.start_tags.append((tag, {key: value or "" for key, value in attrs}))

    def has_attr(self, attr: str) -> bool:
        return any(attr in attrs for _tag, attrs in self.start_tags)

    def tag_count(self, tag: str) -> int:
        return sum(1 for item, _attrs in self.start_tags if item == tag)
