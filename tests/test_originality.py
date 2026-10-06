"""Unit tests for the research topic originality and novelty evaluation module."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from calm_carson.originality.evaluator import OriginalityEvaluator
from calm_carson.originality.exporter import OriginalityExporter, slugify
from calm_carson.originality.models import (
    DifferentiationFeedback,
    OriginalityReport,
    PublicationMatch,
)
from calm_carson.originality.searcher import (
    GlobalLiteratureSearcher,
    reconstruct_inverted_index,
)


class MockEmbeddingEngine:
    """Fast mock embedding engine for deterministic unit testing."""

    def encode(self, texts):
        import numpy as np
        # Return deterministic orthogonal/parallel vectors based on keywords
        vectors = []
        for t in texts:
            t_lower = t.lower()
            v = np.zeros(384, dtype=np.float32)
            if "differential privacy" in t_lower or "privasi" in t_lower:
                v[0] = 0.9
                v[1] = 0.4
            elif "microdata" in t_lower or "data mikro" in t_lower:
                v[0] = 0.7
                v[1] = 0.7
            elif "kriminalitas" in t_lower or "crime" in t_lower:
                v[10] = 1.0
            else:
                v[5] = 0.5
                v[6] = 0.5
            norm = np.linalg.norm(v)
            if norm > 0:
                v = v / norm
            vectors.append(v)
        return np.array(vectors, dtype=np.float32)


class TestOriginality(unittest.TestCase):
    """Test suite for originality and novelty checking pipeline."""

    def test_models(self):
        """Test PublicationMatch and OriginalityReport dataclasses."""
        pm = PublicationMatch(
            id="doi:10.1145/test",
            title="Practical Differential Privacy for SQL Queries",
            authors=["Noah Johnson", "Dawn Song"],
            year=2021,
            venue="VLDB",
            doi="10.1145/test",
            url="https://doi.org/10.1145/test",
            abstract="We present the FLEX differential privacy query engine.",
            citation_count=120,
            similarity_score=0.82,
            overlap_level="HIGH",
        )
        d = pm.to_dict()
        self.assertEqual(d["similarity_score"], 0.82)
        self.assertEqual(d["overlap_level"], "HIGH")

        df = DifferentiationFeedback(
            dimension="methodology_algorithm",
            dimension_name="Metodologi",
            overlap_analysis="Konsep SQL sudah ada.",
            recommended_differentiation="Tambahkan cryptographic budget audit.",
            actionable_guidance="Implementasikan hash chaining.",
        )

        report = OriginalityReport(
            idea_text="Rancang bangun secure differential privacy engine",
            generated_queries=["differential privacy sql engine"],
            matches=[pm],
            max_similarity=0.82,
            mean_similarity=0.82,
            overall_risk="HIGH_OVERLAP",
            risk_summary="Tingkat tumpang tindih tinggi.",
            differentiation_feedbacks=[df],
        )

        self.assertEqual(report.high_overlap_count, 1)
        self.assertEqual(report.moderate_overlap_count, 0)
        self.assertEqual(report.low_overlap_count, 0)
        rep_dict = report.to_dict()
        self.assertIn("max_similarity", rep_dict)
        self.assertEqual(rep_dict["max_similarity"], 0.82)

    def test_query_formulation(self):
        """Test translating Indonesian concepts to English academic search queries."""
        searcher = GlobalLiteratureSearcher()

        idea_dp = "Rancang Bangun Secure Microdata Query Engine dengan Penerapan Differential Privacy dan UU PDP"
        queries_dp = searcher.formulate_search_queries(idea_dp)
        self.assertTrue(any("differential privacy" in q for q in queries_dp))

        idea_fraud = "Deteksi anomali dan falsifikasi survei lapangan pencacahan BPS berbasis paradatak"
        queries_fraud = searcher.formulate_search_queries(idea_fraud)
        self.assertTrue(any("falsification" in q or "curbstoning" in q or "paradata" in q for q in queries_fraud))

    def test_reconstruct_inverted_index(self):
        """Test reconstructing OpenAlex inverted index abstract."""
        inverted = {"This": [0], "is": [1], "a": [2], "differential": [3], "privacy": [4], "paper": [5]}
        reconstructed = reconstruct_inverted_index(inverted)
        self.assertEqual(reconstructed, "This is a differential privacy paper")

    def test_evaluator_with_mock_engine(self):
        """Test semantic similarity scoring and risk classification."""
        mock_engine = MockEmbeddingEngine()
        evaluator = OriginalityEvaluator(embedding_engine=mock_engine)

        idea = "Penerapan differential privacy pada data mikro tabular"
        pubs = [
            {
                "id": "p1",
                "title": "Differential Privacy for Tabular Microdata Release",
                "abstract": "We study differential privacy on tabular data.",
                "authors": ["Alice Smith"],
                "year": 2023,
                "venue": "IEEE S&P",
                "citation_count": 45,
            },
            {
                "id": "p2",
                "title": "Spatial Analysis of Urban Green Space and Crime",
                "abstract": "We analyze crime rates using spatial regression.",
                "authors": ["Bob Jones"],
                "year": 2022,
                "venue": "Urban Studies",
                "citation_count": 10,
            },
        ]

        report = evaluator.evaluate(idea, pubs, generated_queries=["differential privacy microdata"])

        self.assertEqual(len(report.matches), 2)
        # First paper should have high similarity
        self.assertGreater(report.matches[0].similarity_score, 0.70)
        self.assertEqual(report.matches[0].overlap_level, "HIGH")

        # Second paper should have low similarity
        self.assertLess(report.matches[1].similarity_score, 0.40)
        self.assertEqual(report.matches[1].overlap_level, "LOW")

        # Differentiation feedback should have all 5 dimensions
        self.assertEqual(len(report.differentiation_feedbacks), 5)
        dimensions = [df.dimension for df in report.differentiation_feedbacks]
        self.assertIn("methodology_algorithm", dimensions)
        self.assertIn("data_characteristics", dimensions)
        self.assertIn("dsrm_system_engineering", dimensions)
        self.assertIn("regulatory_compliance", dimensions)
        self.assertIn("evaluation_metrics", dimensions)

    def test_export_json_and_markdown(self):
        """Test exporting originality evaluation reports to JSON and Markdown."""
        mock_engine = MockEmbeddingEngine()
        evaluator = OriginalityEvaluator(embedding_engine=mock_engine)

        idea = "Sistem deteksi falsifikasi survei BPS"
        pubs = [{
            "id": "p1",
            "title": "Survey Falsification Detection",
            "abstract": "Detecting interviewer fraud in surveys.",
            "authors": ["Schwanhäuser"],
            "year": 2021,
            "venue": "Public Opinion Quarterly",
            "citation_count": 30,
        }]

        report = evaluator.evaluate(idea, pubs)

        with tempfile.TemporaryDirectory() as tmpdir:
            tmproot = Path(tmpdir)
            exporter = OriginalityExporter(workspace_root=tmproot)

            j_path = exporter.export_json(report)
            m_path = exporter.export_markdown(report)

            self.assertTrue(j_path.exists())
            self.assertTrue(m_path.exists())

            # Verify JSON
            with open(j_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertIn("overall_risk", data)
            self.assertEqual(data["total_matches"], 1)

            # Verify Markdown
            with open(m_path, "r", encoding="utf-8") as f:
                md_text = f.read()
            self.assertIn("Laporan Uji Orisinalitas", md_text)
            self.assertIn("Schwanhäuser", md_text)
            self.assertIn("Aspek Pembeda", md_text)


if __name__ == "__main__":
    unittest.main()
