from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from meta_importer.asset_validation import validate_asset_metadata
from meta_importer.browser_qa import audit_workspace_browser_contract
from meta_importer.cli import main
from meta_importer.html_quality import audit_workspace_html
from meta_importer.launch_workspace import (
    ManifestSchemaError,
    SyntheticDataError,
    build_launch_plan,
    export_plan_dict,
    read_manifest,
    render_html_workspace,
    render_markdown_review,
)
from meta_importer.local_store import write_batch_store
from meta_importer.platform_payload_preview import build_platform_payload_preview
from meta_importer.sqlite_store import SQLiteStoreError, SQLiteWorkspaceStore
from meta_importer.workspace_state import export_workspace_state_dict

FIXTURE = Path("fixtures/fake_agency_creatives/manifest.csv")
V2_FIXTURE = Path("fixtures/fake_agency_creatives/manifest_v2.csv")
ASSET_METADATA = Path("fixtures/fake_agency_creatives/asset_metadata.csv")
EDGE_FIXTURE = Path("fixtures/fake_agency_creatives/manifest_edge_cases.csv")
EDGE_GOLDEN = Path("fixtures/fake_agency_creatives/golden_edge_summary.json")


class LaunchWorkspaceTests(unittest.TestCase):
    def test_fixture_builds_role_owned_dry_run_plan(self) -> None:
        rows = read_manifest(FIXTURE)
        plan = build_launch_plan(rows, source_manifest=str(FIXTURE))
        payload = export_plan_dict(plan)

        self.assertEqual(plan.summary["row_count"], 100)
        self.assertEqual(plan.summary["campaign_count"], 3)
        self.assertEqual(plan.summary["adset_count"], 10)
        self.assertEqual(len(payload["ads"]), 100)
        self.assertEqual(payload["mode"], "offline_dry_run_only")
        self.assertEqual(payload["contract_version"], "offline_launch_plan.v2")
        self.assertFalse(payload["mutation_allowed"])
        self.assertEqual(payload["meta_api_compatibility"], "not_claimed")
        self.assertEqual(plan.summary["batch_states"]["launch_ready"], 30)
        self.assertEqual(plan.summary["batch_states"]["needs_review"], 10)
        self.assertEqual(plan.summary["batch_states"]["blocked"], 60)
        self.assertEqual(plan.summary["issue_codes"]["missing_approval"], 30)
        self.assertEqual(plan.summary["issue_codes"]["destination_mismatch"], 10)
        self.assertEqual(plan.summary["issue_codes"]["duplicate_asset"], 10)
        self.assertEqual(plan.summary["issue_codes"]["naming_error"], 10)
        self.assertEqual(plan.summary["issue_codes"]["unsupported_format"], 10)
        self.assertIn("Approver", plan.summary["owner_queue"])
        self.assertIn("Creative Ops Manager", plan.summary["owner_queue"])
        self.assertIn("Media Buyer", plan.summary["owner_queue"])
        self.assertTrue(all(ad["operation"] == "dry_run_create_ad_candidate" for ad in payload["ads"]))
        self.assertTrue(all(ad["operation_contract"]["mutation_allowed"] is False for ad in payload["ads"]))

    def test_markdown_review_names_guardrails_and_fix_queue(self) -> None:
        rows = read_manifest(FIXTURE)
        plan = build_launch_plan(rows, source_manifest=str(FIXTURE))
        review = render_markdown_review(plan)

        self.assertIn("Offline dry run only", review)
        self.assertIn("## Owner Queue", review)
        self.assertIn("## First 20 Fixes", review)
        self.assertIn("Live publish", review)

    def test_html_workspace_has_first_screen_controls(self) -> None:
        rows = read_manifest(FIXTURE)
        plan = build_launch_plan(rows, source_manifest=str(FIXTURE))
        html = render_html_workspace(plan)

        self.assertIn("Creative Launch Workspace for Meta Ads", html)
        self.assertIn("Dry run only", html)
        self.assertIn('data-filter="launch_ready"', html)
        self.assertIn('data-filter="blocked"', html)
        self.assertIn("No Meta API calls", html)
        self.assertIn("UTM Status", html)
        self.assertIn("Post ID", html)
        self.assertIn("Decision workspace", html)
        self.assertIn("Creative preview", html)
        self.assertIn("Local state and export", html)
        self.assertIn("Confirm visible for dry-run export", html)
        self.assertIn("Return visible for fix", html)
        self.assertIn("Block visible from dry-run export", html)
        self.assertIn("Import state", html)
        self.assertIn("Imported state failed the local-only guardrail.", html)
        self.assertIn("localStorage", html)
        self.assertIn("rows: persisted.rows", html)
        self.assertIn("workspace_review_state.v1", html)
        self.assertIn('id="guided-dialog"', html)
        self.assertIn("1 of 3 · Find", html)
        self.assertIn("2 of 3 · Decide", html)
        self.assertIn("3 of 3 · Verify", html)
        self.assertIn("No external system was changed.", html)
        self.assertIn("mutation_allowed:false", html)
        self.assertNotIn('id="guided-result-write"', html)
        self.assertNotIn('class="guided-boundary"', html)
        self.assertIn("findGuidedRow", html)
        self.assertIn('searchParams.delete("guided")', html)
        self.assertIn('document.getElementById("review-workspace").focus()', html)
        self.assertIn('class="brand" href="index.html"', html)
        self.assertIn('id="guided-return" href="index.html"', html)
        self.assertIn("Return to the case study", html)

    def test_html_static_audit_checks_accessibility_and_network_boundary(self) -> None:
        rows = read_manifest(V2_FIXTURE)
        plan = build_launch_plan(rows, source_manifest=str(V2_FIXTURE))
        audit = audit_workspace_html(render_html_workspace(plan))

        self.assertEqual(audit["contract_version"], "workspace_html_static_audit.v1")
        self.assertEqual(audit["status"], "pass")
        self.assertEqual(audit["passed_count"], audit["check_count"])
        self.assertGreaterEqual(audit["check_count"], 15)
        self.assertEqual(audit["issues"], [])
        self.assertEqual(audit["browser_runtime"], "not_available_in_static_audit")

    def test_html_workspace_uses_editorial_operations_design_contract(self) -> None:
        rows = read_manifest(V2_FIXTURE)
        plan = build_launch_plan(rows, source_manifest=str(V2_FIXTURE))
        html = render_html_workspace(plan)

        self.assertIn('content="Editorial Operations v2"', html)
        self.assertIn('class="focus-panel"', html)
        self.assertIn("creatives need a human decision", html)
        self.assertIn('let activeFilter = "needs_review"', html)
        self.assertIn("AI intake proof", html)
        self.assertIn("No model runs in this browser", html)
        self.assertIn('class="batch-disclosure"', html)
        self.assertIn('class="secondary-actions"', html)
        self.assertIn('class="detail-disclosure"', html)
        self.assertIn("What needs attention", html)
        self.assertIn("Confirm reuse for dry-run export", html)
        self.assertIn('"Confirm " + targetLabel + " for dry-run export? "', html)
        self.assertIn("Passes offline checks", html)
        self.assertIn("Human decision required", html)
        self.assertIn("Confirmed for dry-run export", html)
        self.assertIn("Blocked from dry-run export", html)
        self.assertIn("reviewerRole.value = row.owners[0]", html)
        self.assertIn('thumb.className = "creative-thumb format-"', html)
        self.assertIn('content: attr(data-label)', html)
        self.assertIn('@media (prefers-reduced-motion: reduce)', html)
        self.assertIn('setAttribute("aria-selected"', html)
        self.assertIn("ArrowDown", html)
        self.assertIn("detail-shell.open", html)
        self.assertIn("confirmPendingAction", html)
        self.assertIn("Undo last change", html)
        self.assertIn("Imported state failed structural validation.", html)
        self.assertIn('patch.review_status === "confirmed_ready"', html)
        self.assertIn('row.batch_state !== "blocked"', html)
        self.assertIn("Resolve offline blockers before dry-run export confirmation.", html)
        self.assertIn("<dialog", html)
        self.assertIn("showModal()", html)
        self.assertIn("detailShell.inert = true", html)
        self.assertIn("startGuidedDemo", html)
        self.assertIn("makeGuidedDecision", html)
        self.assertIn("completeGuidedDemo", html)
        self.assertIn("mutation_allowed:false", html)
        self.assertIn(".guided-dialog [hidden] { display: none !important; }", html)
        self.assertIn("clearDetail", html)
        self.assertIn("<span>Approval missing</span>", html)
        self.assertLess(html.index('class="focus-panel"'), html.index('class="table-shell"'))
        self.assertNotIn("linear-gradient", html)
        self.assertNotIn("radial-gradient", html)
        self.assertNotIn("box-shadow:", html)

    def test_workspace_copy_matches_operator_supplied_classification(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            manifest = Path(temp_dir) / "operator.csv"
            manifest.write_text(
                "creative_id,campaign_key,adset_key,format,asset_path,primary_text,headline,destination_url,approval_status,qa_issue\n"
                "cr_operator,camp,adset,image,/tmp/operator.jpg,Copy,Headline,https://customer.example/page,approved,\n"
            )
            plan = build_launch_plan(
                read_manifest(manifest, synthetic_only=False),
                source_manifest=str(manifest),
            )

        html = render_html_workspace(plan)
        state = export_workspace_state_dict(plan)

        self.assertIn("Operator supplied", html)
        self.assertIn("Operator-supplied rows stay local", html)
        self.assertNotIn("No customer assets</li>", html)
        self.assertEqual(state["data_classification"], "operator_supplied_manifest_no_live_mutation")
        self.assertTrue(any("Operator-supplied rows remain local" in item for item in state["guardrails"]))

    def test_task_focus_does_not_invent_nonzero_review_states(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            manifest = Path(temp_dir) / "synthetic.csv"
            manifest.write_text(
                "creative_id,campaign_key,adset_key,format,asset_path,primary_text,headline,destination_url,approval_status,qa_issue\n"
                "cr_one,camp,adset,image,fixtures/fake_agency_creatives/assets/one.jpg,Copy,Headline,https://example.invalid/page,approved,\n"
            )
            plan = build_launch_plan(read_manifest(manifest), source_manifest=str(manifest))

        html = render_html_workspace(plan)

        self.assertIn("0 creatives need a human decision", html)
        self.assertIn("<strong>1</strong> pass offline checks", html)
        self.assertIn("<strong>0</strong> need your decision", html)
        self.assertIn("<strong>0</strong> routed for fixes", html)

    def test_workspace_browser_contract_audits_reusable_ui_behaviors(self) -> None:
        rows = read_manifest(V2_FIXTURE)
        plan = build_launch_plan(rows, source_manifest=str(V2_FIXTURE))
        report = audit_workspace_browser_contract(render_html_workspace(plan))

        self.assertEqual(report["contract_version"], "workspace_browser_qa.v1")
        self.assertEqual(report["status"], "pass")
        self.assertEqual(report["passed_count"], report["check_count"])
        self.assertEqual(report["filter_counts"]["all"], 100)
        self.assertEqual(report["filter_counts"]["blocked"], 60)
        self.assertFalse(report["mutation_allowed"])
        self.assertEqual(report["meta_api_compatibility"], "not_claimed")
        self.assertTrue(report["checks"]["bulk_actions_preserve_visible_scope"])
        self.assertTrue(report["checks"]["state_import_has_batch_and_guardrail_checks"])

    def test_edge_fixture_matches_golden_summary(self) -> None:
        rows = read_manifest(EDGE_FIXTURE)
        plan = build_launch_plan(rows, source_manifest=str(EDGE_FIXTURE))
        actual = {
            "contract_version": "edge_fixture_summary.v1",
            "row_count": plan.summary["row_count"],
            "batch_states": plan.summary["batch_states"],
            "issue_severity": plan.summary["issue_severity"],
            "issue_codes": plan.summary["issue_codes"],
            "owner_queue": plan.summary["owner_queue"],
            "mutation_allowed": False,
            "meta_api_compatibility": "not_claimed",
        }

        self.assertEqual(actual, json.loads(EDGE_GOLDEN.read_text()))

    def test_workspace_state_exports_role_owned_review_state(self) -> None:
        rows = read_manifest(V2_FIXTURE)
        plan = build_launch_plan(rows, source_manifest=str(V2_FIXTURE))
        state = export_workspace_state_dict(plan)
        statuses = {row["review_status"] for row in state["review_statuses"]}

        self.assertEqual(state["mode"], "local_review_state_only")
        self.assertEqual(state["contract_version"], "workspace_review_state.v1")
        self.assertEqual(state["data_classification"], "synthetic_fixture_only")
        self.assertFalse(state["mutation_allowed"])
        self.assertEqual(state["meta_api_compatibility"], "not_claimed")
        self.assertEqual(len(state["review_statuses"]), 100)
        self.assertIn("ready_to_review", statuses)
        self.assertIn("needs_confirmation", statuses)
        self.assertIn("needs_fix", statuses)
        self.assertIn("local_storage_key", state)
        self.assertEqual([event["event_type"] for event in state["audit_events"]], ["batch_created", "review_queue_seeded"])
        self.assertTrue(all("idempotency_key" in row for row in state["review_statuses"]))

    def test_asset_metadata_validation_reports_fixture_asset_readiness(self) -> None:
        rows = read_manifest(V2_FIXTURE)
        plan = build_launch_plan(rows, source_manifest=str(V2_FIXTURE))
        report = validate_asset_metadata(plan, ASSET_METADATA)

        self.assertEqual(report["contract_version"], "synthetic_asset_validation.v1")
        self.assertEqual(report["rows_checked"], 100)
        self.assertGreaterEqual(report["unique_assets"], 90)
        self.assertEqual(report["status"], "blocked")
        self.assertEqual(report["summary"]["unsupported_format_rows"], 10)
        self.assertEqual(
            {issue["code"] for issue in report["issues"]},
            {"unsupported_asset_format"},
        )

    def test_asset_metadata_validation_blocks_missing_metadata(self) -> None:
        rows = read_manifest(V2_FIXTURE)
        plan = build_launch_plan(rows, source_manifest=str(V2_FIXTURE))
        with tempfile.TemporaryDirectory() as temp_dir:
            metadata = Path(temp_dir) / "asset_metadata.csv"
            metadata.write_text("asset_path,asset_hash,declared_format,media_kind,width_px,height_px,duration_seconds,file_size_bytes,checksum_sha256,metadata_source\n")
            report = validate_asset_metadata(plan, metadata)

        self.assertEqual(report["status"], "blocked")
        self.assertEqual(report["blocker_count"], 100)
        self.assertIn("missing_asset_metadata", {issue["code"] for issue in report["issues"]})

    def test_local_batch_store_persists_snapshots_and_appends_audit(self) -> None:
        rows = read_manifest(V2_FIXTURE)
        plan = build_launch_plan(rows, source_manifest=str(V2_FIXTURE))
        with tempfile.TemporaryDirectory() as temp_dir:
            first = write_batch_store(plan, temp_dir, asset_metadata_path=ASSET_METADATA)
            second = write_batch_store(plan, temp_dir, asset_metadata_path=ASSET_METADATA)
            batch_dir = Path(first["root"])
            source_snapshot_exists = (batch_dir / "snapshots/source_manifest.csv").exists()
            launch_plan_exists = (batch_dir / "launch_plan.json").exists()
            review_state_exists = (batch_dir / "review_state.json").exists()
            audit_lines = (batch_dir / "audit/events.jsonl").read_text().splitlines()
            asset_report = json.loads((batch_dir / "asset_validation.json").read_text())

        self.assertEqual(first["contract_version"], "local_batch_store.v1")
        self.assertEqual(first["batch_id"], second["batch_id"])
        self.assertTrue(source_snapshot_exists)
        self.assertTrue(launch_plan_exists)
        self.assertTrue(review_state_exists)
        self.assertEqual(len(audit_lines), 10)
        self.assertEqual(json.loads(audit_lines[-1])["sequence"], 10)
        self.assertEqual(asset_report["status"], "blocked")

    def test_sqlite_store_persists_tenant_batch_rows_and_audit(self) -> None:
        rows = read_manifest(V2_FIXTURE)
        plan = build_launch_plan(rows, source_manifest=str(V2_FIXTURE))
        with tempfile.TemporaryDirectory() as temp_dir:
            db = Path(temp_dir) / "workspace.sqlite3"
            store = SQLiteWorkspaceStore(db)
            try:
                manifest = store.upsert_batch(plan, tenant_id="tenant_fixture_agency")
                store.record_row_decision(
                    manifest["batch_id"],
                    2,
                    review_status="confirmed_ready",
                    decision="approved_for_dry_run_export",
                    actor_role="Approver",
                    note="fixture approval",
                )
                exported = store.export_batch_state(manifest["batch_id"])
            finally:
                store.close()

        self.assertEqual(manifest["contract_version"], "sqlite_workspace_store.v1")
        self.assertEqual(exported["mode"], "local_sqlite_store_only")
        self.assertEqual(exported["tenant_id"], "tenant_fixture_agency")
        self.assertEqual(len(exported["review_statuses"]), 100)
        self.assertEqual(exported["review_statuses"][0]["review_status"], "confirmed_ready")
        self.assertFalse(exported["mutation_allowed"])
        self.assertEqual(exported["meta_api_compatibility"], "not_claimed")
        self.assertEqual(
            [event["event_type"] for event in exported["audit_events"]],
            ["sqlite_batch_upserted", "sqlite_row_decision_updated"],
        )

    def test_sqlite_store_rejects_non_fixture_tenant_ids(self) -> None:
        rows = read_manifest(V2_FIXTURE)
        plan = build_launch_plan(rows, source_manifest=str(V2_FIXTURE))
        with tempfile.TemporaryDirectory() as temp_dir:
            store = SQLiteWorkspaceStore(Path(temp_dir) / "workspace.sqlite3")
            try:
                with self.assertRaises(SQLiteStoreError):
                    store.upsert_batch(plan, tenant_id="real_agency")
            finally:
                store.close()

    def test_sqlite_store_rejects_invalid_roles_and_blocked_approvals(self) -> None:
        rows = read_manifest(V2_FIXTURE)
        plan = build_launch_plan(rows, source_manifest=str(V2_FIXTURE))
        with tempfile.TemporaryDirectory() as temp_dir:
            store = SQLiteWorkspaceStore(Path(temp_dir) / "workspace.sqlite3")
            try:
                manifest = store.upsert_batch(plan)
                with self.assertRaisesRegex(SQLiteStoreError, "unknown reviewer role"):
                    store.record_row_decision(
                        manifest["batch_id"],
                        2,
                        review_status="confirmed_ready",
                        decision="approved_for_dry_run_export",
                        actor_role="Arbitrary Role",
                    )
                with self.assertRaisesRegex(SQLiteStoreError, "blocked rows cannot"):
                    store.record_row_decision(
                        manifest["batch_id"],
                        4,
                        review_status="confirmed_ready",
                        decision="approved_for_dry_run_export",
                        actor_role="Approver",
                    )
            finally:
                store.close()

    def test_v2_fixture_exports_mapping_ledger(self) -> None:
        rows = read_manifest(V2_FIXTURE)
        plan = build_launch_plan(rows, source_manifest=str(V2_FIXTURE))
        payload = export_plan_dict(plan)
        first_ad = payload["ads"][0]

        self.assertEqual(plan.summary["row_count"], 100)
        self.assertEqual(plan.summary["launch_contract"]["account_alias_rows"], 100)
        self.assertEqual(plan.summary["launch_contract"]["placement_rows"], 100)
        self.assertEqual(plan.summary["launch_contract"]["utm_rows"], 100)
        self.assertEqual(plan.summary["launch_contract"]["post_decision_rows"], 100)
        self.assertEqual(plan.summary["launch_contract"]["source_lineage_rows"], 100)
        self.assertEqual(plan.summary["batch_states"]["launch_ready"], 30)
        self.assertIn("account_mapping", first_ad)
        self.assertIn("placement_mapping", first_ad)
        self.assertIn("post_lineage", first_ad)
        self.assertIn("source_lineage", first_ad)
        self.assertIn("approval_record", first_ad)
        self.assertIn("preflight", first_ad)
        self.assertIn("utm_source=facebook", first_ad["tracking"]["final_url_preview"])

    def test_default_manifest_reader_blocks_non_synthetic_data(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            manifest = Path(temp_dir) / "manifest.csv"
            manifest.write_text(
                "creative_id,campaign_key,adset_key,format,asset_path,primary_text,headline,destination_url,approval_status,qa_issue\n"
                "cr_real,camp,adset,image,/Users/example/customer.jpg,Copy,Head,https://customer.example/page,approved,\n"
            )
            with self.assertRaises(SyntheticDataError):
                read_manifest(manifest)

    def test_manifest_schema_guard_blocks_missing_required_columns(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            manifest = Path(temp_dir) / "manifest.csv"
            manifest.write_text(
                "creative_id,campaign_key,adset_key,format,asset_path,primary_text,destination_url,approval_status,qa_issue\n"
                "cr_001,camp,adset,image,fixtures/fake_agency_creatives/assets/a.jpg,Copy,https://example.invalid/page,approved,\n"
            )
            with self.assertRaisesRegex(ManifestSchemaError, "missing required column"):
                read_manifest(manifest)

    def test_manifest_schema_guard_blocks_unknown_columns(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            manifest = Path(temp_dir) / "manifest.csv"
            manifest.write_text(
                "creative_id,campaign_key,adset_key,format,asset_path,primary_text,headline,destination_url,approval_status,qa_issue,surprise_column\n"
                "cr_001,camp,adset,image,fixtures/fake_agency_creatives/assets/a.jpg,Copy,Head,https://example.invalid/page,approved,,extra\n"
            )
            with self.assertRaisesRegex(ManifestSchemaError, "unknown column"):
                read_manifest(manifest)

    def test_synthetic_guard_blocks_live_looking_aliases(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            manifest = Path(temp_dir) / "manifest.csv"
            manifest.write_text(
                "creative_id,campaign_key,adset_key,format,asset_path,primary_text,headline,destination_url,approval_status,qa_issue,account_id_alias,post_id\n"
                "cr_001,camp,adset,image,fixtures/fake_agency_creatives/assets/a.jpg,Copy,Head,https://example.invalid/page,approved,,act_123,123456\n"
            )
            with self.assertRaises(SyntheticDataError):
                read_manifest(manifest)

    def test_v2_mapping_validators_route_risks(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            manifest = Path(temp_dir) / "manifest.csv"
            manifest.write_text(
                "creative_id,campaign_key,adset_key,format,asset_path,primary_text,headline,destination_url,approval_status,qa_issue,account_id_alias,objective,placement,utm_source,utm_medium,utm_campaign,utm_content,post_id_type,source_system,source_row_id\n"
                "cr_bad,camp_launch,adset,story,fixtures/fake_agency_creatives/assets/a.jpg,Copy,Head,https://example.invalid/page,approved,,acct_fixture_us,traffic,feed,facebook,,wrong_campaign,wrong_content,existing,synthetic_sheet,\n"
            )
            rows = read_manifest(manifest)
            plan = build_launch_plan(rows, source_manifest=str(manifest))
            codes = {issue.code for issue in plan.issues}

        self.assertIn("format_placement_mismatch", codes)
        self.assertIn("utm_campaign_mismatch", codes)
        self.assertIn("partial_utm_mapping", codes)
        self.assertIn("utm_content_lineage_missing", codes)
        self.assertIn("existing_post_id_missing", codes)
        self.assertIn("incomplete_source_lineage", codes)

    def test_idempotency_is_stable_across_row_order(self) -> None:
        header = (
            "creative_id,campaign_key,adset_key,format,asset_path,primary_text,headline,destination_url,approval_status,qa_issue,account_id_alias,placement\n"
        )
        row_a = "cr_a,camp,adset,image,fixtures/fake_agency_creatives/assets/a.jpg,Copy A,Head A,https://example.invalid/a,approved,,acct_fixture_us,feed\n"
        row_b = "cr_b,camp,adset,image,fixtures/fake_agency_creatives/assets/b.jpg,Copy B,Head B,https://example.invalid/b,approved,,acct_fixture_us,feed\n"
        with tempfile.TemporaryDirectory() as temp_dir:
            first = Path(temp_dir) / "first.csv"
            second = Path(temp_dir) / "second.csv"
            first.write_text(header + row_a + row_b)
            second.write_text(header + row_b + row_a)
            plan_first = build_launch_plan(read_manifest(first), source_manifest=str(first))
            plan_second = build_launch_plan(read_manifest(second), source_manifest=str(second))

        keys_first = {candidate.creative_id: candidate.idempotency_key for candidate in plan_first.candidates}
        keys_second = {candidate.creative_id: candidate.idempotency_key for candidate in plan_second.candidates}
        self.assertEqual(keys_first, keys_second)

    def test_idempotency_collision_blocks_without_reuse_intent(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            manifest = Path(temp_dir) / "manifest.csv"
            manifest.write_text(
                "creative_id,campaign_key,adset_key,format,asset_path,primary_text,headline,destination_url,approval_status,qa_issue,account_id_alias,placement\n"
                "cr_same,camp,adset,image,fixtures/fake_agency_creatives/assets/a.jpg,Copy,Head,https://example.invalid/a,approved,,acct_fixture_us,feed\n"
                "cr_same,camp,adset,image,fixtures/fake_agency_creatives/assets/a.jpg,Copy,Head,https://example.invalid/a,approved,,acct_fixture_us,feed\n"
            )
            plan = build_launch_plan(read_manifest(manifest), source_manifest=str(manifest))

        self.assertIn("idempotency_collision", {issue.code for issue in plan.issues})

    def test_plan_payload_is_json_serializable(self) -> None:
        rows = read_manifest(FIXTURE)
        plan = build_launch_plan(rows, source_manifest=str(FIXTURE))
        encoded = json.dumps(export_plan_dict(plan), sort_keys=True)

        self.assertIn("offline_dry_run_only", encoded)
        self.assertIn("offline_launch_plan.v2", encoded)
        self.assertIn("not_claimed", encoded)

    def test_platform_payload_preview_is_non_executable_contract_map(self) -> None:
        rows = read_manifest(V2_FIXTURE)
        plan = build_launch_plan(rows, source_manifest=str(V2_FIXTURE))
        preview = build_platform_payload_preview(plan)
        first = preview["payloads"][0]

        self.assertEqual(preview["contract_version"], "meta_platform_payload_preview.v1")
        self.assertEqual(preview["meta_api_compatibility"], "mapped_not_executed")
        self.assertFalse(preview["mutation_allowed"])
        self.assertEqual(
            preview["asset_storage_policy"]["strategy"],
            "meta_native_zero_retention_candidate",
        )
        self.assertEqual(
            preview["asset_storage_policy"]["durable_local_storage"],
            "metadata_lineage_only",
        )
        self.assertEqual(preview["summary"]["row_count"], 100)
        self.assertTrue(preview["summary"]["all_payloads_blocked"])
        self.assertEqual(first["payload_readiness"], "draft_blocked")
        self.assertEqual(first["execution_options"], ["validate_only"])
        self.assertIn("/act_<AD_ACCOUNT_ID>/campaigns", json.dumps(first))
        self.assertIn("/<BUSINESS_ID>/images", json.dumps(preview))
        self.assertIn("creative_folder_id", json.dumps(preview))
        self.assertNotIn("act_122", json.dumps(preview))
        self.assertIn(
            "account_id_alias",
            {blocked["field"] for blocked in first["blocked_fields"]},
        )
        self.assertIn(
            "creative_folder_id",
            {blocked["field"] for blocked in first["blocked_fields"]},
        )
        self.assertEqual(
            first["platform_field_status"]["asset_storage"],
            "planned_meta_native_zero_retention",
        )
        self.assertEqual(
            first["platform_sequence"][0]["payload"]["objective"],
            "OUTCOME_TRAFFIC",
        )

    def test_cli_writes_workspace_state_json(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            base = Path(temp_dir)
            exit_code = main(
                [
                    "plan",
                    str(V2_FIXTURE),
                    "--out",
                    str(base / "launch_plan.json"),
                    "--review",
                    str(base / "review_packet.md"),
                    "--html",
                    str(base / "workspace.html"),
                    "--html-audit",
                    str(base / "workspace_audit.json"),
                    "--state",
                    str(base / "review_state.json"),
                    "--platform-preview",
                    str(base / "platform_preview.json"),
                ]
            )
            state = json.loads((base / "review_state.json").read_text())
            audit = json.loads((base / "workspace_audit.json").read_text())
            platform_preview = json.loads((base / "platform_preview.json").read_text())
            browser_qa = audit_workspace_browser_contract((base / "workspace.html").read_text())

        self.assertEqual(exit_code, 0)
        self.assertEqual(state["mode"], "local_review_state_only")
        self.assertEqual(len(state["review_statuses"]), 100)
        self.assertFalse(state["mutation_allowed"])
        self.assertEqual(audit["status"], "pass")
        self.assertEqual(browser_qa["status"], "pass")
        self.assertEqual(platform_preview["contract_version"], "meta_platform_payload_preview.v1")

    def test_cli_writes_local_batch_store(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            base = Path(temp_dir)
            exit_code = main(
                [
                    "plan",
                    str(V2_FIXTURE),
                    "--out",
                    str(base / "launch_plan.json"),
                    "--review",
                    str(base / "review_packet.md"),
                    "--html",
                    str(base / "workspace.html"),
                    "--html-audit",
                    str(base / "workspace_audit.json"),
                    "--state",
                    str(base / "review_state.json"),
                    "--store-dir",
                    str(base / "store"),
                    "--sqlite-db",
                    str(base / "workspace.sqlite3"),
                    "--asset-metadata",
                    str(ASSET_METADATA),
                ]
            )
            store_dirs = list((base / "store").iterdir())
            store_manifest = json.loads((store_dirs[0] / "batch_store.json").read_text())
            sqlite_exists = (base / "workspace.sqlite3").exists()

        self.assertEqual(exit_code, 0)
        self.assertEqual(store_manifest["contract_version"], "local_batch_store.v1")
        self.assertEqual(store_manifest["asset_validation_status"], "blocked")
        self.assertFalse(store_manifest["mutation_allowed"])
        self.assertTrue(sqlite_exists)


if __name__ == "__main__":
    unittest.main()
