#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from meta_importer.portfolio_page import render_portfolio_page, render_social_card_page


def main() -> int:
    (ROOT / "docs/index.html").write_text(render_portfolio_page())
    (ROOT / "docs/social-card.html").write_text(render_social_card_page())
    print("Rebuilt GitHub Pages portfolio entry")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
