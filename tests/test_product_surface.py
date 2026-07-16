from __future__ import annotations

import json
import re
import unittest
from html.parser import HTMLParser
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


class _VisibleTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hidden_depth = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.casefold() in {"script", "style"}:
            self.hidden_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag.casefold() in {"script", "style"} and self.hidden_depth:
            self.hidden_depth -= 1

    def handle_data(self, data: str) -> None:
        if not self.hidden_depth:
            self.parts.append(data)

    @property
    def text(self) -> str:
        return " ".join(self.parts)


class ProductSurfaceTests(unittest.TestCase):
    def test_homepage_sells_one_product_with_inspectable_boundaries(self) -> None:
        html = render_product_page()

        self.assertIn('property="og:image"', html)
        self.assertIn('property="og:site_name" content="Creative Launch Workspace"', html)
        self.assertIn('name="author" content="Mathieu Petroni"', html)
        self.assertIn('property="og:type" content="website"', html)
        self.assertIn("social-card-v4.png", html)
        self.assertIn('name="theme-color" content="#ECEDEE"', html)
        self.assertIn('name="twitter:image:alt"', html)
        self.assertIn('name="twitter:card" content="summary_large_image"', html)
        for token in (
            "--canvas:#ECEDEE",
            "--shell:#F4F5F5",
            "--surface:#FFFFFF",
            "--ink:#232427",
            "--charcoal:#171719",
            "--orange:#E34A32",
            "--orange-hover:#F05A3C",
            "--orange-copy:#A93625",
            "--body:#55575C",
        ):
            self.assertIn(token, html)
        self.assertIn('@font-face{font-family:"Inter"', html)
        self.assertIn('@font-face{font-family:"Instrument Serif"', html)
        self.assertNotIn("--plum:", html)
        self.assertNotIn("--lemon:", html)
        self.assertNotIn("--fuchsia:", html)
        self.assertIn('.button:active{transform:scale(.98)', html)
        self.assertNotIn("transition:all", html.replace(" ", "").lower())
        self.assertIn('data-variant="primary"', html)
        self.assertIn('href="workspace.html?guided=1"', html)
        self.assertNotIn('href="case-study.html"', html)
        self.assertIn('class="skip-link" href="#main"', html)
        self.assertIn('rel="me" href="https://www.linkedin.com/in/mathieu-petroni/"', html)
        self.assertIn('rel="me" href="https://github.com/mattyu-dev"', html)
        self.assertIn("Catch creative launch mistakes before Ads Manager.", html)
        self.assertIn("Try the live workspace", html)
        self.assertIn("Pre-launch QA for Meta Ads", html)
        self.assertIn("From creative manifest", html)
        self.assertIn("Creative manifest", html)
        self.assertIn("Check, route, review", html)
        self.assertIn("Reviewed launch plan", html)
        self.assertIn("AI prepares the review.", html)
        self.assertIn("Only people approve", html)
        self.assertIn("Current synthetic run", html)
        self.assertIn("Fixture data, no external writes", html)
        self.assertIn('softwareVersion":"4.0.0"', html)
        self.assertEqual(html.count('role="tab" aria-selected'), 3)
        self.assertIn('<a href="#workflow">Workflow</a>', html)
        self.assertIn('<a href="#safeguards">Safeguards</a>', html)
        self.assertIn('<a href="#evidence">Evidence</a>', html)
        self.assertIn('font-family:"Inter"', html)
        self.assertIn("font-display:optional", html)
        self.assertIn('id="hero-motion-root"', html)
        self.assertIn('id="meshGL"', Path("frontend/launch-control-motion.jsx").read_text())
        self.assertIn('import("./assets/launch-control-motion.js")', html)
        self.assertNotIn('rel="stylesheet" href="assets/launch-control-motion.css"', html)
        self.assertIn("stylesheet.href = 'assets/launch-control-motion.css'", Path("frontend/launch-control-motion.jsx").read_text())
        self.assertNotIn("launch-control-core-v3", html)
        for legacy_asset in (
            "workspace-mobile-hero",
            "workspace-desktop",
            "guided-review-step",
            "brief-evidence.png",
        ):
            self.assertNotIn(legacy_asset, html)
        for exact_fact in (
            "78f20843aea8a367",
            "synthetic_fixture_only",
            "cr_007",
            "post_c30fe8f1d4",
            "example.invalid/launch-us",
            "external_mutation:false",
        ):
            if exact_fact in {"synthetic_fixture_only", "external_mutation:false"}:
                continue
            self.assertIn(exact_fact, html)
        self.assertIn("external_mutation:false", html)
        self.assertIn("download='review_state.json'", html)
        self.assertIn('aria-live="polite"', html)
        self.assertIn("new ResizeObserver", html)
        self.assertIn("prefers-reduced-motion:reduce", html)
        visible_main = re.search(r"<main[^>]*>(.*?)</main>", html, re.DOTALL)
        self.assertIsNotNone(visible_main)
        before_closing = visible_main.group(1).split('class="closing"', maxsplit=1)[0]  # type: ignore[union-attr]
        self.assertNotIn("Mathieu", before_closing)
        hero = re.search(r'<section class="hero".*?</section>', html, re.DOTALL)
        self.assertIsNotNone(hero)
        self.assertNotIn("case study", re.sub(r"<[^>]+>", " ", hero.group(0)).lower())  # type: ignore[union-attr]
        body = re.search(r"<body>(.*?)</body>", html, re.DOTALL)
        self.assertIsNotNone(body)
        visible_parser = _VisibleTextParser()
        visible_parser.feed(body.group(1))  # type: ignore[union-attr]
        visible_text = visible_parser.text
        visible_words = re.findall(r"\b[\w'-]+\b", visible_text)
        self.assertLessEqual(len(visible_words), 850)
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
        self.assertIn("Launch Control", html)
        self.assertIn("RECORDED DECISION TRACE", html)
        self.assertNotIn("launch-control-core-v3", html)
        self.assertIn("Detect", html)
        self.assertIn("Route", html)
        self.assertIn("Prove", html)
        self.assertIn("Catch creative launch mistakes before Ads Manager.", html)
        self.assertIn("Validate every creative row.", html)
        self.assertIn("Interactive product", html)
        self.assertNotIn("Personal product case study", html)
        self.assertIn("#171719", html)
        self.assertIn("#E34A32", html)
        self.assertNotIn("workspace-mobile-hero", html)

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
        self.assertIn("social-card-v4.png", rendered)

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
