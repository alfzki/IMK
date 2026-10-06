"""Human-in-the-loop checkpoint module for interactive review, editing, and approval of chapter drafts."""

from __future__ import annotations

import logging
from typing import Any, Callable, Dict, Optional, Tuple

from calm_carson.drafting.models import ChapterOutline, SectionDraft

logger = logging.getLogger(__name__)


class DraftingCheckpoint:
    """Manages user inspection, approval, inline editing, and pause/resume checkpoints."""

    def __init__(self, headless: bool = False):
        self.headless = headless

    def review_chapter(
        self,
        chapter: ChapterOutline,
        draft: SectionDraft,
        auto_approve: bool = False,
        interactive_fn: Optional[Callable[[], str]] = None,
    ) -> Tuple[str, Optional[str]]:
        """
        Presents the drafted chapter to the user and awaits an approval decision.
        Returns:
            Tuple of (action, user_input) where action is one of:
            'approve', 'edit', 'regenerate', 'pause'
        """
        # Display Chapter Inspection Banner
        print("\n" + "=" * 80)
        print(f"📋 TITIK KENDALI PENGGUNA (HUMAN CHECKPOINT): {chapter.title.upper()}")
        print("=" * 80)
        print(f"ID Bab         : {chapter.id} (Bab {chapter.number})")
        print(f"Status Draf    : {draft.status}")
        print(f"Jumlah Revisi  : {draft.revision_count} iterasi otomatis")

        if draft.verification_summary:
            v = draft.verification_summary
            print(f"Audit Keabsahan: 🟢 {v.get('supported_count', 0)} Didukung | "
                  f"🔴 {v.get('contradicted_count', 0)} Kontradiksi | "
                  f"💡 {v.get('missing_citations_count', 0)} Perlu Sitasi | "
                  f"❓ {v.get('unsupported_count', 0)} Kurang Bukti")
            print(f"Status Mutu    : {v.get('overall_status', 'UNKNOWN')}")

        if getattr(draft, "style_summary", None):
            s = draft.style_summary
            score = s.get("ai_risk_score", 0)
            verdict = s.get("risk_verdict", "UNKNOWN")
            fatal = s.get("fatal_count", 0)
            high = s.get("high_count", 0)
            med = s.get("medium_count", 0)
            burstiness = s.get("burstiness_score", 0.0)
            em_dash = s.get("em_dash_count", 0)

            badge_emoji = "🟢" if score < 20 else ("🟡" if score < 40 else ("🟠" if score < 70 else "🔴"))
            print(f"Audit Gaya AI  : {badge_emoji} Skor Risiko {score}/100 ({verdict}) | "
                  f"Temuan: {fatal} Fatal, {high} Tinggi, {med} Sedang | "
                  f"Tanda Pisah (—): {em_dash} | Burstiness: {burstiness:.2f}")

        print("-" * 80)
        print("📄 PRATINJAU DRAF NASKAH (15 Baris Pertama):")
        lines = draft.final_draft.splitlines()
        preview_text = "\n".join(lines[:15])
        print(preview_text)
        if len(lines) > 15:
            print(f"... [{len(lines) - 15} baris tambahan di berkas output] ...")
        print("-" * 80)

        # Handle non-interactive / headless execution
        if auto_approve or self.headless:
            print("[✓] Mode Auto-Approve aktif: Bab otomatis disetujui untuk melanjutkan ke tahap berikutnya.")
            return "approve", None

        def _get_input(prompt_text: str) -> str:
            if interactive_fn is not None:
                import inspect
                try:
                    sig = inspect.signature(interactive_fn)
                    if len(sig.parameters) > 0:
                        return interactive_fn(prompt_text)
                except Exception:
                    pass
                return interactive_fn()
            return input(prompt_text)

        # Interactive Terminal Loop
        while True:
            print("\nPILIHAN TINDAKAN:")
            print("  [1] Setujui & Lanjutkan ke Bab Berikutnya (Approve)")
            print("  [2] Masukkan Catatan Suntingan / Koreksi Manual (Edit)")
            print("  [3] Tulis Ulang Draf Bab Ini (Regenerate)")
            print("  [4] Simpan Status & Jeda Progres (Save & Pause)")
            print("  [5] Tampilkan Rincian Lengkap Audit Gaya Bahasa AI (Signs of AI)")

            try:
                choice = _get_input("\nMasukkan pilihan [1-5] (default: 1): ").strip() or "1"
            except (EOFError, KeyboardInterrupt):
                print("\n[!] Sinyal keluar diterima. Menyimpan progres...")
                return "pause", None

            if choice in ["1", "approve", "y", "ya"]:
                print("[✓] Bab disetujui. Melanjutkan ke bab berikutnya...")
                return "approve", None

            elif choice in ["2", "edit"]:
                try:
                    notes = _get_input("\nMasukkan catatan suntingan atau teks koreksi yang diinginkan:\n> ").strip()
                except (EOFError, KeyboardInterrupt):
                    notes = ""
                return "edit", notes

            elif choice in ["3", "regenerate"]:
                print("[*] Menjadwalkan penulisan ulang bab dengan penyelarasan bukti baru...")
                return "regenerate", None

            elif choice in ["4", "pause", "exit", "quit"]:
                print("[*] Menyimpan status workflow. Anda dapat melanjutkannya kapan saja dengan flag --resume.")
                return "pause", None

            elif choice in ["5", "style", "ai"]:
                from calm_carson.style import AIStyleChecker, StyleExporter
                checker = AIStyleChecker()
                rep = checker.check_text(draft.final_draft, source_id=f"Bab {chapter.number}")
                print(StyleExporter.render_terminal(rep, show_annotated=True, suggest_fixes=True))
                continue

            else:
                print("[-] Pilihan tidak valid. Masukkan angka 1 sampai 5.")
