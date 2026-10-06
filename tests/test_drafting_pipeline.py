"""Unit tests for semi-automated thesis drafting pipeline: outliner, collector, drafter, reviser, checkpoint, and orchestrator."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from calm_carson.drafting.checkpoint import DraftingCheckpoint
from calm_carson.drafting.collector import EvidenceCollector
from calm_carson.drafting.drafter import SectionDrafter
from calm_carson.drafting.models import (
    ChapterOutline,
    EvidenceItem,
    SectionDraft,
    SubSectionOutline,
    WorkflowState,
)
from calm_carson.drafting.outliner import ThesisOutliner
from calm_carson.drafting.pipeline import ThesisDraftingPipeline
from calm_carson.drafting.reviser import AutomatedReviser
from calm_carson.verify.models import (
    ClaimVerificationResult,
    EvidenceMatch,
    FactClaim,
    VerificationReport,
)


class MockVerifier:
    """Mock verifier for deterministic testing."""

    def __init__(self, mode: str = "valid"):
        self.mode = mode

    def verify_claim(self, claim: FactClaim, evidences):
        if self.mode == "contradicted" and "50.000" in claim.extracted_numbers:
            ev = EvidenceMatch(
                file_path="proposals/bank_data.md",
                start_line=10,
                end_line=20,
                breadcrumb="Topik 1 > Masalah 1",
                content="BPS merekrut sekitar 190.000 petugas lapangan [1].",
                similarity_score=0.90,
                matched_numbers=["190.000"],
                extracted_citations=["[1]"],
            )
            return ClaimVerificationResult(
                claim=claim,
                status="CONTRADICTED",
                citation_status="MISMATCH",
                confidence_score=0.90,
                best_evidence=ev,
                alternative_evidences=[],
                explanation="Klaim bertentangan: menyebut 50.000 padahal korpus mencatat 190.000",
                correction_suggestion="Koreksi angka menjadi 190.000",
                annotated_claim=f"{claim.original_sentence} [⚠️ KONTRADIKSI]",
            )
        elif self.mode == "missing_citation" and not claim.embedded_citations:
            ev = EvidenceMatch(
                file_path="proposals/bank_data.md",
                start_line=10,
                end_line=20,
                breadcrumb="Topik 1",
                content="Data resmi BPS mencatat hasil evaluasi [1].",
                similarity_score=0.88,
                matched_numbers=[],
                extracted_citations=["[1]"],
            )
            return ClaimVerificationResult(
                claim=claim,
                status="SUPPORTED",
                citation_status="MISSING",
                confidence_score=0.88,
                best_evidence=ev,
                alternative_evidences=[],
                explanation="Klaim didukung namun belum ada sitasi.",
                correction_suggestion="Tambahkan sitasi [1].",
                annotated_claim=f"{claim.original_sentence} [💡 PERLU SITASI]",
            )
        else:
            return ClaimVerificationResult(
                claim=claim,
                status="SUPPORTED",
                citation_status="VALID",
                confidence_score=0.92,
                best_evidence=None,
                alternative_evidences=[],
                explanation="Valid.",
                correction_suggestion=None,
                annotated_claim=f"{claim.original_sentence} [✓ TERVERIFIKASI]",
            )


class TestDraftingPipeline(unittest.TestCase):
    """Test suite covering the complete chapter drafting pipeline."""

    def test_outliner_preset_and_custom(self):
        """Test outline generation for proposal (Bab 1-3) and thesis (Bab 1-5)."""
        outliner = ThesisOutliner()

        # Proposal Scope (3 Chapters)
        prop_chapters = outliner.generate_outline("1", scope="proposal")
        self.assertEqual(len(prop_chapters), 3)
        self.assertEqual(prop_chapters[0].id, "bab_1")
        self.assertEqual(prop_chapters[1].id, "bab_2")
        self.assertEqual(prop_chapters[2].id, "bab_3")

        # Check Bab 1 Subsections
        sub_ids = [s.id for s in prop_chapters[0].subsections]
        self.assertIn("1.1", sub_ids)
        self.assertIn("1.2", sub_ids)
        self.assertIn("1.3", sub_ids)

        # Thesis Scope (5 Chapters)
        thesis_chapters = outliner.generate_outline("2", scope="thesis")
        self.assertEqual(len(thesis_chapters), 5)
        self.assertEqual(thesis_chapters[3].id, "bab_4")
        self.assertEqual(thesis_chapters[4].id, "bab_5")

        # Custom Topic Outline
        custom_chapters = outliner.generate_outline("Sistem Visualisasi Spasial Kemiskinan Berbasis WebGIS", scope="proposal")
        self.assertEqual(len(custom_chapters), 3)
        self.assertEqual(custom_chapters[0].id, "bab_1")
        self.assertEqual(custom_chapters[0].title, "Pendahuluan")
        self.assertEqual(len(custom_chapters[0].subsections), 5)

    def test_section_drafter_output(self):
        """Test academic chapter drafting with empirical figures and citations."""
        outliner = ThesisOutliner()
        drafter = SectionDrafter()

        topic_info = outliner._resolve_topic("1")
        ch1 = outliner._build_chapter_1(topic_info)

        dummy_evidence = {
            "1.1": [
                EvidenceItem(
                    source="bank_data.md",
                    content="Sensus Pertanian 2023 merekrut 190.000 mitra lapangan [1].",
                    line_reference="L10-L15",
                    relevance_score=0.9,
                    extracted_citations=["[1]"],
                    extracted_numbers=["190.000"],
                )
            ]
        }

        chapter_text = drafter.draft_chapter(ch1, topic_info, dummy_evidence)

        # Check that header and key elements are present
        self.assertIn("# BAB I: PENDAHULUAN", chapter_text)
        self.assertIn("## 1.1 Latar Belakang Masalah", chapter_text)
        self.assertIn("190.000", chapter_text)
        self.assertIn("[1]", chapter_text)
        self.assertIn("## 1.2 Rumusan Masalah", chapter_text)
        self.assertIn("## 1.3 Tujuan Penelitian", chapter_text)

    def test_automated_reviser_fixes_contradiction_and_citation(self):
        """Test that AutomatedReviser corrects conflicting numbers and appends missing citations."""
        mock_v = MockVerifier(mode="contradicted")
        reviser = AutomatedReviser(verifier=mock_v)

        bad_text = (
            "Pada Sensus Pertanian 2023, BPS merekrut sekitar 50.000 petugas lapangan. "
            "Sistem CAPI eksisting memverifikasi durasi pengisian."
        )

        fixed_text, fixes, final_report = reviser.revise_draft(bad_text)

        # Contradiction should have been resolved from 50.000 to 190.000
        self.assertTrue(any(f["type"] == "CONTRADICTION_RESOLVED" for f in fixes))
        self.assertIn("190.000", fixed_text)

    def test_checkpoint_interactive_actions(self):
        """Test DraftingCheckpoint actions: auto-approve, edit, and pause."""
        checkpoint = DraftingCheckpoint(headless=False)
        ch = ChapterOutline(id="bab_1", number=1, title="Pendahuluan", academic_goal="Test Goal")
        draft = SectionDraft(
            chapter_id="bab_1",
            chapter_title="Pendahuluan",
            raw_draft="Draf awal",
            verified_draft="Draf terverifikasi",
            final_draft="Draf final",
            status="VERIFIED",
        )

        # 1. Auto Approve
        act_auto, _ = checkpoint.review_chapter(ch, draft, auto_approve=True)
        self.assertEqual(act_auto, "approve")

        # 2. Interactive Edit
        inputs = ["2", "Catatan revisi saya"]
        act_edit, notes = checkpoint.review_chapter(
            ch,
            draft,
            interactive_fn=lambda prompt="": inputs.pop(0),
        )
        self.assertEqual(act_edit, "edit")
        self.assertEqual(notes, "Catatan revisi saya")

        # 3. Interactive Pause
        act_pause, _ = checkpoint.review_chapter(ch, draft, interactive_fn=lambda prompt="": "4")
        self.assertEqual(act_pause, "pause")

    def test_workflow_state_save_and_load(self):
        """Test state serialization and resumption from JSON."""
        state = WorkflowState(
            session_id="test-123",
            topic_id="topik_1_survey_fraud",
            topic_title="Test Topic",
            topic_cluster="data_collection",
            scope="proposal",
            current_chapter_idx=1,
            chapters_total=3,
            chapters_completed=["bab_1"],
            chapter_drafts={"bab_1": {"final_draft": "Isi Bab 1"}},
            output_dir="drafts/test",
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            p = Path(tmpdir) / "workflow_state.json"
            state.save(p)
            self.assertTrue(p.exists())

            loaded = WorkflowState.load(p)
            self.assertEqual(loaded.session_id, "test-123")
            self.assertEqual(loaded.current_chapter_idx, 1)
            self.assertEqual(loaded.chapters_completed, ["bab_1"])
            self.assertIn("bab_1", loaded.chapter_drafts)

    def test_pipeline_e2e_headless_run(self):
        """Test complete pipeline execution in headless mode for a specific chapter."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            pipeline = ThesisDraftingPipeline(
                workspace_root=tmp_path,
                reviser=AutomatedReviser(verifier=MockVerifier(mode="valid")),
                checkpoint=DraftingCheckpoint(headless=True),
            )

            final_state = pipeline.run_workflow(
                topic_key_or_title="1",
                scope="proposal",
                output_dir="drafts_out",
                auto_approve=True,
                target_chapter_num=1,
            )

            self.assertIn("bab_1", final_state.chapters_completed)
            self.assertTrue((tmp_path / "drafts_out" / "workflow_state.json").exists())
            self.assertTrue((tmp_path / "drafts_out" / "naskah_lengkap_skripsi.md").exists())

            # Read assembled manuscript
            with open(tmp_path / "drafts_out" / "naskah_lengkap_skripsi.md", "r", encoding="utf-8") as f:
                content = f.read()
                self.assertIn("BAB I: PENDAHULUAN", content)
                self.assertIn("190.000", content)


if __name__ == "__main__":
    unittest.main()
