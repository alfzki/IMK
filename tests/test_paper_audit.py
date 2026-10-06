"""
Tests for Scientific Paper Auditor & Fact-Checker (audit_paper_draft.py).
Verifies claim grounding, SIMPUS skripsi blocking, bibliography integrity,
AI style checking, and empirical metric reconciliation.
"""

import unittest
import tempfile
from pathlib import Path
import pandas as pd

from scripts.audit_paper_draft import (
    audit_document,
    load_verified_database,
    is_thesis_or_simpus_citation,
    find_citations_in_sentence,
    check_bibliography_entries
)


class TestPaperAuditor(unittest.TestCase):

    def setUp(self):
        self.db = load_verified_database()

    def test_simpus_thesis_citation_detection(self):
        # Must detect SIMPus or skripsi mentions in citation context
        self.assertTrue(is_thesis_or_simpus_citation("Skripsi STIS (2024)", "Penelitian terdahulu menggunakan model Fasih [Skripsi STIS 2024]."))
        self.assertTrue(is_thesis_or_simpus_citation("Rayhan, 2024", "Studi ini merujuk pada https://simpus.stis.ac.id/repositori/12345."))
        self.assertFalse(is_thesis_or_simpus_citation("Hassan dkk., 2024", "Studi Hassan dkk. (2024) membandingkan model supervised learning."))

    def test_bibliography_integrity_simpus_disallowed(self):
        bib_with_skripsi = """
## DAFTAR PUSTAKA

Hassan, A.A., Muse, A.H., Chesneau, C. (2024). Machine learning study using 2020 SDHS data. Scientific Reports, 14, 1-15. https://doi.org/10.1038/s41598-024-56466-8

Desy, A.F. (2024). Analisis Penerimaan Penggunaan Aplikasi Fasih. Skripsi Sarjana Terapan Komputasi Statistik, Politeknik Statistika STIS. https://simpus.stis.ac.id/repositori/a9d9f7cd
"""
        res = check_bibliography_entries(bib_with_skripsi, self.db)
        self.assertEqual(len(res["disallowed_theses"]), 1)
        self.assertTrue(any(issue["type"] == "SIMPUS_THESIS_DISALLOWED" for issue in res["issues"]))

    def test_audit_document_simpus_violation(self):
        draft_content = """# Judul Artikel Ilmiah Evaluasi Usability Sistem Informasi

## ABSTRAK
Penelitian ini mengevaluasi usabilitas antarmuka sistem informasi dengan instrumen WebQual 4.0 dan pendekatan User-Centered Design.

## PENDAHULUAN
Penerapan antarmuka sistem informasi pada layanan publik menghadapi tantangan kemudahan penggunaan.
Berdasarkan temuan skripsi terdahulu (Skripsi STIS, 2024), akurasi model konvensional mencapai 85%.

## DAFTAR PUSTAKA
[1] Skripsi STIS (2024). Sistem Pengawasan Lapangan BPS. Politeknik Statistika STIS. https://simpus.stis.ac.id/repositori/123
"""
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
            f.write(draft_content)
            temp_path = Path(f.name)

        try:
            report = audit_document(temp_path)
            self.assertEqual(report["status"], "FAILED")
            self.assertGreater(report["disallowed_simpus_theses"], 0)
        finally:
            if temp_path.exists():
                temp_path.unlink()

    def test_audit_document_ai_cliche_detection(self):
        draft_content = """# Artikel Penelitian

## ABSTRAK
Uji coba algoritma klasifikasi.

## PENDAHULUAN
Di era modern ini, kita perlu menyelami interaksi rumit antar variabel prediktor untuk mendongkrak sensitivitas model.
Hasil eksperimen menjadi bukti nyata dari keunggulan metode ini — yang dirancang secara terpisah — dalam klasifikasi.

## KESIMPULAN
- Poin kesimpulan pertama
- Poin kesimpulan kedua
"""
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
            f.write(draft_content)
            temp_path = Path(f.name)

        try:
            report = audit_document(temp_path)
            self.assertEqual(report["status"], "FAILED")
            # Should flag AI cliches: 'di era modern ini', 'menyelami', 'bukti nyata', 'mendongkrak'
            self.assertGreater(report["ai_cliches_count"], 2)
            # Should flag improper em dash spacing
            self.assertTrue(len(report["em_dash_issues"]) > 0)
        finally:
            if temp_path.exists():
                temp_path.unlink()

    def test_simpus_thesis_citekey_and_database_detection(self):
        # Must detect SIMPus citekeys from theses_archive.bib even without keyword 'skripsi'
        self.assertTrue(is_thesis_or_simpus_citation("Desy2024Penerimaan", "Berdasarkan studi Fasih [Desy2024Penerimaan], adopsi teknologi dievaluasi."))
        self.assertTrue(is_thesis_or_simpus_citation("Rayhan2024Vulnerability", "Uji penetrasi RESTful API dilakukan oleh Rayhan (2024)."))

    def test_empirical_numbers_reconciliation(self):
        from scripts.audit_paper_draft import audit_empirical_numbers
        metrics_dict = {
            "pr_auc": 0.8816,
            "roc_auc": 0.9402,
            "accuracy_opt": 0.8750,
            "f1_opt": 0.8252
        }
        # Matching text should have 0 discrepancies
        clean_text = "Model menghasilkan PR-AUC 0.8816 dan ROC-AUC 0.9402 dengan Akurasi 87.50% serta F1 0.8252."
        disc = audit_empirical_numbers(clean_text, metrics_dict)
        self.assertEqual(len(disc), 0)

        # Mismatched text should be caught
        bad_text = "Model menghasilkan PR-AUC 0.6510 dan ROC-AUC 0.7200."
        disc_bad = audit_empirical_numbers(bad_text, metrics_dict)
        self.assertEqual(len(disc_bad), 2)


if __name__ == "__main__":
    unittest.main()

