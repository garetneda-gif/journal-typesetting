#!/usr/bin/env python3
"""Audit DOI and page consistency between sequence table and outputs."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any

MALFORMED_DOI_RE = re.compile(r"10\.65079(?://+mbam\d{2,}|mbam\d{2,}|/[A-Z0-9]+)")
PAGE_NUMBER_RES = [
    re.compile(r"class=[\"'][^\"']*(?:page-number|footer-page|page-no)[^\"']*[\"'][^>]*>\s*(\d+)\s*<", re.I),
    re.compile(r">\s*(\d+)\s*</(?:span|div)>\s*</(?:footer|div)>", re.I),
]


def load_sequence(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _active_entries(data: dict[str, Any]) -> list[dict[str, Any]]:
    return [e for e in data.get("entries", []) if e.get("status", "active") == "active"]


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _extract_page_numbers(html: str) -> list[int]:
    values: list[int] = []
    for regex in PAGE_NUMBER_RES:
        for match in regex.finditer(html):
            try:
                values.append(int(match.group(1)))
            except ValueError:
                continue
        if values:
            break
    return values


def _check_html_file(path: Path, expected_doi: str, entry: dict[str, Any], errors: list[str], warnings: list[str], check_pages: bool) -> None:
    label = entry.get("short_title") or entry.get("doi_suffix") or str(path)
    if not path.exists():
        errors.append(f"{label}: missing HTML file {path}")
        return
    html = _read_text(path)
    malformed = sorted(set(MALFORMED_DOI_RE.findall(html)))
    for value in malformed:
        if value != expected_doi:
            errors.append(f"{label}: malformed DOI {value} in {path.name}")
    if expected_doi not in html:
        errors.append(f"{label}: missing expected DOI {expected_doi} in {path.name}")

    if check_pages:
        found = _extract_page_numbers(html)
        if found:
            expected = list(range(entry["page_start"], entry["page_end"] + 1))
            if sorted(set(found)) != expected:
                errors.append(f"{label}: page footer mismatch in {path.name}; expected {expected}, found {sorted(set(found))}")
        else:
            warnings.append(f"{label}: no page footer numbers detected in {path.name}")


def _pdf_page_count(path: Path) -> int | None:
    pdfinfo = shutil.which("pdfinfo")
    if not pdfinfo:
        return None
    result = subprocess.run([pdfinfo, str(path)], capture_output=True, text=True, timeout=20)
    if result.returncode != 0:
        return None
    for line in result.stdout.splitlines():
        if line.lower().startswith("pages:"):
            try:
                return int(line.split(":", 1)[1].strip())
            except ValueError:
                return None
    return None


def _pdf_text(path: Path) -> str | None:
    try:
        from pypdf import PdfReader  # type: ignore
    except Exception:
        return None
    try:
        reader = PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception:
        return None


def _check_pdf(path: Path, expected_doi: str, entry: dict[str, Any], errors: list[str], warnings: list[str], strict_pdf: bool) -> None:
    label = entry.get("short_title") or entry.get("doi_suffix") or str(path)
    if not path.exists():
        message = f"{label}: missing PDF file {path}"
        (errors if strict_pdf else warnings).append(message)
        return

    count = _pdf_page_count(path)
    if count is None:
        message = f"{label}: pdfinfo unavailable or could not read page count for {path.name}"
        (errors if strict_pdf else warnings).append(message)
    elif count != entry.get("page_count"):
        errors.append(f"{label}: PDF page count mismatch; expected {entry.get('page_count')}, found {count}")

    text = _pdf_text(path)
    if text is None:
        message = f"{label}: pypdf unavailable or could not extract text from {path.name}"
        (errors if strict_pdf else warnings).append(message)
        return
    malformed = sorted(set(MALFORMED_DOI_RE.findall(text)))
    for value in malformed:
        if value != expected_doi:
            errors.append(f"{label}: malformed DOI {value} in {path.name}")
    if expected_doi not in text:
        errors.append(f"{label}: missing expected DOI {expected_doi} in {path.name}")


def audit_sequence_outputs(sequence_path: str | Path, root: str | Path, check_pdf: bool = False, strict_pdf: bool = False) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    data = load_sequence(sequence_path)
    root_path = Path(root)

    for entry in _active_entries(data):
        expected_doi = entry.get("doi")
        if not isinstance(expected_doi, str):
            errors.append(f"{entry.get('short_title')}: missing sequence DOI")
            continue
        for field in ["two_column_html", "single_column_html"]:
            rel = entry.get(field)
            if not rel:
                continue
            _check_html_file(root_path / rel, expected_doi, entry, errors, warnings, check_pages=(field == "two_column_html"))
        if check_pdf and entry.get("pdf"):
            _check_pdf(root_path / entry["pdf"], expected_doi, entry, errors, warnings, strict_pdf)

    return {"ok": not errors, "errors": errors, "warnings": warnings}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sequence", required=True)
    parser.add_argument("--root", required=True)
    parser.add_argument("--check-pdf", action="store_true")
    parser.add_argument("--strict-pdf", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    report = audit_sequence_outputs(args.sequence, args.root, check_pdf=args.check_pdf, strict_pdf=args.strict_pdf)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        for error in report["errors"]:
            print(f"ERROR: {error}")
        for warning in report["warnings"]:
            print(f"WARNING: {warning}")
        print("PASS" if report["ok"] else "FAIL")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
