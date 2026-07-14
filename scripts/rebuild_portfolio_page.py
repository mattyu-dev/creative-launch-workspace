#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from meta_importer.portfolio_page import (
    render_case_study_page,
    render_not_found_page,
    render_portfolio_page,
    render_robots_txt,
    render_sitemap,
    render_social_card_page,
)


def main() -> int:
    (ROOT / "docs/index.html").write_text(render_portfolio_page())
    (ROOT / "docs/case-study.html").write_text(render_case_study_page())
    (ROOT / "docs/social-card.html").write_text(render_social_card_page())
    (ROOT / "docs/robots.txt").write_text(render_robots_txt())
    (ROOT / "docs/sitemap.xml").write_text(render_sitemap())
    (ROOT / "docs/404.html").write_text(render_not_found_page())
    print("Rebuilt GitHub Pages portfolio entry, social card, sitemap, robots, and 404")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
