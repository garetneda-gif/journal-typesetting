import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import audit_doi_pages


def make_sequence(root, doi="10.65079/mbam05", page_start=50, page_end=54):
    article = Path(root) / "mbam05-GERD-LBN-Mendelian-Randomization"
    article.mkdir()
    two = article / "two-column-GERD-LBN-Mendelian-Randomization.html"
    single = article / "single-column-GERD-LBN-Mendelian-Randomization.html"
    two.write_text(
        f"<html><body><span>{doi}</span>"
        + "".join(f"<div class='page-number'>{page}</div>" for page in range(page_start, page_end + 1))
        + "</body></html>",
        encoding="utf-8",
    )
    single.write_text(f"<html><body>{doi}</body></html>", encoding="utf-8")
    data = {
        "issue": "MedBA Medicine working sequence",
        "doi_prefix": "10.65079",
        "last_updated": "2026-06-30T10:00:00+08:00",
        "entries": [
            {
                "order": 5,
                "short_title": "GERD-LBN-Mendelian-Randomization",
                "doi_suffix": "mbam05",
                "doi": "10.65079/mbam05",
                "page_start": page_start,
                "page_end": page_end,
                "page_count": page_end - page_start + 1,
                "two_column_html": "mbam05-GERD-LBN-Mendelian-Randomization/two-column-GERD-LBN-Mendelian-Randomization.html",
                "single_column_html": "mbam05-GERD-LBN-Mendelian-Randomization/single-column-GERD-LBN-Mendelian-Randomization.html",
                "pdf": None,
                "status": "active",
                "folder": "mbam05-GERD-LBN-Mendelian-Randomization",
                "notes": "",
            }
        ],
    }
    seq = Path(root) / "sequence.json"
    seq.write_text(json.dumps(data), encoding="utf-8")
    return seq


class AuditDoiPagesTest(unittest.TestCase):
    def test_valid_html_doi_and_pages_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            seq = make_sequence(tmp)
            report = audit_doi_pages.audit_sequence_outputs(seq, Path(tmp))
            self.assertTrue(report["ok"], report)

    def test_rejects_double_slash_doi(self):
        with tempfile.TemporaryDirectory() as tmp:
            seq = make_sequence(tmp, doi="10.65079//mbam05")
            report = audit_doi_pages.audit_sequence_outputs(seq, Path(tmp))
            self.assertFalse(report["ok"])
            self.assertTrue(any("malformed" in e.lower() for e in report["errors"]))

    def test_rejects_missing_exact_doi(self):
        with tempfile.TemporaryDirectory() as tmp:
            seq = make_sequence(tmp, doi="10.65079/mbam06")
            report = audit_doi_pages.audit_sequence_outputs(seq, Path(tmp))
            self.assertFalse(report["ok"])
            self.assertTrue(any("missing expected doi" in e.lower() for e in report["errors"]))

    def test_rejects_page_footer_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            seq = make_sequence(tmp, page_start=50, page_end=54)
            two = Path(tmp) / "mbam05-GERD-LBN-Mendelian-Randomization" / "two-column-GERD-LBN-Mendelian-Randomization.html"
            two.write_text("<html><body>10.65079/mbam05<div class='page-number'>50</div></body></html>", encoding="utf-8")
            report = audit_doi_pages.audit_sequence_outputs(seq, Path(tmp))
            self.assertFalse(report["ok"])
            self.assertTrue(any("page footer" in e.lower() for e in report["errors"]))


if __name__ == "__main__":
    unittest.main()
