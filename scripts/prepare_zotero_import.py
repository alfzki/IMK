#!/usr/bin/env python3
"""
scripts/prepare_zotero_import.py

Prepares enriched BibTeX and RIS files for 1-click import into Zotero Desktop.
Attaches local PDF paths, abstracts, keywords, and methodological notes so Zotero indexes everything automatically.
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
REF_DIR = WORKSPACE_ROOT / "references"
PAPERS_DIR = REF_DIR / "papers"
VERIFIED_JSON = REF_DIR / "verified_papers.json"
OUTPUT_BIB = REF_DIR / "references_zotero_import.bib"
OUTPUT_RIS = REF_DIR / "references_zotero_import.ris"


def load_verified_papers():
    if not VERIFIED_JSON.exists():
        return []
    try:
        with open(VERIFIED_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def generate_bibtex_entry(p: dict) -> str:
    citekey = p.get("id") or p.get("filename", "").replace(".pdf", "")
    fname = p.get("filename", "")
    pdf_path = PAPERS_DIR / fname if fname else ""
    doi = p.get("doi", "").strip()
    url = p.get("url", "").strip()
    if not url and doi:
        url = f"https://doi.org/{doi}"

    entry_type = "article"
    ptype = p.get("type", "")
    if ptype in ["conference", "ieee", "acm"]:
        entry_type = "inproceedings"
    elif ptype in ["book_chapter", "classic"] and p.get("isbn"):
        entry_type = "incollection"
    elif ptype == "regulation":
        entry_type = "misc"
    elif ptype == "ipdn":
        entry_type = "techreport"

    lines = [f"@{entry_type}{{{citekey},"]
    lines.append(f"  author = {{{p.get('author', 'Unknown')}}},")
    lines.append(f"  title = {{{{{p.get('title', 'Untitled')}}}}},")
    if entry_type in ["inproceedings"]:
        lines.append(f"  booktitle = {{{p.get('journal', 'Conference Proceedings')}}},")
    else:
        lines.append(f"  journal = {{{p.get('journal', 'Academic Journal')}}},")
    lines.append(f"  year = {{{p.get('year', 2024)}}},")
    if doi:
        lines.append(f"  doi = {{{doi}}},")
    if url:
        lines.append(f"  url = {{{url}}},")
    if fname:
        lines.append(f"  file = {{{fname}:{pdf_path}:application/pdf}},")
    lines.append(f"  abstract = {{Metode: {p.get('methods', '')}. Relevansi: {p.get('relevance', '')}}},")
    lines.append("  keywords = {Human-Computer Interaction; Usability; WebQual 4.0; User-Centered Design; Information Systems; Evaluation},")
    lines.append(f"  note = {{Dataset/Metode: {p.get('methods', '')}}}")
    lines.append("}\n")
    return "\n".join(lines)


def generate_ris_entry(p: dict) -> str:
    citekey = p.get("id") or p.get("filename", "").replace(".pdf", "")
    fname = p.get("filename", "")
    pdf_path = PAPERS_DIR / fname if fname else ""
    doi = p.get("doi", "").strip()
    url = p.get("url", "").strip()
    if not url and doi:
        url = f"https://doi.org/{doi}"

    ptype = p.get("type", "")
    ty = "JOUR"
    if ptype in ["conference", "ieee", "acm"]:
        ty = "CONF"
    elif ptype in ["book_chapter", "classic"]:
        ty = "CHAP"
    elif ptype in ["regulation", "ipdn"]:
        ty = "RPRT"

    ris_lines = [
        f"TY  - {ty}",
        f"ID  - {citekey}"
    ]
    for auth in p.get("author", "").split(","):
        auth_clean = auth.strip()
        if auth_clean and auth_clean.lower() != "et al.":
            ris_lines.append(f"AU  - {auth_clean}")

    ris_lines.extend([
        f"TI  - {p.get('title', '')}",
        f"JO  - {p.get('journal', '')}",
        f"PY  - {p.get('year', '')}",
    ])
    if doi:
        ris_lines.append(f"DO  - {doi}")
    if url:
        ris_lines.append(f"UR  - {url}")
    ris_lines.extend([
        f"AB  - Metode: {p.get('methods', '')}. Relevansi: {p.get('relevance', '')}",
        "KW  - Human-Computer Interaction",
        "KW  - Usability",
        "KW  - WebQual 4.0",
        "KW  - User-Centered Design",
        "KW  - Information Systems",
    ])
    if fname:
        ris_lines.append(f"L1  - {pdf_path}")
    ris_lines.append("ER  - \n")
    return "\n".join(filter(bool, ris_lines))


def main():
    papers = load_verified_papers()
    print(f"Loading {len(papers)} verified papers from {VERIFIED_JSON}...")

    REF_DIR.mkdir(parents=True, exist_ok=True)

    bib_entries = [generate_bibtex_entry(p) for p in papers]
    bib_content = "\n".join(bib_entries)
    OUTPUT_BIB.write_text(bib_content, encoding="utf-8")
    print(f"Enriched BibTeX written to: {OUTPUT_BIB}")

    # Also synchronize literature/references.bib
    lit_bib = WORKSPACE_ROOT / "literature" / "references.bib"
    lit_bib.parent.mkdir(parents=True, exist_ok=True)
    lit_bib.write_text(bib_content, encoding="utf-8")
    print(f"Synchronized BibTeX written to: {lit_bib}")

    ris_entries = [generate_ris_entry(p) for p in papers]
    OUTPUT_RIS.write_text("\n".join(ris_entries), encoding="utf-8")
    print(f"Enriched RIS written to: {OUTPUT_RIS}")

    print("\n✅ Persiapan berkas impor Zotero selesai!")


if __name__ == "__main__":
    main()
