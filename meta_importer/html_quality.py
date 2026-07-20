from __future__ import annotations

from html.parser import HTMLParser


def audit_workspace_html(html: str) -> dict[str, object]:
    parser = _WorkspaceHTMLParser()
    parser.feed(html)

    filter_buttons = [
        attrs for tag, attrs in parser.start_tags if tag == "button" and attrs.get("data-filter")
    ]
    labelled_divs = [
        attrs for tag, attrs in parser.start_tags if tag == "div" and attrs.get("aria-label")
    ]
    checks = {
        "has_title": "Launch Control" in html,
        "has_row_detail": "Decision workspace" in html,
        "has_preview": "Creative preview" in html,
        "has_export_panel": "Local state and export" in html,
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
                "Resolve offline blockers before dry-run export confirmation.",
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
        "has_design_system_contract": 'content="Launch Control Product UI v4"' in html,
        "has_ai_assist_trace": all(
            token in html
            for token in (
                "AI intake proof",
                "policy checks",
                "human decisions",
                "No model runs in this browser",
            )
        ),
        "has_task_first_focus": all(
            token in html
            for token in (
                'class="focus-panel"',
                "creatives need a human decision",
                'data-quick-filter="needs_review"',
                'let activeFilter = "needs_review"',
            )
        ),
        "has_progressive_disclosure": all(
            token in html
            for token in (
                'class="batch-disclosure"',
                'class="secondary-actions"',
                'class="detail-disclosure"',
            )
        ),
        "has_guided_demo": all(
            token in html
            for token in (
                'id="guided-dialog"',
                "findGuidedRow",
                "startGuidedDemo",
                "makeGuidedDecision",
                "completeGuidedDemo",
            )
        ),
        "has_guided_progress": all(
            token in html for token in ("1 of 3 · Detect", "2 of 3 · Decide", "3 of 3 · Prove")
        ),
        "has_guided_local_evidence": all(
            token in html
            for token in (
                "No external system was changed.",
                "mutation_allowed:false",
                "persisted.audit.unshift(event)",
            )
        ),
        "has_guided_full_queue_exit": all(
            token in html
            for token in ('id="guided-explore"', 'searchParams.delete("guided")', 'setActiveFilter("all")')
        ),
        "has_mobile_guided_action_order": all(
            token in html
            for token in (
                ".guided-dialog[open]",
                "position: sticky;",
                "overflow-y: auto;",
                ".guided-title:focus",
                "border-left: 4px solid var(--focus);",
            )
        )
        and html.find('id="guided-step-two"') < html.find('id="guided-case"')
        and html.find('id="guided-step-three-actions"') < html.find('class="guided-proof"'),
        "has_guided_architecture_exit": (
            'id="guided-product-builder" href="https://github.com/mattyu-dev/creative-launch-workspace/blob/main/docs/architecture/system.md"'
            in html
        ),
        "brand_accessible_name_matches_visible_text": (
            '<a class="brand" href="index.html">' in html
            and '<a class="brand" href="index.html" aria-label=' not in html
        ),
        "labelled_generic_divs_have_roles": bool(labelled_divs)
        and all(attrs.get("role") in {"group", "img"} for attrs in labelled_divs),
        "has_encoded_data_favicon": (
            'href="data:image/svg+xml,%3Csvg%20xmlns%3D%22' in html
            and "data:image/svg+xml,%3Csvg xmlns='" not in html
            and "%2324142b" not in html
        ),
        "has_skip_link": 'class="skip-link"' in html and 'href="#review-workspace"' in html,
        "has_active_row_semantics": 'setAttribute("aria-selected"' in html,
        "has_mobile_row_cards": 'td.dataset.label' in html and 'content: attr(data-label)' in html,
        "has_reduced_motion_support": "@media (prefers-reduced-motion: reduce)" in html,
        "focus_precedes_review_queue": html.find('class="focus-panel"')
        < html.find('class="table-shell"'),
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
            "Rows with offline blockers must not be confirmed for dry-run export.",
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
            "Creative Launch product design-system metadata is missing.",
        ),
        (
            "has_ai_assist_trace",
            checks["has_ai_assist_trace"],
            "The bounded AI-to-human decision path is not visible.",
        ),
        (
            "has_task_first_focus",
            checks["has_task_first_focus"],
            "The first screen does not make the operator's next action explicit.",
        ),
        (
            "has_progressive_disclosure",
            checks["has_progressive_disclosure"],
            "Secondary batch, bulk, and technical controls must use progressive disclosure.",
        ),
        (
            "has_guided_demo",
            checks["has_guided_demo"],
            "The three-step guided review path is missing or bypasses the local decision path.",
        ),
        (
            "has_guided_progress",
            checks["has_guided_progress"],
            "Guided review lacks visible three-step progress.",
        ),
        (
            "has_guided_local_evidence",
            checks["has_guided_local_evidence"],
            "Guided review does not expose local audit evidence and the mutation boundary.",
        ),
        (
            "has_guided_full_queue_exit",
            checks["has_guided_full_queue_exit"],
            "Guided review lacks a deterministic exit to the full queue.",
        ),
        (
            "has_mobile_guided_action_order",
            checks["has_mobile_guided_action_order"],
            "Guided decisions and completion actions must precede scrollable evidence on small screens.",
        ),
        (
            "has_guided_architecture_exit",
            checks["has_guided_architecture_exit"],
            "Guided completion lacks explicit routes to the product architecture and contact profile.",
        ),
        (
            "brand_accessible_name_matches_visible_text",
            checks["brand_accessible_name_matches_visible_text"],
            "The brand link accessible name must match its visible label.",
        ),
        (
            "labelled_generic_divs_have_roles",
            checks["labelled_generic_divs_have_roles"],
            "Generic labelled containers must expose a valid ARIA role.",
        ),
        (
            "has_encoded_data_favicon",
            checks["has_encoded_data_favicon"],
            "The inline favicon URL must be fully percent encoded.",
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
            "focus_precedes_review_queue",
            checks["focus_precedes_review_queue"],
            "The operator task focus must precede the review queue in DOM order.",
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
