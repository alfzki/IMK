#!/usr/bin/env python3
"""
CLI Runner for Research Topic Originality & Novelty Checker.
Menguji orisinalitas rumusan masalah dan draf ide skripsi terhadap lanskap literatur ilmiah global.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

# Auto-bootstrap local .venv if run with system python
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

from calm_carson.originality import (
    GlobalLiteratureSearcher,
    OriginalityEvaluator,
    OriginalityExporter,
    check_topic_originality,
)


def print_banner() -> None:
    print("=" * 80)
    print("🌐 CALM-CARSON: Global Literature Research Originality & Novelty Checker")
    print("   Politeknik Statistika STIS - Peminatan Sistem Informasi Statistik (SIS)")
    print("=" * 80)


def display_report(report) -> None:
    risk_colors = {
        "HIGH_OVERLAP": "\033[91m🔴 RISIKO TINGGI (HIGH OVERLAP)\033[0m",
        "MODERATE_OVERLAP": "\033[93m🟡 RISIKO SEDANG (MODERATE OVERLAP)\033[0m",
        "DISTINCT_NOVEL": "\033[92m🟢 KEBARUAN TINGGI (DISTINCT NOVELTY)\033[0m",
    }
    badge = risk_colors.get(report.overall_risk, report.overall_risk)

    print(f"\n📋 HASIL EVALUASI ORISINALITAS:")
    print("-" * 80)
    print(f"Status Evaluasi    : {badge}")
    print(f"Kemiripan Tertinggi: {report.max_similarity * 100:.1f}%")
    print(f"Rata-rata Kemiripan: {report.mean_similarity * 100:.1f}%")
    print(f"Distribusi Temuan  : {report.high_overlap_count} High (≥70%) | {report.moderate_overlap_count} Moderate (45–69%) | {report.low_overlap_count} Low (<45%)")
    print(f"\nCatatan Evaluator  :\n> {report.risk_summary}")
    print("-" * 80)

    print("\n📚 PUBLIKASI ILMIAH GLOBAL PALING SERUPA (TOP BENCHMARKS):")
    print("-" * 80)
    print(f"{'No':<3} | {'Skor':<6} | {'Level':<8} | {'Penulis & Tahun':<25} | {'Judul Publikasi'}")
    print("-" * 80)

    for idx, m in enumerate(report.matches[:8], start=1):
        author_short = m.authors[0] if len(m.authors) == 1 else f"{m.authors[0]} et al."
        author_year = f"{author_short[:18]} ({m.year})"
        title_trunc = m.title[:45] + "..." if len(m.title) > 45 else m.title
        print(f"{idx:<3} | {m.similarity_score*100:>5.1f}% | {m.overlap_level:<8} | {author_year:<25} | {title_trunc}")

    print("-" * 80)
    print("\n💡 MASUKAN KRITIS & ASPEK PEMBEDA (STRATEGI PENGUATAN NOVELTY):")
    print("-" * 80)

    for idx, fb in enumerate(report.differentiation_feedbacks, start=1):
        print(f"\n[{idx}] Dimensi: {fb.dimension_name}")
        print(f"    Analisis Irisan: {fb.overlap_analysis}")
        print(f"    Rekomendasi    : ➡️  {fb.recommended_differentiation}")
        print(f"    Panduan Teknis : 🛠️  {fb.actionable_guidance}")

    print("\n" + "=" * 80)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Uji orisinalitas dan kebaruan (novelty) draf ide skripsi terhadap literatur ilmiah global."
    )
    parser.add_argument(
        "--idea",
        "-i",
        type=str,
        help="Rumusan masalah atau draf judul/deskripsi ide penelitian yang ingin diuji",
    )
    parser.add_argument(
        "--file",
        "-f",
        type=str,
        help="Path ke berkas teks atau Markdown yang memuat draf proposal/ide riset",
    )
    parser.add_argument(
        "--min-year",
        type=int,
        default=2021,
        help="Batas tahun minimal publikasi ilmiah internasional (default: 2021)",
    )
    parser.add_argument(
        "--limit",
        "-l",
        type=int,
        default=10,
        help="Maksimal publikasi yang dianalisis (default: 10)",
    )
    parser.add_argument(
        "--export",
        action="store_true",
        help="Ekspor laporan hasil evaluasi ke format JSON dan Markdown",
    )

    args = parser.parse_args()
    print_banner()

    idea_text = ""
    if args.idea:
        idea_text = args.idea.strip()
    elif args.file:
        fpath = Path(args.file)
        if not fpath.exists():
            print(f"❌ Berkas tidak ditemukan: {fpath}")
            sys.exit(1)
        with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
            idea_text = f.read().strip()
    else:
        # Prompt user interactively
        print("\nSilakan masukkan rumusan masalah atau draf ide skripsi Anda:")
        try:
            idea_text = input("> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nOperasi dibatalkan.")
            sys.exit(0)

    if not idea_text:
        print("❌ Teks ide penelitian tidak boleh kosong.")
        sys.exit(1)

    print(f"\n[*] Menganalisis ide riset ({len(idea_text)} karakter)...")
    searcher = GlobalLiteratureSearcher(workspace_root=WORKSPACE_ROOT)
    queries = searcher.formulate_search_queries(idea_text)
    print(f"[*] Kueri akademis terstruktur yang dibentuk:")
    for q in queries:
        print(f"    - {q}")

    print(f"\n[*] Menelusuri publikasi ilmiah internasional (OpenAlex & arXiv, {args.min_year}–2026)...")
    report = check_topic_originality(
        idea_text=idea_text,
        workspace_root=WORKSPACE_ROOT,
        min_year=args.min_year,
        limit=args.limit,
        export_files=args.export,
    )

    display_report(report)

    if args.export:
        slug = report.idea_text[:30].replace(" ", "_").lower()
        print(f"\n[✓] Laporan JSON     : literature/originality_eval_*.json")
        print(f"[✓] Laporan Markdown : brainstorming/laporan_orisinalitas_*.md")


if __name__ == "__main__":
    main()
