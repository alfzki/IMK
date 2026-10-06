"""Orchestrator pipeline that executes the full chapter-by-chapter drafting workflow from outline to assembled manuscript."""

from __future__ import annotations

import logging
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from calm_carson.drafting.checkpoint import DraftingCheckpoint
from calm_carson.drafting.collector import EvidenceCollector
from calm_carson.drafting.drafter import SectionDrafter
from calm_carson.drafting.models import (
    ChapterOutline,
    EvidenceItem,
    SectionDraft,
    WorkflowState,
)
from calm_carson.drafting.outliner import ThesisOutliner
from calm_carson.drafting.reviser import AutomatedReviser

logger = logging.getLogger(__name__)


class ThesisDraftingPipeline:
    """Semi-automated workflow orchestrator for chapter-by-chapter academic thesis drafting."""

    def __init__(
        self,
        workspace_root: Optional[Path] = None,
        outliner: Optional[ThesisOutliner] = None,
        collector: Optional[EvidenceCollector] = None,
        drafter: Optional[SectionDrafter] = None,
        reviser: Optional[AutomatedReviser] = None,
        checkpoint: Optional[DraftingCheckpoint] = None,
    ):
        if workspace_root is None:
            self.workspace_root = Path(__file__).resolve().parent.parent.parent.parent
        else:
            self.workspace_root = Path(workspace_root)

        self.outliner = outliner or ThesisOutliner()
        self.collector = collector or EvidenceCollector(workspace_root=self.workspace_root)
        self.drafter = drafter or SectionDrafter()
        self.reviser = reviser or AutomatedReviser()
        self.checkpoint = checkpoint or DraftingCheckpoint()

    def run_workflow(
        self,
        topic_key_or_title: str = "1",
        scope: str = "proposal",
        output_dir: str = "drafts",
        resume_from: Optional[str | Path] = None,
        auto_approve: bool = False,
        target_chapter_num: Optional[int] = None,
        interactive_fn: Optional[Callable[[], str]] = None,
    ) -> WorkflowState:
        """Executes or resumes the multi-chapter drafting workflow."""
        out_path = self.workspace_root / output_dir
        out_path.mkdir(parents=True, exist_ok=True)
        state_file = out_path / "workflow_state.json"

        # 1. Initialize or Resume Workflow State
        if resume_from or (state_file.exists() and resume_from is not False and target_chapter_num is None):
            load_path = Path(resume_from) if resume_from else state_file
            if load_path.exists():
                logger.info("Resuming workflow from state file: %s", load_path)
                state = WorkflowState.load(load_path)
            else:
                state = self._init_state(topic_key_or_title, scope, output_dir)
        else:
            state = self._init_state(topic_key_or_title, scope, output_dir)

        # 2. Formulate Outlines
        topic_info = self.outliner._resolve_topic(state.topic_title or topic_key_or_title)
        chapters = self.outliner.generate_outline(topic_info["id"], scope=state.scope)
        state.chapters_total = len(chapters)

        print("\n" + "=" * 80)
        print("🚀 CALM-CARSON: Semi-Automated Thesis Drafting Pipeline")
        print("   Politeknik Statistika STIS - Peminatan Sistem Informasi Statistik (SIS)")
        print("=" * 80)
        print(f"Topik Penelitian : {topic_info['title']}")
        print(f"Klaster Minat    : {topic_info.get('cluster', 'SIS')}")
        print(f"Lingkup Naskah   : {state.scope.upper()} ({len(chapters)} Bab)")
        print(f"Direktori Output : {out_path}")
        print(f"Progres Terakhir : Bab {state.current_chapter_idx + 1} / {len(chapters)}")
        print("=" * 80)

        # 3. Iterate through chapters
        start_idx = state.current_chapter_idx
        if target_chapter_num is not None:
            # Filter specifically to requested chapter number
            chapters = [c for c in chapters if c.number == target_chapter_num]
            start_idx = 0

        idx = start_idx
        while idx < len(chapters):
            chapter = chapters[idx]
            ch_num = chapter.number
            print(f"\n[▶] MEMULAI PENYUSUNAN: Bab {ch_num} - {chapter.title}...")

            # Phase 1: Context & Evidence Collection
            print(f"  [*] Mengumpulkan bukti korpus lokal untuk {len(chapter.subsections)} sub-bab...")
            evidence_by_sub = self.collector.collect_for_chapter(chapter, topic_info)
            total_evidences = sum(len(evs) for evs in evidence_by_sub.values())
            print(f"  [+] Terkumpul {total_evidences} potongan bukti relevan dari korpus.")

            # Phase 2: Drafting Academic Prose
            print("  [*] Menyintesis draf bab berbasis bukti literatur dan sitasi IEEE...")
            raw_draft = self.drafter.draft_chapter(chapter, topic_info, evidence_by_sub)

            # Phase 3 & 4: Verification & Automated Revision Loop
            print("  [*] Menjalankan audit verifikasi klaim faktual dan integritas sitasi...")
            revised_draft, fixes, report = self.reviser.revise_draft(raw_draft)
            if fixes:
                print(f"  [✓] Diterapkan {len(fixes)} iterasi koreksi otomatis (kontradiksi angka & nomor sitasi).")
            else:
                print("  [✓] Draf bab langsung terverifikasi sahih tanpa kontradiksi.")

            # Phase 4b: Style & AI Tells Audit (Wikipedia:Signs_of_AI_writing)
            print("  [*] Menjalankan audit gaya penulisan AI (Signs of AI Writing)...")
            from calm_carson.style import AIStyleChecker
            style_checker = AIStyleChecker()
            style_report = style_checker.check_text(revised_draft, source_id=f"Bab {ch_num}")
            print(f"  [✓] Skor Risiko AI: {style_report.ai_risk_score}/100 ({style_report.risk_verdict}) | {style_report.total_violations} anomali gaya bahasa.")
            if style_report.fatal_count > 0:
                print(f"  [⚠️] PERINGATAN FATAL: Terdeteksi {style_report.fatal_count} artefak LLM / sapaan percakapan!")

            style_summary = {
                "ai_risk_score": style_report.ai_risk_score,
                "risk_verdict": style_report.risk_verdict,
                "total_violations": style_report.total_violations,
                "fatal_count": style_report.fatal_count,
                "high_count": style_report.high_count,
                "medium_count": style_report.medium_count,
                "low_count": style_report.low_count,
                "burstiness_score": style_report.metrics.burstiness_score,
                "em_dash_count": style_report.metrics.em_dash_count,
                "summary_verdict": style_report.summary_verdict,
            }

            # Construct SectionDraft object
            verification_summary = {
                "supported_count": report.supported_count,
                "contradicted_count": report.contradicted_count,
                "unsupported_count": report.unsupported_count,
                "missing_citations_count": report.missing_citation_count,
                "overall_status": report.overall_verdict,
            }

            all_ev_items: List[EvidenceItem] = []
            for evs in evidence_by_sub.values():
                all_ev_items.extend(evs)

            draft_obj = SectionDraft(
                chapter_id=chapter.id,
                chapter_title=chapter.title,
                raw_draft=raw_draft,
                verified_draft=revised_draft,
                final_draft=revised_draft,
                status="VERIFIED" if report.contradicted_count == 0 else "NEEDS_REVISION",
                evidences_used=all_ev_items[:10],
                verification_summary=verification_summary,
                style_summary=style_summary,
                revision_count=len(fixes),
            )

            # Phase 5: Human Checkpoint
            action, user_input = self.checkpoint.review_chapter(
                chapter=chapter,
                draft=draft_obj,
                auto_approve=auto_approve,
                interactive_fn=interactive_fn,
            )

            if action == "edit" and user_input:
                draft_obj.user_notes = user_input
                draft_obj.final_draft += f"\n\n### Catatan Penyuntingan Penulis:\n{user_input}\n"
                draft_obj.status = "EDITED"

            if action in ["approve", "edit"]:
                draft_obj.status = "APPROVED"
                # Save Chapter Markdown
                slug_title = self._slugify(chapter.title)
                ch_filename = f"bab_{ch_num}_{slug_title}.md"
                ch_path = out_path / ch_filename
                with open(ch_path, "w", encoding="utf-8") as f:
                    f.write(draft_obj.final_draft)
                print(f"  [✓] Berkas bab tersimpan di: {ch_path}")

                # Update State
                state.chapters_completed.append(chapter.id)
                state.chapter_drafts[chapter.id] = draft_obj.to_dict()
                state.current_chapter_idx = idx + 1
                state.save(state_file)
                idx += 1

            elif action == "regenerate":
                print("  [*] Mengulang proses drafting bab saat ini...")
                continue

            elif action == "pause":
                print(f"\n[⏸] Alur kerja dijeda pada Bab {ch_num}. Status tersimpan di {state_file}.")
                state.save(state_file)
                return state

        # Phase 6: Assembling Complete Manuscript
        print("\n" + "=" * 80)
        print("📚 MERAKIT NASKAH LENGKAP PENELITIAN...")
        assembled_file = self._assemble_manuscript(state, chapters, topic_info, out_path)
        print(f"[✓] Naskah lengkap berhasil dirakit: {assembled_file}")
        print("=" * 80)

        state.is_completed = True
        state.save(state_file)
        return state

    def _init_state(self, topic_key_or_title: str, scope: str, output_dir: str) -> WorkflowState:
        """Initializes a fresh workflow state object."""
        topic_info = self.outliner._resolve_topic(topic_key_or_title)
        return WorkflowState(
            session_id=str(uuid.uuid4())[:8],
            topic_id=topic_info["id"],
            topic_title=topic_info["title"],
            topic_cluster=topic_info.get("cluster", "SIS"),
            scope=scope,
            current_chapter_idx=0,
            chapters_total=3 if scope == "proposal" else 5,
            chapters_completed=[],
            chapter_drafts={},
            output_dir=output_dir,
            last_updated=datetime.now(timezone.utc).isoformat(),
            is_completed=False,
        )

    def _assemble_manuscript(
        self,
        state: WorkflowState,
        chapters: List[ChapterOutline],
        topic_info: Dict[str, Any],
        output_dir: Path,
    ) -> Path:
        """Combines all individual chapter markdown files into a single unified manuscript."""
        assembled_path = output_dir / "naskah_lengkap_skripsi.md"

        lines: List[str] = [
            f"# {topic_info['title'].upper()}",
            "",
            "**Naskah Penelitian Tingkat Akhir Program Studi Diploma IV Komputasi Statistik**  ",
            "**Peminatan Sistem Informasi Statistik (SIS) - Politeknik Statistika STIS**  ",
            f"*Tanggal Perakitan*: {datetime.now(timezone.utc).strftime('%d %B %Y')}  ",
            "",
            "---",
            "",
            "## DAFTAR ISI NASKAH",
            "",
        ]

        for ch in chapters:
            lines.append(f"- **BAB {ch.number}: {ch.title.upper()}**")
            for sub in ch.subsections:
                lines.append(f"  - {sub.id} {sub.title}")
        lines.append("")
        lines.append("---")
        lines.append("")

        for ch in chapters:
            ch_data = state.chapter_drafts.get(ch.id)
            if ch_data and ch_data.get("final_draft"):
                lines.append(ch_data["final_draft"])
                lines.append("")
                lines.append("---")
                lines.append("")
            else:
                # Check if file exists on disk
                slug_title = self._slugify(ch.title)
                ch_path = output_dir / f"bab_{ch.number}_{slug_title}.md"
                if ch_path.exists():
                    with open(ch_path, "r", encoding="utf-8") as f:
                        lines.append(f.read())
                    lines.append("")
                    lines.append("---")
                    lines.append("")

        with open(assembled_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        return assembled_path

    def _slugify(self, text: str) -> str:
        s = text.lower().strip()
        s = re.sub(r"[^\w\s-]", "", s)
        s = re.sub(r"[\s_-]+", "_", s)
        return s[:30]
