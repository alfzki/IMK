#!/usr/bin/env python3
"""
scripts/ingest_new_reference.py

Automated Ingestion Pipeline for newly downloaded scientific research papers:
1. Local PDF repository (references/papers/<citekey>.pdf)
2. Local Markdown RAG engine (references/markdown/<citekey>/<citekey>.md)
3. Verified papers database (references/verified_papers.json)
4. BibTeX databases for LaTeX and Zotero import (literature/references.bib, references/references_zotero_import.bib)
5. RIS database (references/references_zotero_import.ris)

NOTE: Skripsi / SIMPUS theses are strictly disallowed as references for scientific papers.
Only peer-reviewed journal articles, conference papers, preprints, and scholarly books are accepted.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import urllib.request
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
REF_DIR = WORKSPACE_ROOT / "references"
PAPERS_DIR = REF_DIR / "papers"
MARKDOWN_DIR = REF_DIR / "markdown"
VERIFIED_JSON = REF_DIR / "verified_papers.json"
BIB_FILE = WORKSPACE_ROOT / "literature" / "references.bib"
ZOTERO_BIB = REF_DIR / "references_zotero_import.bib"
ZOTERO_RIS = REF_DIR / "references_zotero_import.ris"


def is_simpus_or_thesis(title: str, url: str, methods: str, relevance: str) -> bool:
    """Checks if the reference is an unvetted university skripsi/thesis or SIMPUS source."""
    combined = f"{title} {url} {methods} {relevance}".lower()
    if "simpus.stis.ac.id" in combined or "repositori.stis" in combined:
        return True
    if re.search(r"\bskripsi\b", combined, re.IGNORECASE):
        return True
    if re.search(r"\bmastersthesis\b", combined, re.IGNORECASE):
        return True
    return False


def generate_citekey(author: str, year: int, title: str) -> str:
    first_author = author.split(",")[0].strip()
    tokens = first_author.split()
    surname = tokens[-1] if len(tokens) > 1 and "," not in author else tokens[0]
    surname = re.sub(r"[^\w]", "", surname)

    title_words = [re.sub(r"[^\w]", "", w) for w in title.split() if len(w) > 3]
    stopwords = {"study", "using", "through", "based", "approach", "novel", "analysis", "evidence", "towards", "comparative"}
    keywords = [w.capitalize() for w in title_words if w.lower() not in stopwords][:3]
    key_suffix = "_".join(keywords) if keywords else "Paper"

    return f"{surname}_{year}_{key_suffix}"


def download_or_copy_pdf(src_path_or_url: str, dest_path: Path) -> float:
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    if src_path_or_url.startswith("http://") or src_path_or_url.startswith("https://"):
        print(f"Downloading PDF from: {src_path_or_url}...")
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        req = urllib.request.Request(src_path_or_url, headers=headers)
        with urllib.request.urlopen(req) as resp, open(dest_path, "wb") as out:
            shutil.copyfileobj(resp, out)
    else:
        src = Path(src_path_or_url)
        if not src.exists():
            raise FileNotFoundError(f"PDF source file not found: {src_path_or_url}")
        shutil.copy2(src, dest_path)

    size_kb = os.path.getsize(dest_path) / 1024
    print(f"Saved PDF to {dest_path} ({size_kb:.1f} KB)")
    return size_kb


def extract_pdf_to_markdown(pdf_path: Path, output_md_dir: Path, citekey: str) -> Path:
    output_md_dir.mkdir(parents=True, exist_ok=True)
    out_file = output_md_dir / f"{citekey}.md"

    # Strategy 1: Try pypdf / pypdfium2
    extracted_text = ""
    try:
        import pypdf
        reader = pypdf.PdfReader(str(pdf_path))
        num_pages = len(reader.pages)
        md_lines = [f"# {citekey}", ""]
        for page_idx, page in enumerate(reader.pages):
            text = page.extract_text()
            if text and text.strip():
                md_lines.append(f"\n<!-- Page {page_idx + 1} -->\n")
                md_lines.append(text.strip())
        extracted_text = "\n".join(md_lines)
    except Exception as e:
        print(f"[WARNING] Extraction via pypdf encountered error: {e}")

    if not extracted_text.strip():
        extracted_text = f"# {citekey}\n\n[Full-text extraction pending]"

    out_file.write_text(extracted_text, encoding="utf-8")
    print(f"Extracted markdown saved to: {out_file}")

    meta_json_file = output_md_dir / f"{citekey}_meta.json"
    meta_data = {
        "filetype": "pdf",
        "citekey": citekey
    }
    meta_json_file.write_text(json.dumps(meta_data, indent=2), encoding="utf-8")
    return out_file


def update_verified_json(paper_record: dict) -> None:
    data = []
    if VERIFIED_JSON.exists():
        try:
            with open(VERIFIED_JSON, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = []

    existing_idx = next((i for i, p in enumerate(data) if p.get("filename") == paper_record["filename"]), None)
    if existing_idx is not None:
        data[existing_idx] = paper_record
        print(f"Updated existing entry in {VERIFIED_JSON}")
    else:
        data.append(paper_record)
        print(f"Appended new entry to {VERIFIED_JSON} (Total: {len(data)} papers)")

    VERIFIED_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(VERIFIED_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def append_to_bibtex_files(citekey: str, author: str, title: str, journal: str, year: int, doi: str, url: str, methods: str, relevance: str, pdf_path: Path):
    bib_entry = f"""
