#!/usr/bin/env python3
"""
scripts/query_references.py

Fast Local RAG & Citation Engine for Verified Scientific Research Papers.
Searches across Markdown-extracted papers (full text, tables, equations, sections),
BibTeX entries, and verified paper metadata without requiring external network calls.
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
REF_DIR = WORKSPACE_ROOT / "references"
MARKDOWN_DIR = REF_DIR / "markdown"
PAPERS_DIR = REF_DIR / "papers"
VERIFIED_JSON = REF_DIR / "verified_papers.json"
BIB_FILE = REF_DIR / "references_zotero_import.bib"
if not BIB_FILE.exists():
    BIB_FILE = WORKSPACE_ROOT / "literature" / "references.bib"


def load_metadata():
    if not VERIFIED_JSON.exists():
        return {}
    try:
        with open(VERIFIED_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return {}
    mapping = {}
    for p in data:
        fname = p.get("filename", "")
        citekey = fname.replace(".pdf", "") if fname else ""
        if citekey:
            mapping[citekey] = p
            mapping[citekey.lower()] = p
        pid = p.get("id")
        if pid:
            mapping[pid] = p
            mapping[pid.lower()] = p
    return mapping


def parse_markdown_sections(md_path):
    """Splits a markdown file into sections based on headers (#, ##, ###, ####)."""
    with open(md_path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    lines = text.split("\n")
    sections = []
    current_title = "Document Overview"
    current_lines = []

    for line in lines:
        if line.startswith("#"):
            if current_lines:
                sections.append({
                    "title": current_title,
                    "content": "\n".join(current_lines).strip()
                })
                current_lines = []
            current_title = line.lstrip("#").strip()
        else:
            current_lines.append(line)

    if current_lines:
        sections.append({
            "title": current_title,
            "content": "\n".join(current_lines).strip()
        })

    return sections


def search_papers(query, section_filter=None, limit=5):
    meta_map = load_metadata()
    terms = [t.lower() for t in query.split() if len(t) > 1]
    if not terms:
        terms = [query.lower()]

    results = []
    if not MARKDOWN_DIR.exists():
        print(f"Notice: {MARKDOWN_DIR} not found or empty.")
        return []

    paper_dirs = [d for d in MARKDOWN_DIR.iterdir() if d.is_dir()]
    for pdir in paper_dirs:
        citekey = pdir.name
        md_file = pdir / f"{citekey}.md"
        if not md_file.exists():
            continue

        meta = meta_map.get(citekey, {})
        sections = parse_markdown_sections(md_file)

        for sec in sections:
            sec_title = sec["title"]
            sec_content = sec["content"]

            if section_filter and not re.search(section_filter, sec_title, re.IGNORECASE):
                continue

            sec_lower = sec_content.lower()
            score = 0
            for term in terms:
                count = sec_lower.count(term)
                if count > 0:
                    score += count * (2 if term in sec_title.lower() else 1)

            if score > 0:
                first_pos = -1
                for term in terms:
                    pos = sec_lower.find(term)
                    if pos != -1 and (first_pos == -1 or pos < first_pos):
                        first_pos = pos

                start = max(0, first_pos - 150)
                end = min(len(sec_content), first_pos + 350)
                snippet = sec_content[start:end].replace("\n", " ").strip()
                if start > 0:
                    snippet = "..." + snippet
                if end < len(sec_content):
                    snippet = snippet + "..."

                results.append({
                    "citekey": citekey,
                    "title": meta.get("title", citekey),
                    "author": meta.get("author", ""),
                    "year": meta.get("year", ""),
                    "journal": meta.get("journal", ""),
                    "doi": meta.get("doi", ""),
                    "methods": meta.get("methods", ""),
                    "section": sec_title,
                    "score": score,
                    "snippet": snippet,
                    "md_path": str(md_file),
                    "pdf_path": str(PAPERS_DIR / f"{citekey}.pdf")
                })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:limit]


def get_paper_details(citekey):
    meta_map = load_metadata()
    meta = meta_map.get(citekey)
    if not meta:
        for k, v in meta_map.items():
            if citekey.lower() in k.lower():
                citekey = k
                meta = v
                break

    if not meta:
        return None

    md_file = MARKDOWN_DIR / citekey / f"{citekey}.md"
    pdf_file = PAPERS_DIR / f"{citekey}.pdf"

    latex_cite = f"\\cite{{{citekey}}}"
    markdown_cite = f"[@{citekey}]"

    return {
        "citekey": citekey,
        "title": meta.get("title", ""),
        "author": meta.get("author", ""),
        "year": meta.get("year", ""),
        "journal": meta.get("journal", ""),
        "doi": meta.get("doi", ""),
        "methods": meta.get("methods", ""),
        "relevance": meta.get("relevance", ""),
        "filesize_kb": meta.get("filesize_kb", 0),
        "latex_cite": latex_cite,
        "markdown_cite": markdown_cite,
        "pdf_path": str(pdf_file) if pdf_file.exists() else None,
        "md_path": str(md_file) if md_file.exists() else None
    }


def compare_all_papers():
    meta_map = load_metadata()
    comparison = []
    for citekey, meta in sorted(meta_map.items(), key=lambda x: str(x[1].get("year", "2024")), reverse=True):
        comparison.append({
            "citekey": citekey,
            "title": meta.get("title", ""),
            "author": meta.get("author", ""),
            "year": meta.get("year", ""),
            "journal": meta.get("journal", ""),
            "methods": meta.get("methods", ""),
            "relevance": meta.get("relevance", "")
        })
    return comparison


TOPIC_KEYWORDS = {
    "ucd": ["user centered design", "user-centred design", "ucd", "iso 9241-210", "interactive prototype", "figma", "wireframe"],
    "webqual": ["webqual", "webqual 4.0", "usability quality", "information quality", "service interaction quality", "barnes"],
    "heuristic": ["heuristic", "nielsen", "usability inspection", "severity rating", "10 heuristics"],
    "usability": ["usability", "sus", "system usability scale", "use questionnaire", "ueq", "user experience"],
    "government_portal": ["government", "e-government", "spbe", "public service", "pelayanan publik", "portal", "daerah"],
    "information_architecture": ["information architecture", "navigation", "card sorting", "tree testing", "search"],
    "emotional_design": ["emotional design", "norman", "visceral", "behavioral", "reflective", "cognitive load"]
}


def suggest_papers(topic):
    meta_map = load_metadata()
    topic_clean = topic.lower().strip()
    keywords = TOPIC_KEYWORDS.get(topic_clean, [topic_clean])

    matches = []
    seen = set()
    for citekey, meta in meta_map.items():
        doc_id = meta.get("id") or citekey
        if doc_id in seen:
            continue
        seen.add(doc_id)
        text = f"{meta.get('title', '')} {meta.get('methods', '')} {meta.get('relevance', '')}".lower()
        match_count = sum(text.count(kw) for kw in keywords)
        if match_count > 0:
            matches.append((match_count, doc_id, meta))

    matches.sort(key=lambda x: x[0], reverse=True)
    return [m[1] for m in matches]


def main():
    parser = argparse.ArgumentParser(description="Local Reference RAG & Citation Engine")
    parser.add_argument("--query", "-q", type=str, help="Search query across paper markdowns")
    parser.add_argument("--section", "-s", type=str, help="Regex filter for markdown section title")
    parser.add_argument("--citekey", "-c", type=str, help="Get detailed info and citations for a citekey")
    parser.add_argument("--compare", action="store_true", help="Compare all verified papers in a summary table")
    parser.add_argument("--suggest", type=str, help="Suggest papers for topic (ucd, webqual, heuristic, usability, government_portal, information_architecture, emotional_design)")
    parser.add_argument("--limit", "-n", type=int, default=5, help="Max results to return")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")

    args = parser.parse_args()

    if args.citekey:
        detail = get_paper_details(args.citekey)
        if not detail:
            print(f"Citekey '{args.citekey}' tidak ditemukan.")
            sys.exit(1)
        if args.json:
            print(json.dumps(detail, indent=2, ensure_ascii=False))
        else:
            print("\n" + "="*80)
            print(f"Judul     : {detail['title']}")
            print(f"Citekey   : {detail['citekey']}")
            print(f"Penulis   : {detail['author']}")
            print(f"Tahun/Jrn : {detail['year']} | {detail['journal']}")
            print(f"DOI       : https://doi.org/{detail['doi']}")
            print(f"Metode    : {detail['methods']}")
            print(f"Relevansi : {detail['relevance']}")
            print(f"Sitasi    : LaTeX -> {detail['latex_cite']} | Markdown -> {detail['markdown_cite']}")
            print(f"Berkas MD : {detail['md_path']}")
            print(f"Berkas PDF: {detail['pdf_path']}")
            print("="*80 + "\n")
        return

    if args.compare:
        comp = compare_all_papers()
        if args.json:
            print(json.dumps(comp, indent=2, ensure_ascii=False))
        else:
            print(f"\n{'No':<3} | {'Citekey':<45} | {'Tahun':<5} | {'Metode Utama'}")
            print("-" * 100)
            for i, p in enumerate(comp, 1):
                print(f"{i:<3} | {p['citekey'][:45]:<45} | {p['year']:<5} | {p['methods'][:45]}")
        return

    if args.suggest:
        keys = suggest_papers(args.suggest)
        if args.json:
            print(json.dumps(keys, indent=2))
        else:
            print(f"\nRekomendasi paper untuk topik '{args.suggest}':")
            meta_map = load_metadata()
            for k in keys:
                m = meta_map.get(k, {})
                print(f"- \\cite{{{k}}}: {m.get('title')} ({m.get('year')})")
        return

    if args.query:
        res = search_papers(args.query, section_filter=args.section, limit=args.limit)
        if args.json:
            print(json.dumps(res, indent=2, ensure_ascii=False))
        else:
            if not res:
                print("Tidak ada hasil yang ditemukan.")
                return
            print(f"\nMenemukan {len(res)} hasil relevan:\n" + "="*80)
            for idx, r in enumerate(res, 1):
                print(f"[{idx}] {r['title']} ({r['year']})")
                print(f"    Citekey : {r['citekey']}")
                print(f"    Penulis : {r['author']}")
                print(f"    Jurnal  : {r['journal']} | DOI: {r['doi']}")
                print(f"    Bagian  : {r['section']} (Score: {r['score']})")
                print(f"    Kutipan :\n    \"{r['snippet']}\"")
                print(f"    Berkas  : {r['md_path']}")
                print("-" * 80)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
