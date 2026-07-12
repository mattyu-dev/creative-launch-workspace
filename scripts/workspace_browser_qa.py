#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from meta_importer.browser_qa import audit_workspace_browser_contract


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Audit generated workspace browser behavior")
    parser.add_argument("html", type=Path, help="Generated workspace.html file")
    parser.add_argument("--out", type=Path, required=True, help="Write browser QA JSON")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    report = audit_workspace_browser_contract(args.html.read_text())
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print("# Workspace browser QA")
    print(f"{args.html}: {report['status']} ({report['passed_count']}/{report['check_count']})")
    print(f"Wrote {args.out}")
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
