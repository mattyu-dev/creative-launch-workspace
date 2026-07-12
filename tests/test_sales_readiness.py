from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from meta_importer.cli import main
from meta_importer.sales_readiness import (
    CONTRACT_VERSION,
    build_start_selling_readiness,
    render_start_selling_markdown,
)


class SalesReadinessTests(unittest.TestCase):
    def test_start_selling_report_keeps_live_platform_blocked(self) -> None:
        report = build_start_selling_readiness()

        self.assertEqual(report["contract_version"], CONTRACT_VERSION)
        self.assertEqual(report["current_allowed_tier"], "G0 synthetic/offline only")
        self.assertEqual(report["can_sell_now"], "paid discovery or synthetic rehearsal only")
        self.assertIn("live publishing", report["cannot_sell_yet"])
        self.assertIn("production multi-tenant SaaS", report["cannot_sell_yet"])

    def test_report_tracks_all_selling_readiness_lanes(self) -> None:
        report = build_start_selling_readiness()
        track_ids = {track["id"] for track in report["tracks"]}

        self.assertEqual(
            track_ids,
            {
                "positioning_and_icp",
                "demo_product",
                "pilot_offer",
                "trust_legal_privacy",
                "meta_platform_access",
                "production_engineering",
                "qa_accessibility",
                "onboarding_support_ops",
            },
        )
        self.assertTrue(all(track["blocked_by"] for track in report["tracks"]))

    def test_markdown_render_names_allowed_selling_motion(self) -> None:
        report = build_start_selling_readiness()
        markdown = render_start_selling_markdown(report)

        self.assertIn("# Start Selling Readiness Report", markdown)
        self.assertIn("paid discovery or synthetic rehearsal only", markdown)
        self.assertIn("## Blocked Capabilities", markdown)

    def test_cli_writes_sales_readiness_reports(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            base = Path(temp_dir)
            exit_code = main(
                [
                    "sales-readiness",
                    "--out",
                    str(base / "sales_readiness.json"),
                    "--markdown",
                    str(base / "sales_readiness.md"),
                ]
            )
            payload = json.loads((base / "sales_readiness.json").read_text())
            markdown = (base / "sales_readiness.md").read_text()

        self.assertEqual(exit_code, 0)
        self.assertEqual(payload["contract_version"], CONTRACT_VERSION)
        self.assertIn("Start Selling Readiness Report", markdown)


if __name__ == "__main__":
    unittest.main()
