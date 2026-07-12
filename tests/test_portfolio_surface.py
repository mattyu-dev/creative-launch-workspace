from __future__ import annotations

import unittest

from meta_importer.fix_lab import build_fix_lab_rule_pack, render_fix_lab
from meta_importer.portfolio_page import render_portfolio_page, render_social_card_page


class PortfolioSurfaceTests(unittest.TestCase):
    def test_linkedin_entry_has_social_metadata_and_honest_boundaries(self) -> None:
        html = render_portfolio_page()

        self.assertIn('property="og:image"', html)
        self.assertIn('name="twitter:card" content="summary_large_image"', html)
        self.assertIn('href="workspace.html"', html)
        self.assertIn('href="fix-lab.html"', html)
        self.assertIn("100-row synthetic fixture", html)
        self.assertIn("Designed and built end to end by Mathieu Petroni.", html)
        self.assertIn("Designed and built by Mathieu Petroni · AI Automation Lead", html)
        self.assertIn("From scattered handoffs to one decision queue.", html)
        self.assertIn("Spend human attention only where it matters.", html)
        self.assertIn("CMO · Operations", html)
        self.assertIn("CTO · Engineering", html)
        self.assertIn("Recruiting · Technical depth", html)
        self.assertIn("What this does not prove", html)
        self.assertIn("live model quality is not claimed", html)
        self.assertIn("synthetic, local-first and non-executable", html)
        self.assertNotIn("one accountable review path", html)
        self.assertNotIn("Model proposes.", html)
        self.assertNotIn("cleared automatically", html)

    def test_social_card_has_safe_dedicated_composition(self) -> None:
        html = render_social_card_page()

        self.assertIn("width:1200px; height:630px", html)
        self.assertIn("padding:46px 64px 42px", html)
        self.assertIn("Built by Mathieu Petroni", html)
        self.assertNotIn("workspace-desktop.png", html)

    def test_fix_lab_replays_every_bounded_python_scenario(self) -> None:
        pack = build_fix_lab_rule_pack()

        self.assertEqual(pack["contract_version"], "fix_lab_rule_pack.v1")
        self.assertEqual(len(pack["scenarios"]), 8)
        initial = pack["scenarios"]["feed|pending|camp_launch"]
        target = pack["scenarios"]["story|approved|camp_sale"]
        self.assertEqual(initial["state"], "blocked")
        self.assertEqual(
            {issue["code"] for issue in initial["issues"]},
            {"pending_approval", "format_placement_mismatch", "utm_campaign_mismatch"},
        )
        self.assertEqual(target["state"], "launch_ready")
        self.assertEqual(target["issues"], [])
        self.assertEqual(len(pack["rule_pack_sha256"]), 64)

    def test_fix_lab_renderer_embeds_contract_and_boundaries(self) -> None:
        html = render_fix_lab(build_fix_lab_rule_pack())

        self.assertIn("8 Python golden scenarios", html)
        self.assertIn("The browser does not invent or execute validation rules.", html)
        self.assertIn("external_write:false", html)
        self.assertIn('href="evidence/interactive-rule-pack.json"', html)


if __name__ == "__main__":
    unittest.main()
