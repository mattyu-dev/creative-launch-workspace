#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from meta_importer.fix_lab import build_fix_lab_rule_pack, render_fix_lab


def main() -> int:
    pack = build_fix_lab_rule_pack()
    (ROOT / "docs/evidence/interactive-rule-pack.json").write_text(
        json.dumps(pack, indent=2, sort_keys=True) + "\n"
    )
    (ROOT / "docs/fix-lab.html").write_text(render_fix_lab(pack))
    print("Rebuilt Fix & Revalidate Lab and eight Python golden scenarios")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
