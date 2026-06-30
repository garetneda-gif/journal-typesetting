#!/usr/bin/env python3
"""Maintain the MedBA issue DOI/page sequence table."""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DOI_SUFFIX_RE = re.compile(r"^mbam(\d{2,})$")
DEFAULT_PREFIX = "10.65079"


class SequenceError(ValueError):
    """Raised when the sequence table cannot be updated safely."""


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def load_sequence(path: str | Path) -> dict[str, Any]:
    p = Path(path)
    with p.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise SequenceError("sequence root must be a JSON object")
    return data


def _prefix(data: dict[str, Any]) -> str:
    prefix = data.get("doi_prefix") or DEFAULT_PREFIX
    return str(prefix).rstrip("/")


def _suffix_number(suffix: Any) -> int | None:
    if not isinstance(suffix, str):
        return None
    m = DOI_SUFFIX_RE.match(suffix)
    return int(m.group(1)) if m else None


def _active_entries(data: dict[str, Any]) -> list[dict[str, Any]]:
    return [e for e in data.get("entries", []) if e.get("status", "active") == "active"]


def _sort_key(entry: dict[str, Any]) -> tuple[int, int, str]:
    suffix_num = _suffix_number(entry.get("doi_suffix"))
    order = entry.get("order")
    if not isinstance(order, int):
        order = suffix_num if suffix_num is not None else 999999
    page_start = entry.get("page_start")
    if not isinstance(page_start, int):
        page_start = 999999
    return (page_start, order, str(entry.get("short_title") or ""))


def validate_sequence(data: dict[str, Any], root: str | Path | None = None) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []

    if not isinstance(data, dict):
        return {"ok": False, "errors": ["sequence root must be a JSON object"], "warnings": []}
    if not data.get("issue"):
        errors.append("missing issue")
    if not data.get("doi_prefix"):
        errors.append("missing doi_prefix")
    entries = data.get("entries")
    if not isinstance(entries, list):
        errors.append("entries must be a list")
        return {"ok": False, "errors": errors, "warnings": warnings}

    prefix = _prefix(data)
    seen_doi: dict[str, str] = {}
    seen_suffix: dict[str, str] = {}
    active = _active_entries(data)

    for idx, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"entry {idx} must be an object")
            continue
        label = entry.get("short_title") or f"entry {idx}"
        status = entry.get("status", "active")
        if status not in {"active", "needs_doi_assignment", "archived", "draft"}:
            warnings.append(f"{label}: unknown status {status!r}")
        if status != "active":
            continue

        suffix = entry.get("doi_suffix")
        doi = entry.get("doi")
        if not isinstance(suffix, str) or not DOI_SUFFIX_RE.match(suffix):
            errors.append(f"{label}: invalid doi_suffix {suffix!r}")
            continue
        expected_doi = f"{prefix}/{suffix}"
        if doi != expected_doi:
            errors.append(f"{label}: doi must be {expected_doi}, got {doi!r}")
        if suffix in seen_suffix:
            errors.append(f"duplicate doi_suffix {suffix}: {seen_suffix[suffix]} and {label}")
        seen_suffix[suffix] = str(label)
        if isinstance(doi, str):
            if doi in seen_doi:
                errors.append(f"duplicate doi {doi}: {seen_doi[doi]} and {label}")
            seen_doi[doi] = str(label)

        for field in ["page_start", "page_end", "page_count"]:
            if not isinstance(entry.get(field), int):
                errors.append(f"{label}: {field} must be an integer")
        if all(isinstance(entry.get(f), int) for f in ["page_start", "page_end", "page_count"]):
            if entry["page_end"] < entry["page_start"]:
                errors.append(f"{label}: page_end must be >= page_start")
            expected_count = entry["page_end"] - entry["page_start"] + 1
            if entry["page_count"] != expected_count:
                errors.append(f"{label}: page_count must be {expected_count}, got {entry['page_count']}")

    active_sorted = sorted(active, key=_sort_key)
    previous_end = None
    previous_label = None
    for entry in active_sorted:
        start = entry.get("page_start")
        end = entry.get("page_end")
        label = entry.get("short_title") or entry.get("doi_suffix") or "unknown"
        if not isinstance(start, int) or not isinstance(end, int):
            continue
        if previous_end is not None and start != previous_end + 1:
            errors.append(
                f"active pages are not continuous: {previous_label} ends at {previous_end}, {label} starts at {start}"
            )
        previous_end = end
        previous_label = label

    if root is not None:
        root_path = Path(root)
        for entry in active:
            label = entry.get("short_title") or entry.get("doi_suffix") or "unknown"
            for field in ["two_column_html", "single_column_html", "pdf"]:
                rel = entry.get(field)
                if rel:
                    path = root_path / rel
                    if not path.exists():
                        warnings.append(f"{label}: declared {field} missing at {rel}")

    return {"ok": not errors, "errors": errors, "warnings": warnings}


