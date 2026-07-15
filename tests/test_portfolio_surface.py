from __future__ import annotations

import json
import re
import unittest
from urllib.parse import urljoin

from meta_importer.ai.contracts import FIELD_NAMES
from meta_importer.ai.evidence_page import render_evidence_page
from meta_importer.fix_lab import build_fix_lab_rule_pack, render_fix_lab
from meta_importer.portfolio_page import (
    render_case_study_page,
    render_not_found_page,
    render_portfolio_page,
    render_robots_txt,
    render_sitemap,
    render_social_card_page,
)


class PortfolioSurfaceTests(unittest.TestCase):
    def test_linkedin_entry_is_a_product_first_landing_with_final_references(self) -> None:
        html = render_portfolio_page()

        self.assertIn('property="og:image"', html)
        self.assertIn('property="og:site_name" content="Creative Launch Workspace"', html)
        self.assertIn('name="author" content="Mathieu Petroni"', html)
        self.assertIn('property="og:type" content="website"', html)
        self.assertIn("social-card-v2-0.png", html)
        self.assertIn('content="Catch launch blockers before Ads Manager"', html)
        self.assertIn('name="theme-color" content="#f4f1ea"', html)
        self.assertIn('name="twitter:image:alt"', html)
        self.assertIn('name="twitter:card" content="summary_large_image"', html)
        for token in (
            "--canvas:#f4f1ea",
            "--surface:#fbf9f5",
            "--raised:#fffdf8",
            "--ink:#1d1f1c",
            "--muted:#666b64",
            "--border:#d7d8d2",
            "--brand:#b83b1f",
            "--brand-hover:#972d18",
            "--brand-soft:#f4dcd4",
        ):
            self.assertIn(token, html)
        self.assertNotIn("#7bd9b0", html)
        self.assertNotIn("#5e6ad2", html)
        self.assertNotIn("body:before", html)
        self.assertNotIn("linear-gradient", html)
        self.assertIn(
            '.button[data-variant="primary"]:hover{background:var(--brand-hover)}',
            html,
        )
        self.assertIn('.button:active{transform:scale(.98)}', html)
        self.assertIn('data-variant="primary"', html)
        self.assertNotIn("--serif", html)
        self.assertIn('href="workspace.html?guided=1"', html)
        self.assertIn('href="workspace.html"', html)
        self.assertNotIn('href="case-study.html"', html)
        self.assertIn('class="skip-link" href="#main"', html)
        self.assertIn('rel="me" href="https://www.linkedin.com/in/mathieu-petroni/"', html)
        self.assertIn('rel="me" href="https://github.com/mattyu-dev"', html)
        self.assertIn("Catch launch blockers before Ads Manager.", html)
        self.assertIn("Review a sample batch", html)
        self.assertIn("Pre-launch QA for Meta creative teams", html)
        self.assertIn("routes every detected exception to an owner", html)
        self.assertIn("The model proposes. Rules verify. People decide.", html)
        self.assertIn("Product judgment and implementation, in one system.", html)
        self.assertIn("64 automated tests", html)
        self.assertIn("It does not manufacture customer impact.", html)
        self.assertIn("no customer data, no Meta credentials and no publishing path", html)
        self.assertIn('softwareVersion":"2.0.0"', html)
        self.assertNotIn("object-fit:cover", html)
        self.assertIn("since 2017", html)
        self.assertEqual(html.count('<li><b>'), 7)
        self.assertEqual(html.count('<ul class="sample-metrics"'), 1)
        self.assertIn('<a href="#workflow">How it works</a>', html)
        self.assertIn('<a href="#architecture">Controls</a>', html)
        self.assertNotIn('<a href="#role">My role</a>', html)
        self.assertIn('type="image/avif"', html)
        self.assertIn('type="image/webp"', html)
        self.assertIn('decoding="async" fetchpriority="high"', html)
        self.assertIn("workspace-mobile-hero.webp", html)
        self.assertIn("workspace-mobile-hero.png", html)
        self.assertIn("guided-receipt-mobile.webp", html)
        self.assertIn("guided-review-step-3.png", html)
        visible_main = re.search(r"<main[^>]*>(.*?)</main>", html, re.DOTALL)
        self.assertIsNotNone(visible_main)
        before_builder = visible_main.group(1).split('id="about"', maxsplit=1)[0]  # type: ignore[union-attr]
        self.assertNotIn("Mathieu", before_builder)
        self.assertNotIn("I built", before_builder)
        self.assertNotIn("Personal project", before_builder)
        self.assertNotIn("case study", before_builder.lower())
        self.assertNotIn("Hiring", before_builder)
        body = re.search(r"<body>(.*?)</body>", html, re.DOTALL)
        self.assertIsNotNone(body)
        visible_words = re.findall(r"\b[\w'-]+\b", re.sub(r"<[^>]+>", " ", body.group(1)))  # type: ignore[union-attr]
        self.assertLessEqual(len(visible_words), 620)

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

    def test_legacy_case_study_redirects_to_the_single_product_page(self) -> None:
        html = render_case_study_page()

        self.assertIn(
            '<link rel="canonical" href="https://mattyu-dev.github.io/creative-launch-workspace/">',
            html,
        )
        self.assertIn('name="robots" content="noindex,follow"', html)
        self.assertIn('http-equiv="refresh" content="0; url=./#architecture"', html)
        self.assertIn('window.location.replace("./#architecture")', html)
        self.assertIn('href="./#architecture"', html)
        self.assertNotIn('property="og:type" content="article"', html)
        self.assertNotIn("Technical case study", html)

    def test_social_card_has_safe_dedicated_composition(self) -> None:
        html = render_social_card_page()

        self.assertIn("width:1200px;height:630px", html)
        self.assertIn("Mathieu Petroni", html)
        self.assertIn("Creative Launch Workspace", html)
        self.assertIn("workspace-desktop.png", html)
        self.assertIn("Catch launch blockers before Ads Manager.", html)
        self.assertIn("Check every row, route detected exceptions", html)
        self.assertIn("Interactive sample", html)
        self.assertIn("No publishing permissions", html)
        self.assertNotIn("Personal product case study", html)
        self.assertIn("#f4f1ea", html)
        self.assertIn("#b83b1f", html)
        self.assertNotIn("#5e6ad2", html)
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
        self.assertIn("Review a sample batch", html)
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
        self.assertIn("Review a sample batch", rendered)
        self.assertIn("Back to product", rendered)
        self.assertNotIn("case study", rendered.lower())
        self.assertNotIn("hiring", rendered.lower())
        self.assertIn("social-card-v2-0.png", rendered)

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
