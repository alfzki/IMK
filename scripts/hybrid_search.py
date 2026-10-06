#!/usr/bin/env python3
"""
CLI Runner: Hybrid Markdown Retrieval (Dense Semantic + Sparse BM25 with RRF)
Indexes and searches technical and scientific markdown documents across the workspace.
"""

import argparse
import os
import shutil
import sys

# Auto-reexec into project .venv if run with system python
try:
    import torch
    import transformers
except ImportError:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    venv_python = os.path.join(project_root, ".venv", "bin", "python")
    if os.path.exists(venv_python) and sys.executable != venv_python:
        os.execv(venv_python, [venv_python] + sys.argv)
    uv_bin = shutil.which("uv")
    if uv_bin:
        os.execv(uv_bin, ["uv", "run", "python"] + sys.argv)
    print("Error: Missing required packages (torch, transformers).")
    print("Please run using: uv run python " + " ".join(sys.argv))
    sys.exit(1)

# Ensure src/ is on sys.path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
src_dir = os.path.join(project_root, "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from calm_carson.search import MarkdownHybridSearchEngine


def format_search_results(results, query: str):
    """Prints nicely formatted search results in terminal."""
    if not results:
        print("\n[-] Tidak ada potongan dokumen yang cocok ditemukan.")
        return

    print(f"\n[+] Ditemukan {len(results)} hasil pencarian paling relevan:")
    print("=" * 80)

    for idx, r in enumerate(results, start=1):
        print(f"\n📌 HASIL #{idx} | Skor RRF: {r.rrf_score:.5f}")
        print(f"📄 Berkas   : {r.doc_path} (Baris {r.start_line}–{r.end_line})")
        print(f"🏷️  Hierarki : {r.breadcrumb}")
        
        detail_scores = []
        if r.dense_score is not None:
            detail_scores.append(f"Dense: {r.dense_score:.4f} (Rank #{r.dense_rank})")
        if r.sparse_score is not None:
            detail_scores.append(f"BM25: {r.sparse_score:.2f} (Rank #{r.sparse_rank})")
        if detail_scores:
            print(f"📊 Rincian  : {' | '.join(detail_scores)}")

        print("-" * 80)
        # Show preview (first 400 chars of raw content)
        snippet = r.raw_content.strip()
        lines = snippet.splitlines()
        preview_lines = lines[:8]
        preview = "\n".join(preview_lines)
        if len(lines) > 8 or len(snippet) > 500:
            preview = preview[:500] + "\n... [teks dipotong] ..."

        print(preview)
        print("=" * 80)


def main():
    parser = argparse.ArgumentParser(
        description="Hybrid Markdown Retrieval System (Dense Vector + Sparse BM25)"
    )
    parser.add_argument(
        "--query", "-q",
        type=str,
        default=None,
        help="Teks kueri pencarian (pertanyaan atau kata kunci)",
    )
    parser.add_argument(
        "--index",
        action="store_true",
        help="Bangun / perbarui indeks korpus Markdown",
    )
    parser.add_argument(
        "--reindex",
        action="store_true",
        help="Bangun ulang seluruh indeks korpus Markdown dari awal",
    )
    parser.add_argument(
        "--top-k", "-k",
        type=int,
        default=5,
        help="Jumlah hasil teratas yang ditampilkan (default: 5)",
    )
    parser.add_argument(
        "--mode", "-m",
        type=str,
        default="hybrid",
        choices=["hybrid", "dense", "sparse"],
        help="Metode pencarian: hybrid (RRF), dense (semantik), sparse (BM25) (default: hybrid)",
    )
    parser.add_argument(
        "--filter-dir", "-f",
        type=str,
        default=None,
        help="Batasi pencarian pada direktori tertentu (misal: 'proposals', 'literature', 'docs')",
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Tampilkan statistik indeks saat ini",
    )
    parser.add_argument(
        "--index-dir",
        type=str,
        default="literature/search_index",
        help="Direktori penyimpanan indeks (default: literature/search_index)",
    )

    args = parser.parse_args()

    engine = MarkdownHybridSearchEngine(index_dir=args.index_dir)

    # 1. Stats command
    if args.stats:
        stats = engine.get_stats()
        print("\n=== Statistik Indeks Hybrid Retrieval ===")
        for k, v in stats.items():
            print(f"  {k:25}: {v}")
        return

    # 2. Index / Reindex command
    if args.index or args.reindex:
        print("\n[*] Memulai pengindeksan korpus dokumen Markdown...")
        total_chunks = engine.index_corpus(base_dir=project_root)
        print(f"[+] Pengindeksan selesai! {total_chunks} potongan teks terindeks.")
        if not args.query:
            return

    # 3. Query search
    if args.query:
        # Check if index exists
        stats = engine.get_stats()
        if stats.get("status") != "ready":
            print("[*] Indeks belum ditemukan. Membangun indeks otomatis pertama kali...")
            engine.index_corpus(base_dir=project_root)

        print(f"\n🔍 Menjalankan pencarian ({args.mode.upper()}): '{args.query}'")
        if args.filter_dir:
            print(f"📁 Filter folder: '{args.filter_dir}'")

        results = engine.search(
            query=args.query,
            top_k=args.top_k,
            mode=args.mode,
            filter_dir=args.filter_dir,
        )
        format_search_results(results, args.query)
        return

    # If no action specified, show help
    parser.print_help()


if __name__ == "__main__":
    main()
