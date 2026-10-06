"""Unit tests for the research gap extraction, synthesis, and topic brainstorming module."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from calm_carson.brainstorm.exporter import BrainstormExporter
from calm_carson.brainstorm.extractor import (
    ResearchGapExtractor,
    classify_topic_cluster,
    split_sentences_id,
)
from calm_carson.brainstorm.models import BrainstormClusterSummary, ResearchGapItem
from calm_carson.brainstorm.synthesizer import BrainstormSynthesizer


class TestBrainstormer(unittest.TestCase):
    """Test suite for research gap analysis and brainstorming module."""

    def test_models_and_cluster_summary(self):
        """Test dataclass serialization and property calculations."""
        item1 = ResearchGapItem(
            id="test_gap_1",
            source_type="stis_thesis",
            source_title="Pengembangan CAPI Survei Pertanian",
            year="2023",
            author="Budi Santoso",
            cluster="data_collection_capi",
            gap_category="future_work",
            raw_excerpt="Saran pada penelitian selanjutnya adalah menambahkan validasi geospasial offline.",
            synthesized_summary="Saran penambahan validasi geospasial.",
            recommended_opportunity="Membangun modul validasi offline pada CAPI.",
            source_location="theses_data.json#1",
        )
        d = item1.to_dict()
        self.assertEqual(d["id"], "test_gap_1")
        self.assertEqual(d["cluster"], "data_collection_capi")

        summary = BrainstormClusterSummary(
            cluster_id="data_collection_capi",
            cluster_name="Pengumpulan Data Cerdas",
            future_works=[item1],
        )
        self.assertEqual(summary.total_items, 1)
        self.assertEqual(len(summary.future_works), 1)
        self.assertIn("cluster_id", summary.to_dict())

    def test_cluster_classification(self):
        """Test classification of titles and text into SIS topic clusters."""
        text_sec = "Vulnerability assessment dan penetration testing RESTful API pada microservice SIPADU-NG."
        self.assertEqual(classify_topic_cluster(text_sec), "security_privacy")

        text_sdi = "Pengembangan API Gateway interoperabilitas Satu Data Indonesia dengan standar SIMETRIS SPBE."
        self.assertEqual(classify_topic_cluster(text_sdi), "sdi_interoperability")

        text_capi = "Aplikasi CAPI survei harga konsumen berbasis mobile Android untuk pencacahan lapangan BPS."
        self.assertEqual(classify_topic_cluster(text_capi), "data_collection_capi")

        text_geo = "Pemetaan tutupan lahan dan RTH berbasis citra satelit Landsat dan WebGIS spasial."
        self.assertEqual(classify_topic_cluster(text_geo), "geospatial")

    def test_sentence_splitting_and_patterns(self):
        """Test sentence splitting on Indonesian academic abstracts."""
        text = (
            "Sistem saat ini masih menggunakan kertas. "
            "Namun sistem yang ada belum sepenuhnya mengakomodasi kebutuhan manajemen pengawasan. "
            "Saran pada penelitian selanjutnya adalah mengembangkan modul notifikasi dan aplikasi Android."
        )
        sentences = split_sentences_id(text)
        self.assertEqual(len(sentences), 3)

    def test_markdown_section_extraction(self):
        """Test extraction of Limitation and Future Work sections from markdown files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmproot = Path(tmpdir)
            md_dir = tmproot / "literature" / "markdowns"
            md_dir.mkdir(parents=True, exist_ok=True)

            md_content = """# Paper Uji Coba Privasi Mikrodata

## 1. Pendahuluan
Penelitian ini menguji privasi pada data sensus.

## 2. Metodologi
Menggunakan algoritma diferensial privasi.

## 3. Limitations of the study
Certain limitations of the current version must be acknowledged. First, the library implements a limited set of mechanisms and does not yet support free-text attributes. Second, computational overhead is high.

## 4. Future Work
For future research, we recommend implementing automated privacy budgeting and GPU acceleration for matrix operations.
"""
            test_md = md_dir / "paper_test.md"
            with open(test_md, "w", encoding="utf-8") as f:
                f.write(md_content)

            extractor = ResearchGapExtractor(workspace_root=tmproot)
            items = extractor.extract_from_markdown_sections(target_dirs=["literature/markdowns"])

            self.assertGreaterEqual(len(items), 2)
            categories = [it.gap_category for it in items]
            self.assertIn("methodological_bottleneck", categories)
            self.assertIn("future_work", categories)

    def test_synthesizer_and_export(self):
        """Test full synthesis and export to JSON, CSV, and Markdown."""
        item1 = ResearchGapItem(
            id="test_gap_sec",
            source_type="intl_paper",
            source_title="Differential Privacy in Census",
            year="2024",
            author="Garfinkel et al.",
            cluster="security_privacy",
            gap_category="methodological_bottleneck",
            raw_excerpt="Query reconstruction attacks remain a challenge when privacy budget is exhausted.",
            synthesized_summary="Tantangan rekonstruksi data saat budget privasi habis.",
            recommended_opportunity="Implementasi cryptographic budget tracking.",
            source_location="literature/topik_3.md:120",
        )
        item2 = ResearchGapItem(
            id="test_gap_capi",
            source_type="stis_thesis",
            source_title="Aplikasi CAPI Survei SHK",
            year="2023",
            author="Rayhan",
            cluster="data_collection_capi",
            gap_category="future_work",
            raw_excerpt="Saran pada penelitian selanjutnya adalah menambahkan modul pemantauan paradatak.",
            synthesized_summary="Saran penambahan modul paradatak.",
            recommended_opportunity="Deteksi anomali waktu dwell-time pencacahan.",
            source_location="theses_data.json#123",
        )

        synthesizer = BrainstormSynthesizer([item1, item2])
        summaries = synthesizer.synthesize_by_cluster()
        matrix = synthesizer.generate_research_matrix()

        self.assertEqual(len(summaries["security_privacy"].methodological_bottlenecks), 1)
        self.assertEqual(len(summaries["data_collection_capi"].future_works), 1)
        self.assertEqual(len(matrix), 3)

        with tempfile.TemporaryDirectory() as tmpdir:
            tmproot = Path(tmpdir)
            exporter = BrainstormExporter(workspace_root=tmproot)

            j_path = exporter.export_json([item1, item2])
            c_path = exporter.export_csv([item1, item2])
            m_path = exporter.export_markdown_report(summaries, matrix)

            self.assertTrue(j_path.exists())
            self.assertTrue(c_path.exists())
            self.assertTrue(m_path.exists())

            # Validate JSON content
            with open(j_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertEqual(len(data), 2)

            # Validate Markdown content
            with open(m_path, "r", encoding="utf-8") as f:
                md_text = f.read()
            self.assertIn("Peta Peluang Riset", md_text)
            self.assertIn("Keamanan Sistem & Privasi Data Statistik", md_text)


if __name__ == "__main__":
    unittest.main()
