from __future__ import annotations

import json
import re
import unittest

from meta_importer.fix_lab import build_fix_lab_rule_pack, render_fix_lab
from meta_importer.portfolio_page import render_portfolio_page, render_social_card_page


class PortfolioSurfaceTests(unittest.TestCase):
    def test_linkedin_entry_has_social_metadata_and_honest_boundaries(self) -> None:
        html = render_portfolio_page()

        self.assertIn('property="og:image"', html)
        self.assertIn('property="og:site_name"', html)
        self.assertIn('name="theme-color" content="#113e31"', html)
        self.assertIn('name="twitter:image:alt"', html)
        self.assertIn('name="twitter:card" content="summary_large_image"', html)
        self.assertIn('href="workspace.html?guided=1"', html)
        self.assertIn('href="fix-lab.html"', html)
        self.assertIn('class="skip-link" href="#main"', html)
        self.assertIn('rel="me" href="https://www.linkedin.com/in/mathieu-petroni/"', html)
        self.assertIn('rel="me" href="https://github.com/mattyu-dev"', html)
        self.assertIn("100-row Meta creative batch", html)
        self.assertIn("These are test outcomes and implementation boundaries, not customer or business results.", html)
        self.assertIn("Mathieu Petroni · AI Automation Lead", html)
        self.assertIn("Launch risk accumulates in the handoff.", html)
        self.assertIn("Why not another launch spreadsheet?", html)
        self.assertIn("Experience the workflow", html)
        self.assertIn("Inspect the system", html)
        self.assertIn("Review engineering evidence", html)
        self.assertIn("What this does not prove", html)
        self.assertIn("What I would validate next", html)
        self.assertIn("Proposed production pilot metrics · not measured results", html)
        self.assertIn("Building an AI workflow where trust matters?", html)
        self.assertIn('version": "1.6.2"', html)
        self.assertIn("live platform mutations — by design", html)
        self.assertIn("One decision queue holds the review state.", html)
        self.assertIn("Each stage has deliberately bounded authority.", html)
        self.assertIn("See how the system works &rarr;", html)
        self.assertIn("since 2017", html)
        self.assertIn('<time datetime="2026-07-13">', html)
        self.assertIn('<svg viewBox="0 0 720 530" role="img"', html)
        self.assertIn('class="architecture-stack"', html)
        self.assertEqual(html.count('<div class="difference">'), 3)
        self.assertEqual(html.count('<div class="metric-group">'), 3)
        self.assertEqual(html.count('<li><strong>'), 7)
        self.assertIn('<a href="#business">Business case</a>', html)
        self.assertIn('<a href="#system">System</a>', html)
        self.assertIn('<a href="#evidence">Evidence</a>', html)
        self.assertIn('<a href="#about">About</a>', html)
        self.assertIn('type="image/avif"', html)
        self.assertIn('type="image/webp"', html)
        self.assertIn('decoding="async" fetchpriority="high"', html)
        self.assertIn("workspace-mobile-hero.webp", html)
        self.assertIn("workspace-mobile-hero.png", html)
        self.assertIn("The demo begins after governed brief intake.", html)
        self.assertEqual(html.count('<article class="ai-proof'), 2)
        self.assertIn("Accepted by reviewer", html)
        self.assertIn("Destination URL", html)
        self.assertIn("Not found in source", html)
        self.assertIn("Human input before materialization", html)
        self.assertNotIn("CMO · Operations", html)
        self.assertNotIn("CTO · Engineering", html)
        self.assertNotIn("Recruiting · Technical depth", html)
        self.assertNotIn("one accountable review path", html)
        self.assertNotIn("Model proposes.", html)
        self.assertNotIn("cleared automatically", html)
        self.assertNotIn("Exclusive states across a 100-row synthetic fixture", html)
        self.assertNotIn("hero-mobile-author", html)
        self.assertNotIn("The expensive part is usually the handoff.", html)
        self.assertNotIn("certified viewport", html)
        self.assertNotIn("external writes available in this implementation", html)
        self.assertNotIn("holds the launch state", html)
        self.assertNotIn("narrower authority than the one before it", html)
        self.assertNotIn("Explore architecture and evidence", html)
        self.assertNotIn("nine years", html)
        self.assertNotIn("30</strong>", html)
        self.assertNotIn("60</strong>", html)
        self.assertNotIn("10</strong>", html)

        json_ld_match = re.search(
            r'<script type="application/ld\+json">\s*(.*?)\s*</script>', html, re.DOTALL
        )
        self.assertIsNotNone(json_ld_match)
        graph = json.loads(json_ld_match.group(1))["@graph"]  # type: ignore[union-attr]
        self.assertEqual(
            {item["@type"] for item in graph},
            {"Person", "SoftwareSourceCode", "CreativeWork"},
        )

    def test_social_card_has_safe_dedicated_composition(self) -> None:
        html = render_social_card_page()

        self.assertIn("width:1200px;height:630px", html)
        self.assertIn("Mathieu Petroni", html)
        self.assertIn("AI Automation · Product Systems", html)
        self.assertIn("workspace-desktop.png", html)
        self.assertIn("100</b> fixture rows", html)
        self.assertIn("70</b> seeded exceptions", html)
        self.assertIn("0</b> live mutations", html)
        self.assertNotIn("30</b>", html)
        self.assertNotIn("60</b>", html)
        self.assertNotIn("10</b>", html)

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
        self.assertIn('rel="icon" href="assets/favicon.svg"', html)


if __name__ == "__main__":
    unittest.main()
