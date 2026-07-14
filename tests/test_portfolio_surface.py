from __future__ import annotations

import json
import re
import unittest
from urllib.parse import urljoin

from meta_importer.ai.contracts import FIELD_NAMES
from meta_importer.ai.evidence_page import render_evidence_page
from meta_importer.fix_lab import build_fix_lab_rule_pack, render_fix_lab
from meta_importer.portfolio_page import (
    render_not_found_page,
    render_portfolio_page,
    render_robots_txt,
    render_sitemap,
    render_social_card_page,
)


class PortfolioSurfaceTests(unittest.TestCase):
    def test_linkedin_entry_has_social_metadata_and_honest_boundaries(self) -> None:
        html = render_portfolio_page()

        self.assertIn('property="og:image"', html)
        self.assertIn('property="og:site_name"', html)
        self.assertIn('name="author" content="Mathieu Petroni"', html)
        self.assertIn('property="og:type" content="article"', html)
        self.assertIn('property="article:author"', html)
        self.assertIn("social-card-v1-7.png", html)
        self.assertIn(
            'content="How I built a governed AI workflow for creative launches | Mathieu Petroni"',
            html,
        )
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
        self.assertIn("One launch review is split across too many tools.", html)
        self.assertIn("Why not another launch spreadsheet?", html)
        self.assertIn("Experience the workflow", html)
        self.assertIn("Inspect the system", html)
        self.assertIn("Review engineering evidence", html)
        self.assertIn("What this does not prove", html)
        self.assertIn("What I would validate next", html)
        self.assertIn("Proposed production pilot metrics · not measured results", html)
        self.assertIn("Hiring or project conversation", html)
        self.assertIn("Connect with Mathieu on LinkedIn", html)
        self.assertIn('version": "1.7.0"', html)
        self.assertIn("live platform mutations. The demo cannot publish or change spend.", html)
        self.assertIn("One decision queue holds the review state.", html)
        self.assertIn("No stage can make the next decision on its own.", html)
        self.assertIn("See how the system works &rarr;", html)
        self.assertIn("since 2017", html)
        self.assertIn("reviewing large campaign batches", html)
        self.assertIn("Every proposal needs evidence.", html)
        self.assertIn("The tests, browser reports and generated evidence live in the repository.", html)
        self.assertIn("What the prototype proves, and what still needs testing.", html)
        self.assertIn("I built the workflow, interface, Python contracts", html)
        self.assertIn('<time datetime="2026-07-14">', html)
        self.assertIn('<svg viewBox="0 0 720 530" role="img"', html)
        self.assertIn('class="architecture-stack"', html)
        self.assertEqual(html.count('<div class="difference">'), 3)
        self.assertEqual(html.count('<div class="metric-group">'), 3)
        self.assertEqual(html.count('<li><strong>'), 7)
        self.assertIn('<a href="#business">Business case</a>', html)
        self.assertIn('<a href="#system">System</a>', html)
        self.assertIn('<a href="#evidence">Evidence</a>', html)
        self.assertIn('<a href="#about">Contribution</a>', html)
        self.assertIn('type="image/avif"', html)
        self.assertIn('type="image/webp"', html)
        self.assertIn('decoding="async" fetchpriority="high"', html)
        self.assertIn("workspace-mobile-hero.webp", html)
        self.assertIn("workspace-mobile-hero.png", html)
        self.assertIn("The demo begins after governed brief intake.", html)
        self.assertEqual(html.count('<div class="ai-proof '), 2)
        self.assertIn("Accepted by reviewer", html)
        self.assertIn("Destination URL", html)
        self.assertIn("Not found in source", html)
        self.assertIn("Human input before materialization", html)
        self.assertIn("Fixture scale", html)
        self.assertIn("Exception coverage", html)
        self.assertIn("Safety boundary", html)
        self.assertNotRegex(html, r'<div[^>]+aria-label=')
        self.assertNotIn('aria-label="Open the guided interactive review workspace"', html)
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
        self.assertNotIn("Rows are easy. Governed decisions are harder.", html)
        self.assertNotIn("Inspect the evidence, not the promise.", html)
        self.assertNotIn("A reference implementation with a serious next-proof plan.", html)
        self.assertNotIn("AI proposes. Rules verify. A human decides.", html)
        self.assertNotIn("Launch risk accumulates in the handoff.", html)
        self.assertNotIn("Exercise human authority.", html)
        self.assertNotIn("—", html)
        self.assertNotIn("–", html)
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
        self.assertIn("AI automation · Product systems · Growth operations", html)
        self.assertIn("workspace-desktop.png", html)
        self.assertIn("Synthetic fixture", html)
        self.assertIn("Reproducible evidence", html)
        self.assertIn("No Meta write path", html)
        self.assertIn("Rules verify. A person decides.", html)
        self.assertIn("Built and documented by Mathieu", html)
        self.assertIn('class="creator-copy"', html)
        self.assertNotIn(".creator span{", html)
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
        self.assertIn('name="author" content="Mathieu Petroni"', html)
        self.assertIn("Mathieu Petroni / Creative Launch Workspace", html)
        self.assertIn("Connect on LinkedIn", html)
        self.assertNotIn("font:600 13px/1.2 inherit", html)

    def test_secondary_evidence_page_converts_back_to_mathieu(self) -> None:
        receipt = {
            "fields": {
                name: {
                    "value": f"fixture-{name}",
                    "evidence_quote": f"source-{name}",
                    "confidence_band": "high",
                    "review_status": "accepted",
                }
                for name in FIELD_NAMES
            }
        }
        proposal = {
            "provider": "deterministic",
            "model": "fixture",
            "contract_version": "test.v1",
            "prompt_sha256": "a" * 64,
            "schema_sha256": "b" * 64,
        }
        rendered = render_evidence_page(
            brief="Synthetic brief",
            proposal=proposal,
            receipt=receipt,
            materialization={
                "row_count": 2,
                "validation_summary": {"batch_states": {"launch_ready": 2}},
            },
        )

        self.assertIn('name="author" content="Mathieu Petroni"', rendered)
        self.assertIn("Mathieu Petroni / Creative Launch Workspace", rendered)
        self.assertIn("Connect on LinkedIn", rendered)
        self.assertIn("social-card-v1-7.png", rendered)

    def test_github_pages_discovery_and_not_found_surfaces(self) -> None:
        robots = render_robots_txt()
        sitemap = render_sitemap()
        not_found = render_not_found_page()

        self.assertIn("User-agent: *\nAllow: /", robots)
        self.assertIn("creative-launch-workspace/sitemap.xml", robots)
        self.assertEqual(sitemap.count("<url>"), 4)
        self.assertIn("workspace.html", sitemap)
        self.assertIn('name="robots" content="noindex"', not_found)
        self.assertIn("Mathieu Petroni's case study", not_found)
        self.assertIn("Connect on LinkedIn", not_found)
        nested_missing_url = (
            "https://mattyu-dev.github.io/creative-launch-workspace/missing/nested/page"
        )
        resolved_links = {
            urljoin(nested_missing_url, href)
            for href in re.findall(r'href="([^"]+)"', not_found)
        }
        self.assertIn(
            "https://mattyu-dev.github.io/creative-launch-workspace/", resolved_links
        )
        self.assertIn(
            "https://mattyu-dev.github.io/creative-launch-workspace/workspace.html?guided=1",
            resolved_links,
        )
        self.assertIn(
            "https://mattyu-dev.github.io/creative-launch-workspace/assets/favicon.svg",
            resolved_links,
        )


if __name__ == "__main__":
    unittest.main()
