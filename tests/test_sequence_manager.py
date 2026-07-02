import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("sequence_manager", ROOT / "scripts" / "sequence_manager.py")
assert SPEC is not None and SPEC.loader is not None
sequence_manager = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(sequence_manager)


def sample_sequence() -> dict[str, Any]:
    return {
        "issue": "MedBA Medicine working sequence",
        "doi_prefix": "10.65079",
        "last_updated": "2026-06-30T10:00:00+08:00",
        "entries": [
            {
                "order": 4,
                "short_title": "WAA-Anorectal-Scoping-Review",
                "doi_suffix": "mbam04",
                "doi": "10.65079/mbam04",
                "page_start": 40,
                "page_end": 49,
                "page_count": 10,
                "two_column_html": "mbam04-WAA-Anorectal-Scoping-Review/two-column-WAA-Anorectal-Scoping-Review.html",
                "single_column_html": None,
                "pdf": "mbam04-WAA-Anorectal-Scoping-Review/10.65079/mbam04.pdf",
                "status": "active",
                "folder": "mbam04-WAA-Anorectal-Scoping-Review",
                "notes": "",
            },
            {
                "order": 5,
                "short_title": "GERD-LBN-Mendelian-Randomization",
                "doi_suffix": "mbam05",
                "doi": "10.65079/mbam05",
                "page_start": 50,
                "page_end": 54,
                "page_count": 5,
                "two_column_html": "mbam05-GERD-LBN-Mendelian-Randomization/two-column-GERD-LBN-Mendelian-Randomization.html",
                "single_column_html": "mbam05-GERD-LBN-Mendelian-Randomization/single-column-GERD-LBN-Mendelian-Randomization.html",
                "pdf": "mbam05-GERD-LBN-Mendelian-Randomization/10.65079/mbam05.pdf",
                "status": "active",
                "folder": "mbam05-GERD-LBN-Mendelian-Randomization",
                "notes": "",
            },
        ],
    }


class SequenceManagerTest(unittest.TestCase):
    def test_next_entry_uses_max_doi_and_page_end(self):
        entry = sequence_manager.next_entry(sample_sequence(), "RRM2-Cervical-Cancer", 7)
        self.assertEqual(entry["doi_suffix"], "mbam06")
        self.assertEqual(entry["doi"], "10.65079/mbam06")
        self.assertEqual(entry["page_start"], 55)
        self.assertEqual(entry["page_end"], 61)
        self.assertEqual(entry["folder"], "mbam06-RRM2-Cervical-Cancer")
        self.assertEqual(entry["pdf"], "mbam06-RRM2-Cervical-Cancer/10.65079/mbam06.pdf")

    def test_validate_rejects_duplicate_doi(self):
        data = sample_sequence()
        duplicate = dict(data["entries"][1])
        duplicate["short_title"] = "Duplicate"
        data["entries"].append(duplicate)
        report = sequence_manager.validate_sequence(data)
        self.assertFalse(report["ok"])
        self.assertTrue(any("duplicate doi" in error.lower() for error in report["errors"]))

    def test_validate_rejects_page_overlap(self):
        data = sample_sequence()
        data["entries"][1]["page_start"] = 49
        data["entries"][1]["page_end"] = 53
        report = sequence_manager.validate_sequence(data)
        self.assertFalse(report["ok"])
        self.assertTrue(any("page" in error.lower() and "continuous" in error.lower() for error in report["errors"]))

    def test_activate_needs_doi_assignment(self):
        data = sample_sequence()
        data["entries"].append({
            "order": None,
            "short_title": "Pending-Article",
            "doi_suffix": None,
            "doi": None,
            "page_start": None,
            "page_end": None,
            "page_count": None,
            "two_column_html": "Pending-Article/two-column-Pending-Article.html",
            "single_column_html": "Pending-Article/single-column-Pending-Article.html",
            "pdf": None,
            "status": "needs_doi_assignment",
            "folder": "Pending-Article",
            "notes": "",
        })
        updated = sequence_manager.activate_entry(data, "Pending-Article", "mbam06", 4)
        entry = next(e for e in updated["entries"] if e["short_title"] == "Pending-Article")
        self.assertEqual(entry["status"], "active")
        self.assertEqual(entry["doi"], "10.65079/mbam06")
        self.assertEqual(entry["page_start"], 55)
        self.assertEqual(entry["page_end"], 58)
        self.assertEqual(entry["folder"], "mbam06-Pending-Article")
        self.assertEqual(entry["pdf"], "mbam06-Pending-Article/10.65079/mbam06.pdf")

    def test_update_pages_shifts_later_entries(self):
        data = sample_sequence()
        updated = sequence_manager.assign_entry(data, "RRM2-Cervical-Cancer", 7)
        shifted = sequence_manager.update_pages(updated, "mbam05", 6)
        mbam05 = next(e for e in shifted["entries"] if e["doi_suffix"] == "mbam05")
        mbam06 = next(e for e in shifted["entries"] if e["doi_suffix"] == "mbam06")
        self.assertEqual((mbam05["page_start"], mbam05["page_end"]), (50, 55))
        self.assertEqual((mbam06["page_start"], mbam06["page_end"]), (56, 62))

    def test_atomic_write_json_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sequence.json"
            sequence_manager.atomic_write_json(path, sample_sequence())
            self.assertTrue(path.exists())
            self.assertFalse(path.with_suffix(path.suffix + ".tmp").exists())
            loaded = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(loaded["doi_prefix"], "10.65079")


if __name__ == "__main__":
    unittest.main()
