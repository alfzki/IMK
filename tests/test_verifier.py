"""Unit tests for factual claim decomposition, alignment verification, and citation validation."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from calm_carson.verify.annotator import DraftAnnotator
from calm_carson.verify.decomposer import (
    ClaimDecomposer,
    extract_citations,
    extract_quantities,
    split_text_into_sentences,
)
from calm_carson.verify.exporter import VerificationExporter
from calm_carson.verify.models import (
    ClaimVerificationResult,
    EvidenceMatch,
    FactClaim,
    VerificationReport,
)
from calm_carson.verify.verifier import FactVerifier


class MockEmbeddingEngine:
    """Mock dense embedding engine for deterministic unit tests."""

    def encode(self, texts):
        import numpy as np
        vectors = []
        for t in texts:
            t_lower = t.lower()
            v = np.zeros(384, dtype=np.float32)
            if "petugas" in t_lower or "sensus" in t_lower or "mitra" in t_lower:
                v[0] = 0.9
                v[1] = 0.3
            elif "ips" in t_lower or "evaluasi" in t_lower or "metadata" in t_lower:
                v[2] = 0.9
                v[3] = 0.3
            elif "alien" in t_lower or "mars" in t_lower:
                v[15] = 1.0
            else:
                v[8] = 0.5
                v[9] = 0.5
            norm = np.linalg.norm(v)
            if norm > 0:
                v = v / norm
            vectors.append(v)
        return np.array(vectors, dtype=np.float32)


class TestVerifier(unittest.TestCase):
    """Test suite for claim decomposition, factual verification, and citation checking."""

    def test_decomposer_and_quantities(self):
        """Test sentence decomposition, numbers, and citation extraction."""
        text = (
            "Pada Sensus Pertanian 2023, BPS merekrut sekitar 190.000 mitra lapangan [1]. "
            "Tingkat pemalsuan kuesioner tersembunyi diperkirakan berkisar antara 3% hingga 15% [2], [3]. "
            "Nilai IPS nasional mencapai 1,48 dari skala 5,00."
        )

        decomposer = ClaimDecomposer()
        claims = decomposer.decompose(text)

        self.assertEqual(len(claims), 3)

        # Claim 1
        c1 = claims[0]
        self.assertIn("190.000", c1.extracted_numbers)
        self.assertIn("[1]", c1.embedded_citations)
        self.assertNotIn("[1]", c1.claim_text)  # cleaned text shouldn't have citation

        # Claim 2
        c2 = claims[1]
        self.assertTrue(any("3%" in n or "15%" in n for n in c2.extracted_numbers))
        self.assertTrue(any("[2]" in c or "[3]" in c for c in c2.embedded_citations))

        # Claim 3
        c3 = claims[2]
        self.assertIn("1,48", c3.extracted_numbers)
        self.assertEqual(len(c3.embedded_citations), 0)

    def test_abbreviations_in_sentence_splitting(self):
        """Test sentence splitting with academic abbreviations."""
        text = "Menurut Schwanhäuser et al. [2], metode deteksi fraud sangat efektif. Hal ini ditunjukkan pada vol. 86 no. 1 pp. 51–77."
        sentences = split_text_into_sentences(text)
        self.assertEqual(len(sentences), 2)

    def test_supported_claim_with_valid_and_missing_citations(self):
        """Test supported claim evaluation with both valid and missing citation markers."""
        mock_engine = MockEmbeddingEngine()
        verifier = FactVerifier(embedding_engine=mock_engine)

        evidence = EvidenceMatch(
            file_path="proposals/bank_data_masalah_proposal.md",
            start_line=12,
            end_line=18,
            breadcrumb="Topik 1 > Masalah 1",
            content="Pada Sensus Pertanian 2023 (ST2023), BPS merekrut sekitar 190.000 petugas/mitra lapangan [1].",
            similarity_score=0.95,
            matched_numbers=["190.000"],
            extracted_citations=["[1]"],
        )

        # Case A: Supported and citation is present
        claim_with_cite = FactClaim(
            id="c1",
            claim_text="Pada Sensus Pertanian 2023 BPS merekrut 190.000 mitra",
            original_sentence="Pada Sensus Pertanian 2023 BPS merekrut 190.000 mitra [1].",
            start_char=0,
            end_char=50,
            extracted_numbers=["190.000", "2023"],
            embedded_citations=["[1]"],
        )

        res_a = verifier.verify_claim(claim_with_cite, [evidence])
        self.assertEqual(res_a.status, "SUPPORTED")
        self.assertEqual(res_a.citation_status, "VALID")
        self.assertIn("TERVERIFIKASI", res_a.annotated_claim)

        # Case B: Supported but citation is missing
        claim_no_cite = FactClaim(
            id="c2",
            claim_text="Pada Sensus Pertanian 2023 BPS merekrut 190.000 mitra",
            original_sentence="Pada Sensus Pertanian 2023 BPS merekrut 190.000 mitra.",
            start_char=0,
            end_char=50,
            extracted_numbers=["190.000", "2023"],
            embedded_citations=[],
        )

        res_b = verifier.verify_claim(claim_no_cite, [evidence])
        self.assertEqual(res_b.status, "SUPPORTED")
        self.assertEqual(res_b.citation_status, "MISSING")
        self.assertIn("PERLU SITASI", res_b.annotated_claim)

    def test_contradiction_detection(self):
        """Test contradiction detection when numbers conflict with evidence."""
        mock_engine = MockEmbeddingEngine()
        verifier = FactVerifier(embedding_engine=mock_engine)

        evidence = EvidenceMatch(
            file_path="proposals/bank_data_masalah_proposal.md",
            start_line=12,
            end_line=18,
            breadcrumb="Topik 1 > Masalah 1",
            content="Pada Sensus Pertanian 2023 (ST2023), BPS merekrut sekitar 190.000 petugas/mitra lapangan [1].",
            similarity_score=0.88,
            matched_numbers=[],
            extracted_citations=["[1]"],
        )

        # Claim says 50.000 instead of 190.000
        claim_contra = FactClaim(
            id="c_contra",
            claim_text="Pada Sensus Pertanian 2023 BPS merekrut 50.000 petugas lapangan",
            original_sentence="Pada Sensus Pertanian 2023 BPS merekrut 50.000 petugas lapangan.",
            start_char=0,
            end_char=55,
            extracted_numbers=["50.000", "2023"],
            embedded_citations=[],
        )

        res = verifier.verify_claim(claim_contra, [evidence])
        self.assertEqual(res.status, "CONTRADICTED")
        self.assertIn("KONTRADIKSI", res.annotated_claim)
        self.assertIn("50.000", res.explanation)

    def test_unsupported_claim(self):
        """Test unsupported claim when no corpus evidence matches."""
        mock_engine = MockEmbeddingEngine()
        verifier = FactVerifier(embedding_engine=mock_engine)

        claim_alien = FactClaim(
            id="c_alien",
            claim_text="Alien mendarat di kantor BPS Jakarta pada tahun 2023.",
            original_sentence="Alien mendarat di kantor BPS Jakarta pada tahun 2023.",
            start_char=0,
            end_char=50,
            extracted_numbers=["2023"],
            embedded_citations=[],
        )

        res = verifier.verify_claim(claim_alien, [])
        self.assertEqual(res.status, "UNSUPPORTED")
        self.assertIn("TIDAK BERDASAR", res.annotated_claim)

    def test_annotator_and_exporter(self):
        """Test draft annotation and export to JSON & Markdown."""
        c1 = FactClaim(
            id="c1",
            claim_text="BPS merekrut 190.000 petugas",
            original_sentence="BPS merekrut 190.000 petugas [1].",
            start_char=0,
            end_char=30,
            extracted_numbers=["190.000"],
            embedded_citations=["[1]"],
        )
        res1 = ClaimVerificationResult(
            claim=c1,
            status="SUPPORTED",
            citation_status="VALID",
            confidence_score=0.95,
            best_evidence=None,
            annotated_claim="BPS merekrut 190.000 petugas [1]. [✓ TERVERIFIKASI]",
        )

        annotator = DraftAnnotator()
        annotated_text = annotator.annotate([res1])
        self.assertIn("[✓ TERVERIFIKASI]", annotated_text)

        report = VerificationReport(
            draft_text="BPS merekrut 190.000 petugas [1].",
            results=[res1],
            overall_verdict="READY_FOR_SUBMISSION",
            verdict_summary="Lolos verifikasi.",
            supported_count=1,
            contradicted_count=0,
            unsupported_count=0,
            missing_citation_count=0,
            annotated_draft=annotated_text,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            tmproot = Path(tmpdir)
            exporter = VerificationExporter(workspace_root=tmproot)

            j_path = exporter.export_json(report)
            m_path = exporter.export_markdown(report)

            self.assertTrue(j_path.exists())
            self.assertTrue(m_path.exists())

            with open(j_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertEqual(data["supported_count"], 1)

            with open(m_path, "r", encoding="utf-8") as f:
                md_text = f.read()
            self.assertIn("Laporan Audit Keabsahan Faktual", md_text)
            self.assertIn("LOLOS VERIFIKASI", md_text)


    def test_disallowed_thesis_citation_handling(self):
        """Test that citations to SIMPUS/theses are strictly flagged as DISALLOWED."""
        mock_engine = MockEmbeddingEngine()
        verifier = FactVerifier(embedding_engine=mock_engine)

        evidence = EvidenceMatch(
            file_path="proposals/bank_data_masalah_proposal.md",
            start_line=12,
            end_line=18,
            breadcrumb="Topik 1 > Masalah 1",
            content="Pada Sensus Pertanian 2023 (ST2023), BPS merekrut sekitar 190.000 petugas/mitra lapangan.",
            similarity_score=0.92,
            matched_numbers=["190.000"],
            extracted_citations=["[1]"],
        )

        claim_with_thesis = FactClaim(
            id="c_thesis",
            claim_text="Pada Sensus Pertanian 2023 BPS merekrut 190.000 mitra",
            original_sentence="Pada Sensus Pertanian 2023 BPS merekrut 190.000 mitra [Skripsi STIS, 2024].",
            start_char=0,
            end_char=60,
            extracted_numbers=["190.000", "2023"],
            embedded_citations=["[Skripsi STIS, 2024]"],
        )

        res = verifier.verify_claim(claim_with_thesis, [evidence])
        self.assertEqual(res.status, "DISALLOWED")
        self.assertEqual(res.citation_status, "DISALLOWED_THESIS")
        self.assertIn("SITASI SKRIPSI DILARANG", res.annotated_claim)


if __name__ == "__main__":
    unittest.main()

