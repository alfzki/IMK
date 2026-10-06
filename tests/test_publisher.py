"""Unit tests for Document Publishing & Compilation Pipeline (Template Validation, Citations, IEEE Docx)."""

import tempfile
import unittest
from pathlib import Path

from calm_carson.publisher import (
    BibliographyItem,
    CitationValidator,
    DocumentConverter,
    DocumentPublisher,
    IEEEBibliographyRenderer,
    PublicationConfig,
    TemplateValidator,
    ValidationSeverity,
)


class TestPublisher(unittest.TestCase):
    """Test suite for the publishing pipeline components."""

    def setUp(self):
        self.sample_compliant_markdown = """# RANCANG BANGUN SISTEM VALIDASI SURVEI LAPANGAN BPS

## Ringkasan
Penelitian ini mengembangkan artefak backend berbasis machine learning untuk memitigasi anomali data entri survei BPS. Sistem mengintegrasikan verifikasi kriptografis dan evaluasi ISO 25010.

Kata Kunci: CAPI, curbstoning, isolation forest, paradata, integrity

## I. Latar Belakang Masalah
Akurasi data statistik resmi merupakan landasan utama perumusan kebijakan publik [1]. Namun kegiatan lapangan menghadapi tiga permasalahan konkret:

### 1. Skala Masif Mitra Non-Organik dan Risiko Falsifikasi
BPS merekrut sekitar 190.000 petugas lapangan pada Sensus Pertanian 2023 [1]. Pemalsuan data tercatat mencapai 3% hingga 15% dari total sampel [2].

### 2. Keterbatasan Kapasitas Verifikasi Fisik Pengawas Lapangan
PML hanya mampu melakukan verifikasi ulang sebesar 5% hingga 10% [3].

### 3. Anomali Durasi Pengisian Kuesioner
Wawancara memakan waktu 45 hingga 75 menit, namun pencacah nakal memangkas waktu hingga lebih dari 60% [4].

## II. Rumusan Masalah
Bagaimana merancang backend deteksi anomali real-time untuk mitigasi kecurangan survei?

## III. Tujuan Penelitian
Mengembangkan arsitektur microservices untuk mendeteksi curbstoning pada aplikasi CAPI BPS.

## IV. Tinjauan Pustaka
Pengumpulan data CAPI memegang peranan krusial dalam GSBPM [1].

**TABEL I**  
**TABEL KONTRIBUSI PENELITIAN**

| Penulis | Tujuan | Metode | Variabel |
| :--- | :--- | :--- | :--- |
| Olbrich dkk. [2] | Deteksi fraud | Multilevel | Waktu |
| Penelitian ini | Deteksi real-time | Isolation Forest | HMAC & Dwell-Time |

Penelitian ini mengisi kesenjangan penelitian sebelumnya dengan pendekatan real-time streaming.

## V. Metodologi Penelitian
Penelitian menerapkan 6 tahapan Design Science Research Methodology (DSRM) [5].

**TABEL II**  
**RANCANGAN JADWAL PENELITIAN**

| No | Kegiatan | Bulan 1 | Bulan 2 | Bulan 10 |
| :-: | :--- | :-: | :-: | :-: |
| 1 | Analisis Kebutuhan | X | | |
| 2 | Pengembangan Sistem | | X | X |

## VI. Daftar Pustaka
[1] S. Schwanhäuser, "How to catch a falsifier," Public Opinion Quarterly, 2021.  
[2] L. Olbrich, "Detecting interviewer fraud," JSSAM, 2023.  
[3] SOP Pengawasan BPS, Jakarta: BPS RI, 2023.  
[4] P. Schenk, "Algorithmic fairness," AStA, 2024.  
[5] K. Peffers, "A design science research methodology," JMIS, 2007.
"""

    def test_template_validator_compliant_proposal(self):
        """Test template validation against a compliant proposal manuscript."""
        validator = TemplateValidator()
        report = validator.validate(self.sample_compliant_markdown, scope="proposal")

        self.assertTrue(report.is_compliant)
        self.assertGreaterEqual(report.compliance_score, 75.0)
        self.assertEqual(report.error_count, 0)
        self.assertTrue(report.metadata.get("has_abstract"))
        self.assertEqual(report.metadata.get("keywords_count"), 5)

    def test_template_validator_missing_sections(self):
        """Test template validation when critical sections are missing."""
        bad_markdown = """# PROPOSAL TANPA STRUKTUR LENGKAP
Teks singkat tanpa abstrak dan tanpa bab metodologi atau daftar pustaka.
"""
        validator = TemplateValidator()
        report = validator.validate(bad_markdown, scope="proposal")

        self.assertFalse(report.is_compliant)
        self.assertLess(report.compliance_score, 70.0)
        self.assertGreater(report.error_count, 0)

        # Check missing abstract issue
        issue_codes = [iss.code for iss in report.issues]
        self.assertIn("MISSING_ABSTRACT", issue_codes)
        self.assertIn("MISSING_SECTION_BAB_2_TINJAUAN_PUSTAKA", issue_codes)

    def test_citation_validator_matching_and_broken(self):
        """Test citation extraction, matching, and broken citation detection."""
        validator = CitationValidator()

        # Text with valid inline citations [1], [2] and broken citation [99]
        text = "Menurut studi [1], [2], dan rujukan fiktif [99], anomali terdeteksi [1]-[3]."
        report = validator.validate(text)

        self.assertIn("99", report.missing_citations)
        self.assertFalse(report.is_valid)
        self.assertGreater(report.error_count, 0)

    def test_citation_validator_disallowed_thesis(self):
        """Test that CitationValidator flags disallowed SIMPUS/theses citations."""
        validator = CitationValidator(bib_path="literature/non_existent.bib")
        text = """Menurut studi [1], sistem bekerja baik.

## DAFTAR PUSTAKA
[1] F. A. Fauzi, "Penerimaan Sistem Informasi Menggunakan TAM (Skripsi Sarjana Terapan)", Politeknik Statistika STIS, https://simpus.stis.ac.id/repositori/123, 2024.
"""
        report = validator.validate(text)
        issue_codes = [iss.code for iss in report.issues]
        self.assertIn("DISALLOWED_THESIS", issue_codes)
        self.assertFalse(report.is_valid)

    def test_ieee_bibliography_renderer_formats(self):
        """Test IEEE reference formatting for journals, books, conferences, and theses."""
        renderer = IEEEBibliographyRenderer()

        # Journal Article
        journal_item = BibliographyItem(
            key="schwan2021",
            entry_type="article",
            title="How to Catch a Falsifier",
            authors=["S. Schwanhäuser", "J. W. Sakshaug", "Y. Kosyakova"],
            venue="Public Opinion Quarterly",
            volume="86",
            number_issue="1",
            pages="51-77",
            year=2021,
            doi="10.1093/poq/nfab066",
        )
        j_str = renderer.format_ieee_reference(journal_item, number=1)
        self.assertIn("[1]", j_str)
        self.assertIn("How to Catch a Falsifier", j_str)
        self.assertIn("Public Opinion Quarterly", j_str)
        self.assertIn("vol. 86", j_str)
        self.assertIn("doi: 10.1093/poq/nfab066", j_str)

        # Skripsi / Thesis
        thesis_item = BibliographyItem(
            key="rayhan2024",
            entry_type="mastersthesis",
            title="Vulnerability Assessment and Penetration Testing RESTful API",
            authors=["Rayhan Zaki Abrar"],
            school="Politeknik Statistika STIS",
            year=2024,
            url="https://simpus.stis.ac.id/repositori/fab3ff94",
        )
        t_str = renderer.format_ieee_reference(thesis_item, number=2)
        self.assertIn("[2]", t_str)
        self.assertIn("R. Z. Abrar", t_str)
        self.assertIn("Skripsi Sarjana Terapan", t_str)
        self.assertIn("Politeknik Statistika STIS", t_str)

    def test_citation_renumbering_engine(self):
        """Test chronological citation renumbering and ordering."""
        renderer = IEEEBibliographyRenderer()
        bib_entries = {
            "10": BibliographyItem(key="10", title="Ref Ten"),
            "20": BibliographyItem(key="20", title="Ref Twenty"),
        }
        # Out-of-order text where [20] appears before [10]
        text = "Paragraf awal mengutip [20]. Paragraf kedua mengutip [10].\n\n## DAFTAR PUSTAKA\n[10] Ref Ten\n[20] Ref Twenty"

        renumbered_text, ordered_bib = renderer.renumber_manuscript_citations(text, bib_entries)

        # In renumbered text, [20] should become [1], and [10] should become [2]
        self.assertIn("mengutip [1]", renumbered_text)
        self.assertIn("mengutip [2]", renumbered_text)
        self.assertEqual(ordered_bib[0][0], 1)
        self.assertEqual(ordered_bib[0][1].key, "20")
        self.assertEqual(ordered_bib[1][0], 2)
        self.assertEqual(ordered_bib[1][1].key, "10")

    def test_document_converter_docx_generation(self):
        """Test Markdown to Word DOCX conversion with IEEE formatting."""
        converter = DocumentConverter()
        with tempfile.TemporaryDirectory() as tmp_dir:
            out_docx = Path(tmp_dir) / "test_output.docx"
            result_path = converter.convert_to_docx(
                markdown_text=self.sample_compliant_markdown,
                output_docx_path=str(out_docx),
            )
            self.assertTrue(Path(result_path).exists())
            self.assertGreater(Path(result_path).stat().st_size, 5000)

            # Check that LibreOffice can convert it to PDF
            out_pdf = Path(tmp_dir) / "test_output.pdf"
            pdf_result = converter.convert_to_pdf(result_path, str(out_pdf))
            if pdf_result:
                self.assertTrue(Path(pdf_result).exists())
                self.assertGreater(Path(pdf_result).stat().st_size, 1000)

    def test_end_to_end_publisher_engine(self):
        """Test end-to-end DocumentPublisher workflow execution."""
        publisher = DocumentPublisher()
        with tempfile.TemporaryDirectory() as tmp_dir:
            cfg = PublicationConfig(
                output_dir=tmp_dir,
                output_format="docx",
                base_filename="e2e_proposal",
                strict_validation=False,
            )
            res = publisher.publish(self.sample_compliant_markdown, "test_manuscript", cfg)

            self.assertTrue(res.success)
            self.assertIsNotNone(res.docx_path)
            self.assertTrue(Path(res.docx_path).exists())
            self.assertIsNotNone(res.template_report)
            self.assertIsNotNone(res.citation_report)


if __name__ == "__main__":
    unittest.main()
