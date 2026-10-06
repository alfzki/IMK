#!/usr/bin/env python3
"""
scripts/convert_papers_to_markdown.py

Batch converts scientific PDFs into Markdown files for the Local RAG search engine.
Extracts sections, headings, text, and structure.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
PAPERS_DIR = WORKSPACE_ROOT / "references" / "papers"
MARKDOWN_DIR = WORKSPACE_ROOT / "references" / "markdown"


def convert_pdf_file(pdf_path: Path, output_dir: Path) -> Path:
    citekey = pdf_path.stem
    target_dir = output_dir / citekey
    target_dir.mkdir(parents=True, exist_ok=True)
    target_file = target_dir / f"{citekey}.md"

    try:
        import pypdf
        reader = pypdf.PdfReader(str(pdf_path))
        lines = [f"# {citekey}", ""]
        for idx, page in enumerate(reader.pages):
            text = page.extract_text()
            if text and text.strip():
                lines.append(f"\n<!-- Page {idx + 1} -->\n")
                lines.append(text.strip())
        content = "\n".join(lines)
    except Exception as e:
        print(f"[WARNING] Extraction error for {pdf_path.name}: {e}")
        content = f"# {citekey}\n\n[Full text pending extraction]"

    target_file.write_text(content, encoding="utf-8")
    return target_file


def main():
    parser = argparse.ArgumentParser(description="Convert reference PDFs to Markdown for RAG indexing")
    parser.add_argument("--pdf-dir", default=str(PAPERS_DIR), help="Directory containing PDF files")
    parser.add_argument("--out-dir", default=str(MARKDOWN_DIR), help="Directory to save Markdown files")
    parser.add_argument("--single", help="Convert a single PDF file")

    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.single:
        p = Path(args.single)
        if not p.exists():
            print(f"File not found: {args.single}")
            sys.exit(1)
        res = convert_pdf_file(p, out_dir)
        print(f"Converted {p.name} -> {res}")
        return

    pdf_dir = Path(args.pdf_dir)
    if not pdf_dir.exists():
        print(f"PDF directory does not exist: {pdf_dir}")
        return

    pdfs = list(pdf_dir.glob("*.pdf"))
    print(f"Found {len(pdfs)} PDF files in {pdf_dir}...")
    for p in pdfs:
        res = convert_pdf_file(p, out_dir)
        print(f"Converted: {p.name} -> {res}")


if __name__ == "__main__":
    main()