def next_entry(data: dict[str, Any], short_title: str, page_count: int) -> dict[str, Any]:
    if page_count < 1:
        raise SequenceError("page_count must be >= 1")
    entries = data.get("entries", [])
    active = _active_entries(data)
    suffix_nums = [_suffix_number(e.get("doi_suffix")) for e in entries]
    suffix_nums = [n for n in suffix_nums if n is not None]
    next_num = (max(suffix_nums) + 1) if suffix_nums else 1
    suffix = f"mbam{next_num:02d}"
    if any(e.get("doi_suffix") == suffix for e in entries):
        raise SequenceError(f"doi_suffix already exists: {suffix}")

    starts = [e.get("page_end") for e in active if isinstance(e.get("page_end"), int)]
    page_start = (max(starts) + 1) if starts else 1
    page_end = page_start + page_count - 1
    folder = f"{suffix}-{short_title}"
    prefix = _prefix(data)
    return {
        "order": next_num,
        "short_title": short_title,
        "doi_suffix": suffix,
        "doi": f"{prefix}/{suffix}",
        "page_start": page_start,
        "page_end": page_end,
        "page_count": page_count,
        "two_column_html": f"{folder}/two-column-{short_title}.html",
        "single_column_html": f"{folder}/single-column-{short_title}.html",
        "pdf": f"{folder}/two-column-{short_title}.pdf",
        "status": "active",
        "notes": "",
        "folder": folder,
    }


def _touch(data: dict[str, Any]) -> dict[str, Any]:
    data["last_updated"] = now_iso()
    return data


def assign_entry(data: dict[str, Any], short_title: str, page_count: int) -> dict[str, Any]:
    updated = copy.deepcopy(data)
    if any(e.get("short_title") == short_title and e.get("status") == "active" for e in updated.get("entries", [])):
        raise SequenceError(f"active entry already exists for short_title: {short_title}")
    updated.setdefault("entries", []).append(next_entry(updated, short_title, page_count))
    report = validate_sequence(updated)
    if not report["ok"]:
        raise SequenceError("; ".join(report["errors"]))
    return _touch(updated)


def activate_entry(data: dict[str, Any], short_title: str, doi_suffix: str, page_count: int) -> dict[str, Any]:
    if not DOI_SUFFIX_RE.match(doi_suffix):
        raise SequenceError(f"invalid doi_suffix: {doi_suffix}")
    if page_count < 1:
        raise SequenceError("page_count must be >= 1")
    updated = copy.deepcopy(data)
    entries = updated.setdefault("entries", [])
    matching = [e for e in entries if e.get("short_title") == short_title]
    if not matching:
        raise SequenceError(f"no entry found for short_title: {short_title}")
    target = matching[0]
    if target.get("status") == "active" and target.get("doi_suffix") != doi_suffix:
        raise SequenceError(f"active entry already has different doi_suffix: {target.get('doi_suffix')}")
    for entry in entries:
        if entry is not target and entry.get("doi_suffix") == doi_suffix:
            raise SequenceError(f"doi_suffix already exists: {doi_suffix}")

    active = [e for e in entries if e is not target and e.get("status") == "active"]
    previous_ends = [e.get("page_end") for e in active if isinstance(e.get("page_end"), int)]
    page_start = (max(previous_ends) + 1) if previous_ends else 1
    page_end = page_start + page_count - 1
    folder = f"{doi_suffix}-{short_title}"
    target.update(
        {
            "order": _suffix_number(doi_suffix),
            "doi_suffix": doi_suffix,
            "doi": f"{_prefix(updated)}/{doi_suffix}",
            "page_start": page_start,
            "page_end": page_end,
            "page_count": page_count,
            "two_column_html": f"{folder}/two-column-{short_title}.html",
            "single_column_html": f"{folder}/single-column-{short_title}.html",
            "pdf": f"{folder}/two-column-{short_title}.pdf",
            "status": "active",
            "folder": folder,
        }
    )
    report = validate_sequence(updated)
    if not report["ok"]:
        raise SequenceError("; ".join(report["errors"]))
    return _touch(updated)


