#!/usr/bin/env python3
"""
scripts/orchestrate_drafting.py
Berkas eksekusi utama CLI alur kerja semi-otomatis penyusunan naskah penelitian bab demi bab
untuk mahasiswa Diploma IV Komputasi Statistik (SIS) Politeknik Statistika STIS.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Add project root to sys.path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root / "src"))

from calm_carson.drafting import (
    DraftingCheckpoint,
    EvidenceCollector,
    SectionDrafter,
    ThesisDraftingPipeline,
    ThesisOutliner,
    AutomatedReviser,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Alur kerja semi-otomatis penyusunan naskah penelitian skripsi bab demi bab (STIS D-IV SIS)."
    )
    parser.add_argument(
        "--topic",
        "-t",
        type=str,
        default="1",
        help="Pilihan topik: '1' (Survey Fraud CAPI), '2' (SDI Gateway), '3' (Differential Privacy), atau judul kustom (default: 1)",
    )
    parser.add_argument(
        "--scope",
        "-s",
        type=str,
        choices=["proposal", "thesis"],
        default="proposal",
        help="Lingkup naskah: 'proposal' (Bab 1 s.d. Bab 3) atau 'thesis' (Bab 1 s.d. Bab 5) (default: proposal)",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        type=str,
        default="",
        help="Direktori penyimpanan draf bab dan naskah lengkap (default: drafts/topik_<id>)",
    )
    parser.add_argument(
        "--auto-approve",
        action="store_true",
        help="Mode otomatis: menyetujui setiap bab tanpa menunggu konfirmasi terminal interaktif (cocok untuk batch/CI)",
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        default=True,
        help="Mode interaktif dengan titik kendali review, edit, regenerate, atau pause (default: True)",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Lanjutkan proses penyusunan dari checkpoint state terakhir yang tersimpan",
    )
    parser.add_argument(
        "--chapter",
        "-c",
        type=int,
        default=None,
        help="Susun bab tertentu saja (misal: 1, 2, atau 3)",
    )
    parser.add_argument(
        "--list-topics",
        action="store_true",
        help="Tampilkan daftar 3 topik skripsi rekomendasi terverifikasi di workspace",
    )

    args = parser.parse_args()

    # List Topics Option
    if args.list_topics:
        outliner = ThesisOutliner()
        presets = outliner.get_preset_topics()
        print("\n" + "=" * 80)
        print("📚 DAFTAR TOPIK PENELITIAN REKOMENDASI TERVERIFIKASI (STIS D-IV SIS):")
        print("=" * 80)
        for k, v in presets.items():
            print(f"[{k}] {v['title']}")
            print(f"    Klaster : {v['cluster']}")
            print(f"    Keyword : {', '.join(v['keywords'][:5])}\n")
        print("=" * 80)
        return

    # Determine default output dir if not specified
    output_dir = args.output_dir
    if not output_dir:
        topic_key = args.topic.strip()
        if topic_key in ["1", "2", "3"]:
            output_dir = f"drafts/topik_{topic_key}"
        else:
            output_dir = "drafts/custom_topic"

    # Configure auto-approve
    auto_approve = args.auto_approve
    checkpoint = DraftingCheckpoint(headless=auto_approve)

    # Initialize Pipeline
    pipeline = ThesisDraftingPipeline(
        workspace_root=project_root,
        checkpoint=checkpoint,
    )

    try:
        final_state = pipeline.run_workflow(
            topic_key_or_title=args.topic,
            scope=args.scope,
            output_dir=output_dir,
            resume_from=args.resume,
            auto_approve=auto_approve,
            target_chapter_num=args.chapter,
        )

        print("\n" + "=" * 80)
        print("🎉 ALUR KERJA PENYUSUNAN NASKAH SELESAI!")
        print("=" * 80)
        print(f"Topik         : {final_state.topic_title}")
        print(f"Status        : {'SELESAI (LENGKAP)' if final_state.is_completed else 'DIJEDA'}")
        print(f"Bab Tersusun  : {len(final_state.chapters_completed)} Bab ({', '.join(final_state.chapters_completed)})")
        print(f"Folder Berkas : {project_root / final_state.output_dir}")
        print(f"Naskah Terpadu: {project_root / final_state.output_dir / 'naskah_lengkap_skripsi.md'}")
        print("=" * 80 + "\n")

    except KeyboardInterrupt:
        print("\n[!] Eksekusi dihentikan oleh pengguna.")
        sys.exit(0)


if __name__ == "__main__":
    main()
