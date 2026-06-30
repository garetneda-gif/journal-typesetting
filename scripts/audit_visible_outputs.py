#!/usr/bin/env python3
"""Audit visible files in MedBA issue/article folders."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

ARTICLE_DIR_RE = re.compile(r"^mbam\d{2,}-.+")
IGNORED_ROOT_NAMES = {".DS_Store", ".logs", ".sequence", ".reference", ".incoming"}


def _article_short_title(folder_name: str) -> str:
    return folder_name.split("-", 1)[1]


def audit_root(issue_root: str | Path, allow_pdf: bool = False) -> dict[str, Any]:
    root = Path(issue_root)
    unexpected: list[dict[str, str]] = []
    checked: list[str] = []
    warnings: list[str] = []

    if not root.exists():
        return {"ok": False, "checked_folders": [], "unexpected": [], "warnings": [], "errors": [f"root not found: {root}"]}

    for item in sorted(root.iterdir(), key=lambda p: p.name):
        if item.name in IGNORED_ROOT_NAMES or item.name.startswith("."):
            continue
        if item.is_dir() and ARTICLE_DIR_RE.match(item.name):
            checked.append(item.name)
            short = _article_short_title(item.name)
            allowed = {f"two-column-{short}.html", f"single-column-{short}.html"}
            if allow_pdf:
                allowed.add(f"two-column-{short}.pdf")
            for child in sorted(item.iterdir(), key=lambda p: p.name):
                if child.name == ".DS_Store" or child.name.startswith("."):
                    continue
                if child.name not in allowed:
                    unexpected.append({"folder": item.name, "path": str(child.relative_to(root)), "type": "dir" if child.is_dir() else "file"})
        elif item.is_file():
            unexpected.append({"folder": ".", "path": item.name, "type": "file"})
        elif item.is_dir():
            warnings.append(f"ignored non-article visible directory: {item.name}")

    return {"ok": not unexpected, "checked_folders": checked, "unexpected": unexpected, "warnings": warnings, "errors": []}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("issue_root")
    parser.add_argument("--allow-pdf", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    report = audit_root(args.issue_root, allow_pdf=args.allow_pdf)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"checked folders: {len(report['checked_folders'])}")
        if report["unexpected"]:
            print("unexpected visible files:")
            for item in report["unexpected"]:
                print(f"- {item['path']}")
        if report["warnings"]:
            print("warnings:")
            for warning in report["warnings"]:
                print(f"- {warning}")
        print("PASS" if report["ok"] else "FAIL")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
