#!/usr/bin/env python3
"""
CLI Runner: Automated Paper Metadata Extractor & BibTeX Citation Generator
Integrates local PDF and Markdown documents with Crossref, Semantic Scholar,
OpenAlex, and Politeknik Statistika STIS theses database.
"""

import argparse
import glob
import os
import shutil
import sys
from pathlib import Path

# Auto-reexec into project .venv if run with system python
try:
    import pypdf
    import requests
    from tqdm import tqdm
except ImportError:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    venv_python = os.path.join(project_root, ".venv", "bin", "python")
    if os.path.exists(venv_python) and sys.executable != venv_python:
        os.execv(venv_python, [venv_python] + sys.argv)
    uv_bin = shutil.which("uv")
    if uv_bin:
        os.execv(uv_bin, ["uv", "run", "python"] + sys.argv)
    print("Error: Missing required packages (pypdf, requests, tqdm).")
    print("Please run using: uv run python " + " ".join(sys.argv))
    sys.exit(1)

# Ensure src/ is on sys.path so calm_carson can be imported
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
src_dir = os.path.join(project_root, "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from calm_carson.metadata import (
    AcademicResolver,
    batch_process_documents,
    clean_doi,
    extract_paper_metadata,
)


def main():
    parser = argparse.ArgumentParser(
        description="Ekstraktor Metadata Paper & Generator Sitasi BibTeX Otomatis"
    )
    parser.add_argument(
        "--input", "-i",
        type=str,
        default=None,
        help="Path ke berkas PDF, Markdown, atau direktori dokumen",
    )
    parser.add_argument(
        "--doi",
        type=str,
        default=None,
        help="Ekstraksi metadata langsung menggunakan nomor DOI",
    )
    parser.add_argument(
        "--title",
        type=str,
        default=None,
        help="Pencarian metadata langsung menggunakan judul paper",
    )
    parser.add_argument(
        "--output-dir", "-o",
        type=str,
        default="literature",
        help="Direktori penyimpanan metadata JSON, CSV, dan BibTeX (default: literature)",
    )
    parser.add_argument(
        "--bibtex-file",
        type=str,
        default="references.bib",
        help="Nama berkas sitasi BibTeX output (default: references.bib)",
    )
    parser.add_argument(
        "--api",
        type=str,
        default="all",
        choices=["all", "crossref", "semanticscholar", "openalex"],
        help="Pilihan API literatur akademis yang diprioritaskan (default: all)",
    )
    parser.add_argument(
        "--recursive", "-r",
        action="store_true",
        help="Pindai subdirektori secara rekursif jika input berupa direktori",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Timpa metadata dan sitasi yang sudah ada sebelumnya",
    )
    parser.add_argument(
        "--allow-theses",
        action="store_true",
        help="Izinkan pencocokan skripsi SIMPUS sebagai referensi (default: False / disabled untuk artikel ilmiah)",
    )

    args = parser.parse_args()

    # 1. Direct DOI lookup
    if args.doi:
        print(f"[*] Menarik metadata untuk DOI: {args.doi}")
        resolver = AcademicResolver(allow_simpus_theses=args.allow_theses)
        meta, bib = resolver.resolve(doi=args.doi, preferred_api=args.api, allow_simpus_theses=args.allow_theses)
        if meta:
            print("\n[+] Metadata Ditemukan:")
            print(f"    Judul    : {meta.get('title')}")
            print(f"    Penulis  : {meta.get('authors')}")
            print(f"    Tahun    : {meta.get('year')}")
            print(f"    Venue    : {meta.get('venue')}")
            print(f"    Sumber   : {meta.get('api_source')}")
            if bib:
                print("\n[+] BibTeX:\n" + bib)
                
            batch_process_documents(
                [f"doi:{clean_doi(args.doi)}"],
                output_dir=args.output_dir,
                bibtex_filename=args.bibtex_file,
                preferred_api=args.api,
                force=args.force,
            )
        else:
            print("[-] Gagal menemukan metadata untuk DOI tersebut.")
        return

    # 2. Direct Title lookup
    if args.title:
        print(f"[*] Menarik metadata untuk Judul: {args.title}")
        resolver = AcademicResolver(allow_simpus_theses=args.allow_theses)
        meta, bib = resolver.resolve(title=args.title, preferred_api=args.api, allow_simpus_theses=args.allow_theses)
        if meta:
            print("\n[+] Metadata Ditemukan:")
            print(f"    Judul    : {meta.get('title')}")
            print(f"    Penulis  : {meta.get('authors')}")
            print(f"    Tahun    : {meta.get('year')}")
            print(f"    Venue    : {meta.get('venue')}")
            print(f"    Sumber   : {meta.get('api_source')}")
            if bib:
                print("\n[+] BibTeX:\n" + bib)
        else:
            print("[-] Gagal menemukan metadata untuk judul tersebut.")
        return

    # 3. File or Directory input
    if args.input:
        target_path = os.path.abspath(args.input)
        if not os.path.exists(target_path):
            print(f"[-] Error: Path input tidak ditemukan: {target_path}")
            sys.exit(1)

        targets = []
        if os.path.isdir(target_path):
            # Try top-level first
            pdf_top = glob.glob(os.path.join(target_path, "*.pdf"))
            md_top = glob.glob(os.path.join(target_path, "*.md"))
            targets.extend(pdf_top)
            targets.extend(md_top)

            # If user asked for recursive or top-level is empty, scan recursively
            if args.recursive or len(targets) == 0:
                rec_pdfs = glob.glob(os.path.join(target_path, "**/*.pdf"), recursive=True)
                rec_mds = glob.glob(os.path.join(target_path, "**/*.md"), recursive=True)
                for item in rec_pdfs + rec_mds:
                    if item not in targets:
                        targets.append(item)
        else:
            targets.append(target_path)

        if not targets:
            print(f"[-] Tidak ada berkas PDF atau Markdown yang ditemukan di {target_path}")
            sys.exit(1)

        print(f"[+] Ditemukan {len(targets)} berkas target.")
        batch_process_documents(
            targets,
            output_dir=args.output_dir,
            bibtex_filename=args.bibtex_file,
            preferred_api=args.api,
            force=args.force,
        )
        return

    parser.print_help()


if __name__ == "__main__":
    main()