def update_pages(data: dict[str, Any], doi_suffix: str, page_count: int) -> dict[str, Any]:
    if page_count < 1:
        raise SequenceError("page_count must be >= 1")
    updated = copy.deepcopy(data)
    active_sorted = sorted(_active_entries(updated), key=lambda e: (_suffix_number(e.get("doi_suffix")) or 999999))
    target_index = None
    for idx, entry in enumerate(active_sorted):
        if entry.get("doi_suffix") == doi_suffix:
            target_index = idx
            break
    if target_index is None:
        raise SequenceError(f"active doi_suffix not found: {doi_suffix}")

    target = active_sorted[target_index]
    target["page_count"] = page_count
    target["page_end"] = target["page_start"] + page_count - 1
    previous_end = target["page_end"]
    for entry in active_sorted[target_index + 1 :]:
        entry["page_start"] = previous_end + 1
        entry["page_end"] = entry["page_start"] + entry["page_count"] - 1
        previous_end = entry["page_end"]

    report = validate_sequence(updated)
    if not report["ok"]:
        raise SequenceError("; ".join(report["errors"]))
    return _touch(updated)


def atomic_write_json(path: str | Path, data: dict[str, Any]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_name(p.name + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    json.loads(tmp.read_text(encoding="utf-8"))
    tmp.replace(p)


def _print_json(payload: Any) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    def add_sequence_arg(p: argparse.ArgumentParser) -> None:
        p.add_argument("--sequence", required=True, help="Path to medba-issue-sequence.json")

    p_validate = sub.add_parser("validate")
    add_sequence_arg(p_validate)
    p_validate.add_argument("--root")

    p_next = sub.add_parser("next")
    add_sequence_arg(p_next)
    p_next.add_argument("--short-title", required=True)
    p_next.add_argument("--page-count", type=int, required=True)

    p_assign = sub.add_parser("assign")
    add_sequence_arg(p_assign)
    p_assign.add_argument("--short-title", required=True)
    p_assign.add_argument("--page-count", type=int, required=True)
    p_assign.add_argument("--write", action="store_true")

    p_activate = sub.add_parser("activate")
    add_sequence_arg(p_activate)
    p_activate.add_argument("--short-title", required=True)
    p_activate.add_argument("--doi-suffix", required=True)
    p_activate.add_argument("--page-count", type=int, required=True)
    p_activate.add_argument("--write", action="store_true")

    p_update = sub.add_parser("update-pages")
    add_sequence_arg(p_update)
    p_update.add_argument("--doi-suffix", required=True)
    p_update.add_argument("--page-count", type=int, required=True)
    p_update.add_argument("--write", action="store_true")

    args = parser.parse_args(argv)
    try:
        data = load_sequence(args.sequence)
        if args.command == "validate":
            report = validate_sequence(data, root=args.root)
            _print_json(report)
            return 0 if report["ok"] else 1
        if args.command == "next":
            _print_json(next_entry(data, args.short_title, args.page_count))
            return 0
        if args.command == "assign":
            updated = assign_entry(data, args.short_title, args.page_count)
        elif args.command == "activate":
            updated = activate_entry(data, args.short_title, args.doi_suffix, args.page_count)
        elif args.command == "update-pages":
            updated = update_pages(data, args.doi_suffix, args.page_count)
        else:
            parser.error("unknown command")
            return 2

        if args.write:
            atomic_write_json(args.sequence, updated)
            _print_json({"ok": True, "written": args.sequence})
        else:
            _print_json(updated)
        return 0
    except (OSError, json.JSONDecodeError, SequenceError) as exc:
        _print_json({"ok": False, "errors": [str(exc)], "warnings": []})
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
