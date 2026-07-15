from __future__ import annotations

import json
import re
import unittest
from pathlib import Path
from urllib.parse import urljoin

from meta_importer.ai.contracts import FIELD_NAMES
from meta_importer.ai.evidence_page import render_evidence_page
from meta_importer.fix_lab import build_fix_lab_rule_pack, render_fix_lab
from meta_importer.product_page import (
    render_not_found_page,
    render_product_page,
    render_robots_txt,
    render_sitemap,
    render_social_card_page,
)


class ProductSurfaceTests(unittest.TestCase):
    def test_homepage_sells_one_product_with_inspectable_boundaries(self) -> None:
        html = render_product_page()

        self.assertIn('property="og:image"', html)
        self.assertIn('property="og:site_name" content="Creative Launch Workspace"', html)
        self.assertIn('name="author" content="Mathieu Petroni"', html)
        self.assertIn('property="og:type" content="website"', html)
        self.assertIn("social-card-v2-2.png", html)
        self.assertIn('name="theme-color" content="#24142b"', html)
        self.assertIn('name="twitter:image:alt"', html)
        self.assertIn('name="twitter:card" content="summary_large_image"', html)
        for token in (
            "--canvas:oklch(97.5% .006 315)",
            "--surface:oklch(100% 0 0)",
            "--ink:oklch(19% .032 315)",
            "--plum:oklch(21% .055 315)",
            "--lemon:oklch(91% .17 100)",
            "--fuchsia:oklch(57% .216 4)",
            "--lavender:oklch(82% .08 292)",
            "--border:oklch(87% .016 315)",
        ):
            self.assertIn(token, html)
        self.assertIn('@font-face{font-family:"Mona Sans"', html)
        self.assertIn('@font-face{font-family:"Geist Mono"', html)
        self.assertNotIn("#c83b24", html)
        self.assertNotIn("linear-gradient", html)
        self.assertIn(
            '.button[data-variant="primary"]:hover{background:var(--lemon-hover)}',
            html,
        )
        self.assertIn('.button:active{transform:scale(.97)', html)
        self.assertIn('data-variant="primary"', html)
        self.assertIn('href="workspace.html?guided=1"', html)
        self.assertNotIn('href="case-study.html"', html)
        self.assertIn('class="skip-link" href="#main"', html)
        self.assertIn('rel="me" href="https://www.linkedin.com/in/mathieu-petroni/"', html)
        self.assertIn('rel="me" href="https://github.com/mattyu-dev"', html)
        self.assertIn("The launch control layer before Ads Manager.", html)
        self.assertIn("Open the workspace", html)
        self.assertIn("Pre-launch QA for Meta creative operations", html)
        self.assertIn("A clean creative is not a clean launch.", html)
        self.assertIn("Turn the handoff into a controlled route.", html)
        self.assertIn("Automation proposes. Control stays explicit.", html)
        self.assertIn("AI proposes", html)
        self.assertIn("Rules verify", html)
        self.assertIn("People decide", html)
        self.assertIn("Interactive synthetic fixture", html)
        self.assertIn("No Meta publishing", html)
        self.assertEqual(html.count("synthetic fixture"), 1)
        self.assertIn('softwareVersion":"2.2.0"', html)
        self.assertEqual(html.count('<ol class="workflow-steps"'), 1)
        self.assertEqual(html.count('<ol class="handoff-list"'), 1)
        self.assertEqual(html.count('class="eyebrow"'), 1)
        self.assertEqual(html.count('role="tab" aria-selected'), 3)
        self.assertIn('<a href="#workflow">Workflow</a>', html)
        self.assertIn('<a href="#controls">Controls</a>', html)
        self.assertIn('<a href="#evidence">Evidence</a>', html)
        self.assertIn('type="image/avif"', html)
        self.assertIn('type="image/webp"', html)
        self.assertIn('font-family:"Mona Sans"', html)
        self.assertIn("font-display:optional", html)
        self.assertIn('decoding="async" fetchpriority="high"', html)
        self.assertIn("workspace-mobile-hero.webp", html)
        self.assertIn("workspace-mobile-hero.png", html)
        self.assertIn("guided-review-step-1.webp", html)
        self.assertIn("guided-review-step-3.png", html)
        self.assertIn("brief-evidence.png", html)
        visible_main = re.search(r"<main[^>]*>(.*?)</main>", html, re.DOTALL)
        self.assertIsNotNone(visible_main)
        before_closing = visible_main.group(1).split('class="closing"', maxsplit=1)[0]  # type: ignore[union-attr]
        self.assertNotIn("Mathieu", before_closing)
        hero = re.search(r'<section class="hero".*?</section>', html, re.DOTALL)
        self.assertIsNotNone(hero)
        self.assertNotIn("AI", re.sub(r"<[^>]+>", " ", hero.group(0)))  # type: ignore[union-attr]
        body = re.search(r"<body>(.*?)</body>", html, re.DOTALL)
        self.assertIsNotNone(body)
        visible_words = re.findall(r"\b[\w'-]+\b", re.sub(r"<[^>]+>", " ", body.group(1)))  # type: ignore[union-attr]
        self.assertLessEqual(len(visible_words), 850)
        visible_text = re.sub(r"<[^>]+>", " ", body.group(1))  # type: ignore[union-attr]
        for banned in (
            "case study",
            "personal project",
            "portfolio",
            "hiring",
            "my contribution",
            "proof without theatre",
            "review a sample",
        ):
            self.assertNotIn(banned, visible_text.lower())
        self.assertNotRegex(visible_text, "[\u2013\u2014]")

        json_ld_match = re.search(
            r'<script type="application/ld\+json">\s*(.*?)\s*</script>', html, re.DOTALL
        )
        self.assertIsNotNone(json_ld_match)
        graph = json.loads(json_ld_match.group(1))["@graph"]  # type: ignore[union-attr]
        self.assertEqual(
            {item["@type"] for item in graph},
            {"Person", "SoftwareApplication", "WebSite"},
        )
        person = next(item for item in graph if item["@type"] == "Person")
        self.assertEqual(person["jobTitle"], "AI Automation Builder")

    def test_removed_route_has_no_generated_file_or_sitemap_entry(self) -> None:
        self.assertFalse(Path("docs/case-study.html").exists())
        self.assertNotIn("case-study.html", render_sitemap())

    def test_social_card_has_safe_dedicated_composition(self) -> None:
        html = render_social_card_page()

        self.assertIn("width:1200px;height:630px", html)
        self.assertIn("Mathieu Petroni", html)
        self.assertIn("Creative Launch Workspace", html)
        self.assertIn("workspace-mobile-hero.png", html)
        self.assertIn("The launch control layer before Ads Manager.", html)
        self.assertIn("Check every creative row, route each exception", html)
        self.assertIn("Interactive workspace", html)
        self.assertNotIn("Personal product case study", html)
        self.assertIn("#24142b", html)
        self.assertIn("#ffe44d", html)
        self.assertNotIn("#c83b24", html)
        self.assertNotIn("object-fit:cover", html)
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
        self.assertIn('aria-label="Product navigation"', html)
        self.assertIn("Open the workspace", html)
        self.assertIn("Back to product", html)
        self.assertNotIn("case study", html.lower())
        self.assertNotIn("hiring", html.lower())
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
        self.assertIn('aria-label="Product navigation"', rendered)
        self.assertIn("Open the workspace", rendered)
        self.assertIn("Back to product", rendered)
        self.assertNotIn("case study", rendered.lower())
        self.assertNotIn("hiring", rendered.lower())
        self.assertIn("social-card-v2-2.png", rendered)

    def test_github_pages_discovery_and_not_found_surfaces(self) -> None:
        robots = render_robots_txt()
        sitemap = render_sitemap()
        not_found = render_not_found_page()

        self.assertIn("User-agent: *\nAllow: /", robots)
        self.assertIn("creative-launch-workspace/sitemap.xml", robots)
        self.assertEqual(sitemap.count("<url>"), 4)
        self.assertNotIn("case-study.html", sitemap)
        self.assertIn("workspace.html", sitemap)
        self.assertIn('name="robots" content="noindex"', not_found)
        self.assertIn("Return to the product", not_found)
        self.assertIn("Contact Mathieu", not_found)
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
