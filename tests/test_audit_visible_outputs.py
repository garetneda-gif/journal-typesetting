import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import audit_visible_outputs


class AuditVisibleOutputsTest(unittest.TestCase):
    def make_article(self, root, folder="mbam05-GERD-LBN-Mendelian-Randomization"):
        article = Path(root) / folder
        article.mkdir()
        short = folder.split("-", 1)[1]
        (article / f"two-column-{short}.html").write_text("two", encoding="utf-8")
        (article / f"single-column-{short}.html").write_text("single", encoding="utf-8")
        (article / ".source").mkdir()
        (article / ".source" / "source.docx").write_text("hidden", encoding="utf-8")
        return article, short

    def test_allows_only_single_and_two_column_html_by_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.make_article(tmp)
            report = audit_visible_outputs.audit_root(Path(tmp))
            self.assertTrue(report["ok"], report)
            self.assertEqual(report["unexpected"], [])

    def test_rejects_unexpected_visible_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            article, _ = self.make_article(tmp)
            (article / "debug-preview.html").write_text("debug", encoding="utf-8")
            report = audit_visible_outputs.audit_root(Path(tmp))
            self.assertFalse(report["ok"])
            self.assertTrue(any("debug-preview.html" in item["path"] for item in report["unexpected"]))

    def test_pdf_requires_allow_pdf(self):
        with tempfile.TemporaryDirectory() as tmp:
            article, _ = self.make_article(tmp)
            (article / "10.65079:mbam05.pdf").write_text("pdf", encoding="utf-8")
            self.assertFalse(audit_visible_outputs.audit_root(Path(tmp))["ok"])
            self.assertTrue(audit_visible_outputs.audit_root(Path(tmp), allow_pdf=True)["ok"])

    def test_ignores_root_housekeeping(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.make_article(tmp)
            for name in [".logs", ".sequence", ".reference", ".incoming"]:
                (Path(tmp) / name).mkdir()
            (Path(tmp) / ".DS_Store").write_text("", encoding="utf-8")
            report = audit_visible_outputs.audit_root(Path(tmp))
            self.assertTrue(report["ok"], report)


if __name__ == "__main__":
    unittest.main()