@article{{{citekey},
  author = {{{author}}},
  title = {{{{{title}}}}},
  journal = {{{journal}}},
  year = {{{year}}},
  doi = {{{doi}}},
  url = {{{url}}},
  file = {{{pdf_path.name}:{pdf_path}:application/pdf}},
  abstract = {{Metode: {methods}. Relevansi: {relevance}}},
  keywords = {{Human-Computer Interaction; Usability; WebQual 4.0; User-Centered Design; Information Systems; Evaluation}},
  note = {{Methods: {methods} | Ingested via Academic Ingestion Pipeline}}
}}
"""
    for bf in [BIB_FILE, ZOTERO_BIB]:
        bf.parent.mkdir(parents=True, exist_ok=True)
        existing = bf.read_text(encoding="utf-8") if bf.exists() else ""
        if f"@{citekey}," not in existing and f"{{{citekey}," not in existing:
            with open(bf, "a", encoding="utf-8") as f:
                f.write(bib_entry)
            print(f"Appended entry to {bf}")


def append_to_ris(citekey: str, author: str, title: str, journal: str, year: int, doi: str, methods: str, relevance: str, pdf_path: Path):
    ZOTERO_RIS.parent.mkdir(parents=True, exist_ok=True)
    ris_entry = f"""
TY  - JOUR
ID  - {citekey}
"""
    for auth in author.split(","):
        auth_clean = auth.strip()
        if auth_clean and auth_clean.lower() != "et al.":
            ris_entry += f"AU  - {auth_clean}\n"

    ris_entry += f"""TI  - {title}
JO  - {journal}
PY  - {year}
DO  - {doi}
UR  - https://doi.org/{doi} if doi else ""
AB  - Metode: {methods}. Relevansi: {relevance}
KW  - Human-Computer Interaction
KW  - Usability
KW  - WebQual 4.0
KW  - User-Centered Design
KW  - Information Systems
L1  - {pdf_path}
ER  - 
"""
    with open(ZOTERO_RIS, "a", encoding="utf-8") as f:
        f.write(ris_entry)
    print(f"Appended entry to {ZOTERO_RIS}")


def main():
    parser = argparse.ArgumentParser(description="Ingest new research paper into local RAG and reference library")
    parser.add_argument("--pdf", required=True, help="Local PDF path or direct download URL")
    parser.add_argument("--title", required=True, help="Paper title")
    parser.add_argument("--author", required=True, help="Authors string (e.g. 'Smith, J., Doe, A.')")
    parser.add_argument("--year", type=int, required=True, help="Publication year")
    parser.add_argument("--journal", default="Academic Journal", help="Journal/Conference name")
    parser.add_argument("--doi", default="", help="Digital Object Identifier")
    parser.add_argument("--url", default="", help="Publication URL")
    parser.add_argument("--methods", default="User-Centered Design, WebQual 4.0, Heuristic Evaluation, Usability Testing", help="Methods summary")
    parser.add_argument("--relevance", default="Menyediakan bukti literatur pendukung untuk artikel ilmiah.", help="Research relevance")
    parser.add_argument("--citekey", default="", help="Custom citekey (optional)")

    args = parser.parse_args()

    # Disallow SIMPUS or skripsi
    if is_simpus_or_thesis(args.title, args.url, args.methods, args.relevance):
        print("\n❌ [ERROR]: Penggunaan skripsi alumni atau SIMPUS STIS dilarang sebagai referensi artikel ilmiah.")
        print("   Artikel ilmiah hanya menerima rujukan dari jurnal ilmiah bereputasi, prosiding konferensi, atau preprint resmi.")
        sys.exit(1)

    citekey = args.citekey.strip() if args.citekey else generate_citekey(args.author, args.year, args.title)
    pdf_dest = PAPERS_DIR / f"{citekey}.pdf"
    md_dest_dir = MARKDOWN_DIR / citekey
    url = args.url if args.url else (f"https://doi.org/{args.doi}" if args.doi else "")

    print("\n" + "="*80)
    print(f"🚀 MEMPROSES INGESTI REFERENSI BARU: {citekey}")
    print("="*80)

    # 1. Download/Copy PDF
    size_kb = download_or_copy_pdf(args.pdf, pdf_dest)

    # 2. Extract to Markdown
    extract_pdf_to_markdown(pdf_dest, md_dest_dir, citekey)

    # 3. Update verified papers json
    paper_rec = {
        "id": args.doi if args.doi else citekey,
        "type": "external_ingested",
        "filename": f"{citekey}.pdf",
        "title": args.title,
        "author": args.author,
        "year": args.year,
        "journal": args.journal,
        "doi": args.doi,
        "methods": args.methods,
        "relevance": args.relevance,
        "local_path": f"references/papers/{citekey}.pdf",
        "filesize_kb": round(size_kb, 1)
    }
    update_verified_json(paper_rec)

    # 4. Append BibTeX & RIS
    append_to_bibtex_files(citekey, args.author, args.title, args.journal, args.year, args.doi, url, args.methods, args.relevance, pdf_dest)
    append_to_ris(citekey, args.author, args.title, args.journal, args.year, args.doi, args.methods, args.relevance, pdf_dest)

    print("\n" + "="*80)
    print("✅ INGESTI BERHASIL!")
    print(f"  • Citekey     : {citekey}")
    print(f"  • Sitasi LaTeX: \\cite{{{citekey}}}")
    print(f"  • Sitasi APA  : {args.author.split(',')[0].strip()} ({args.year})")
    print(f"  • Berkas PDF  : {pdf_dest}")
    print(f"  • Berkas MD   : {md_dest_dir / f'{citekey}.md'}")
    print(f"  • Status RAG  : Siap dicari via scripts/query_references.py")
    print(f"  • Status Zotero: Tercatat di {ZOTERO_BIB}")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
