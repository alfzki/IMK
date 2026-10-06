#!/usr/bin/env python3
"""
CLI Runner for Research Gap Analysis & Topic Brainstorming.
Menganalisis keterbatasan, saran, dan celah penelitian dari korpus lokal skripsi STIS dan paper internasional.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

# Auto-bootstrap local .venv if not currently active
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
VENV_PYTHON = WORKSPACE_ROOT / ".venv" / "bin" / "python"
SRC_PATH = WORKSPACE_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

if VENV_PYTHON.exists() and sys.executable != str(VENV_PYTHON):
    if not os.environ.get("CALM_CARSON_BOOTSTRAPPED"):
        os.environ["CALM_CARSON_BOOTSTRAPPED"] = "1"
        os.environ["PYTHONPATH"] = f"{SRC_PATH}:{os.environ.get('PYTHONPATH', '')}"
        os.execv(str(VENV_PYTHON), [str(VENV_PYTHON)] + sys.argv)

from calm_carson.brainstorm import (
    CLUSTER_NAMES,
    BrainstormExporter,
    BrainstormSynthesizer,
    ResearchGapExtractor,
    run_brainstorm_pipeline,
)


def print_banner() -> None:
    print("=" * 80)
    print("💡 CALM-CARSON: Research Gap Analyzer & Topic Brainstorming Engine")
    print("   Politeknik Statistika STIS - Peminatan Sistem Informasi Statistik (SIS)")
    print("=" * 80)


def print_stats(summaries: dict) -> None:
    print("\n📊 STATISTIK KESENJANGAN RISET & ARAHAN PENELITIAN LANJUTAN:")
    print("-" * 80)
    print(f"{'Klaster SIS':<45} | {'Masalah':<8} | {'Limitasi':<9} | {'Saran (FW)':<10} | {'Total':<6}")
    print("-" * 80)

    total_prob = 0
    total_lim = 0
    total_fw = 0

    for cid, cs in summaries.items():
        n_prob = len(cs.open_problems)
        n_lim = len(cs.methodological_bottlenecks)
        n_fw = len(cs.future_works)
        total_prob += n_prob
        total_lim += n_lim
        total_fw += n_fw
        cname = cs.cluster_name[:43]
        print(f"{cname:<45} | {n_prob:<8} | {n_lim:<9} | {n_fw:<10} | {cs.total_items:<6}")

    print("-" * 80)
    print(f"{'TOTAL KESELURUHAN':<45} | {total_prob:<8} | {total_lim:<9} | {total_fw:<10} | {total_prob+total_lim+total_fw:<6}")
    print("=" * 80)


def display_cluster_results(summary, limit: int = 5) -> None:
    print(f"\n📂 KLASTER: {summary.cluster_name}")
    print("=" * 80)

    print("\n💡 PELUANG PENELITIAN BARU STRATEGIS (DSRM / REKAYASA SIS):")
    for idx, opp in enumerate(summary.synthesized_opportunities, start=1):
        print(f"  {idx}. {opp}")

    if summary.future_works:
        print(f"\n📌 ARAHAN PENELITIAN SELANJUTNYA (FUTURE WORK DARI DOKUMEN) [Top {min(limit, len(summary.future_works))}]:")
        for idx, item in enumerate(summary.future_works[:limit], start=1):
            print(f"\n  [{idx}] {item.source_title} ({item.author}, {item.year})")
            print(f"      Lokasi : {item.source_location}")
            print(f"      Kutipan: \"{item.raw_excerpt[:200]}...\"")
            print(f"      Peluang: ➡️  {item.recommended_opportunity}")

    if summary.methodological_bottlenecks:
        print(f"\n⚠️  KETERBATASAN METODOLOGI SKRIPSI/PAPER TERDAHULU [Top {min(limit, len(summary.methodological_bottlenecks))}]:")
        for idx, item in enumerate(summary.methodological_bottlenecks[:limit], start=1):
            print(f"\n  [{idx}] {item.source_title} ({item.author}, {item.year})")
            print(f"      Lokasi : {item.source_location}")
            print(f"      Limitasi: \"{item.raw_excerpt[:200]}...\"")
            print(f"      Solusi  : 🛠️  {item.recommended_opportunity}")

    print("\n" + "-" * 80)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analisis gap penelitian, limitasi, dan arahan riset selanjutnya dari korpus dokumen lokal."
    )
    parser.add_argument(
        "--cluster",
        "-c",
        choices=list(CLUSTER_NAMES.keys()) + ["all"],
        default="all",
        help="Filter berdasarkan klaster bidang SIS (default: all)",
    )
    parser.add_argument(
        "--query",
        "-q",
        type=str,
        help="Kueri hybrid search tertarget untuk mengekstrak gap konsep spesifik (misal: 'API gateway', 'differential privacy')",
    )
    parser.add_argument(
        "--min-year",
        type=int,
        default=2021,
        help="Batas tahun minimal publikasi skripsi/paper (default: 2021)",
    )
    parser.add_argument(
        "--limit",
        "-l",
        type=int,
        default=5,
        help="Jumlah tampilan item per kategori (default: 5)",
    )
    parser.add_argument(
        "--export",
        action="store_true",
        help="Ekspor hasil ekstraksi ke literature/brainstorming_gaps.json, .csv, dan brainstorming/peta_peluang_riset.md",
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Tampilkan hanya statistik sebaran kesenjangan riset",
    )

    args = parser.parse_args()
    print_banner()

    extractor = ResearchGapExtractor(workspace_root=WORKSPACE_ROOT)

    if args.query:
        print(f"🔍 Menjalankan penelusuran kesenjangan spesifik untuk kueri: '{args.query}'...")
        gap_items = extractor.extract_from_hybrid_search(
            query=args.query,
            cluster_filter=args.cluster,
            top_k=args.limit,
        )
        if not gap_items:
            print("❌ Tidak ditemukan potongan limitasi atau future work yang cocok dengan kueri tersebut.")
            return

        print(f"\n[+] Ditemukan {len(gap_items)} kesenjangan riset terkait:")
        for idx, item in enumerate(gap_items, start=1):
            print(f"\n[{idx}] {item.source_title} ({item.author}, {item.year})")
            print(f"    Kategori: {item.gap_category} | Klaster: {item.cluster}")
            print(f"    Lokasi  : {item.source_location}")
            print(f"    Kutipan : \"{item.raw_excerpt[:250]}...\"")
            print(f"    Peluang : 💡 {item.recommended_opportunity}")
        print("\n" + "=" * 80)
        return

    # Extract all or per-cluster
    cluster_arg = None if args.cluster == "all" else args.cluster
    print(f"[*] Menambang batasan masalah, diskusi, dan saran dari korpus dokumen (Tahun >= {args.min_year})...")
    items = extractor.extract_all(cluster_filter=cluster_arg, min_year=args.min_year)
    print(f"[+] Berhasil mengekstrak {len(items)} item kesenjangan dan saran penelitian.")

    synthesizer = BrainstormSynthesizer(items)
    summaries = synthesizer.synthesize_by_cluster()
    matrix = synthesizer.generate_research_matrix()

    if args.stats:
        print_stats(summaries)
        return

    # Display findings
    if args.cluster != "all" and args.cluster in summaries:
        display_cluster_results(summaries[args.cluster], limit=args.limit)
    else:
        print_stats(summaries)
        for cid in ["security_privacy", "sdi_interoperability", "data_collection_capi"]:
            if cid in summaries:
                display_cluster_results(summaries[cid], limit=args.limit)

    if args.export:
        print("\n[*] Mengekspor data terstruktur dan laporan sintesis...")
        exporter = BrainstormExporter(workspace_root=WORKSPACE_ROOT)
        j_path = exporter.export_json(items)
        c_path = exporter.export_csv(items)
        m_path = exporter.export_markdown_report(summaries, matrix)
        print(f"  [✓] JSON     : {j_path.relative_to(WORKSPACE_ROOT)}")
        print(f"  [✓] CSV      : {c_path.relative_to(WORKSPACE_ROOT)}")
        print(f"  [✓] Markdown : {m_path.relative_to(WORKSPACE_ROOT)}")
        print("\n[+] Selesai! Berkas siap digunakan sebagai pijakan perumusan proposal penelitian.")
    else:
        print("\n💡 Gunakan flag '--export' untuk menyimpan seluruh hasil ke format JSON, CSV, dan Markdown.")


if __name__ == "__main__":
    main()
