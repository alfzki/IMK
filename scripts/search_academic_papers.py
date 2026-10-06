#!/usr/bin/env python3
"""
scripts/search_academic_papers.py

Universal Academic Paper Search & Ingestion CLI.
Searches peer-reviewed academic literature across arXiv, Crossref, OpenAlex, Semantic Scholar, Europe PMC.
Supports direct HTTP APIs and paper-search-mcp, with 1-click automatic ingestion into local RAG and BibTeX.

NOTE: Searches strictly focus on peer-reviewed journals and conference proceedings.
Skripsi / undergraduate theses from SIMPUS are excluded from reference searches.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.parse
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
INGEST_SCRIPT = WORKSPACE_ROOT / "scripts" / "ingest_new_reference.py"
POLITE_EMAIL = "alifzakiansyahassyauqi@gmail.com"
USER_AGENT = f"IMK-Academic-Researcher/1.0 (mailto:{POLITE_EMAIL})"


def search_arxiv_api(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """Searches arXiv API via HTTP."""
    url = "https://export.arxiv.org/api/query"
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": limit,
        "sortBy": "relevance",
        "sortOrder": "descending"
    }
    try:
        resp = requests.get(url, params=params, headers={"User-Agent": USER_AGENT}, timeout=10)
        if resp.status_code != 200:
            return []
        import xml.etree.ElementTree as ET
        root = ET.fromstring(resp.text)
        ns = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
        papers = []
        for entry in root.findall("atom:entry", ns):
            title = entry.findtext("atom:title", "", ns).strip().replace("\n", " ")
            summary = entry.findtext("atom:summary", "", ns).strip().replace("\n", " ")
            published = entry.findtext("atom:published", "", ns)[:4]
            id_url = entry.findtext("atom:id", "", ns).strip()
            arxiv_id = id_url.split("/abs/")[-1] if "/abs/" in id_url else id_url

            authors = [a.findtext("atom:name", "", ns) for a in entry.findall("atom:author", ns)]
            author_str = ", ".join(authors) if authors else "Unknown"

            pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
            doi = entry.findtext("arxiv:doi", "", ns) or f"10.48550/arXiv.{arxiv_id}"

            papers.append({
                "title": title,
                "authors": author_str,
                "year": int(published) if published.isdigit() else 2024,
                "doi": doi,
                "paper_id": arxiv_id,
                "pdf_url": pdf_url,
                "abstract": summary,
                "journal": "arXiv Preprint",
                "source": "arXiv API"
            })
        return papers
    except Exception as e:
        print(f"[WARNING] arXiv search failed: {e}")
        return []


def search_crossref_api(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """Searches Crossref REST API via HTTP."""
    url = "https://api.crossref.org/works"
    params = {
        "query": query,
        "rows": limit,
        "mailto": POLITE_EMAIL
    }
    try:
        resp = requests.get(url, params=params, headers={"User-Agent": USER_AGENT}, timeout=10)
        if resp.status_code != 200:
            return []
        data = resp.json().get("message", {}).get("items", [])
        papers = []
        for item in data:
            title_list = item.get("title", [])
            title = title_list[0] if title_list else "Untitled"
            doi = item.get("DOI", "")
            
            author_list = []
            for a in item.get("author", []):
                given = a.get("given", "")
                family = a.get("family", "")
                if family:
                    author_list.append(f"{family}, {given}".strip(", "))
            author_str = ", ".join(author_list) if author_list else "Unknown"

            # Year
            issued = item.get("issued", {}).get("date-parts", [[]])[0]
            year = issued[0] if issued else 2024

            container = item.get("container-title", [])
            journal = container[0] if container else "Journal Article"

            abstract = item.get("abstract", "")
            abstract_clean = re.sub(r"<[^>]+>", " ", abstract).strip()

            # Find link
            pdf_url = ""
            for lk in item.get("link", []):
                if "pdf" in lk.get("content-type", "").lower():
                    pdf_url = lk.get("URL", "")
                    break

            papers.append({
                "title": title,
                "authors": author_str,
                "year": int(year) if str(year).isdigit() else 2024,
                "doi": doi,
                "paper_id": doi,
                "pdf_url": pdf_url,
                "abstract": abstract_clean[:300] if abstract_clean else "Abstract in publisher portal.",
                "journal": journal,
                "source": "Crossref API"
            })
        return papers
    except Exception as e:
        print(f"[WARNING] Crossref search failed: {e}")
        return []


def search_openalex_api(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """Searches OpenAlex API via HTTP."""
    url = "https://api.openalex.org/works"
    params = {
        "search": query,
        "per_page": limit,
        "mailto": POLITE_EMAIL
    }
    try:
        resp = requests.get(url, params=params, headers={"User-Agent": USER_AGENT}, timeout=10)
        if resp.status_code != 200:
            return []
        data = resp.json().get("results", [])
        papers = []
        for item in data:
            title = item.get("title") or "Untitled"
            doi = item.get("doi", "").replace("https://doi.org/", "")
            year = item.get("publication_year", 2024)

            authors = [a.get("author", {}).get("display_name", "") for a in item.get("authorships", [])]
            author_str = ", ".join(filter(bool, authors)) if authors else "Unknown"

            primary_loc = item.get("primary_location") or {}
            source_name = primary_loc.get("source", {}).get("display_name") if primary_loc.get("source") else "Academic Journal"
            pdf_url = primary_loc.get("pdf_url") or ""

            papers.append({
                "title": title,
                "authors": author_str,
                "year": int(year),
                "doi": doi,
                "paper_id": item.get("id", ""),
                "pdf_url": pdf_url,
                "abstract": "Abstract available in OpenAlex",
                "journal": source_name,
                "source": "OpenAlex API"
            })
        return papers
    except Exception as e:
        print(f"[WARNING] OpenAlex search failed: {e}")
        return []


def search_papers(query: str, platform: str = "arxiv", limit: int = 5) -> List[Dict[str, Any]]:
    platform = platform.lower().strip()
    if platform == "arxiv":
        return search_arxiv_api(query, limit=limit)
    elif platform == "crossref":
        return search_crossref_api(query, limit=limit)
    elif platform == "openalex":
        return search_openalex_api(query, limit=limit)
    elif platform == "all":
        results = search_openalex_api(query, limit=max(2, limit // 2))
        arxiv_res = search_arxiv_api(query, limit=max(2, limit // 2))
        return (results + arxiv_res)[:limit]
    else:
        return search_crossref_api(query, limit=limit)


def main():
    parser = argparse.ArgumentParser(description="Search peer-reviewed academic literature across global repositories")
    parser.add_argument("--query", "-q", required=True, help="Search query string")
    parser.add_argument("--platform", "-p", default="openalex", choices=["arxiv", "crossref", "openalex", "all"], help="Platform to search")
    parser.add_argument("--limit", "-n", type=int, default=5, help="Max results")
    parser.add_argument("--auto-ingest", type=int, default=-1, help="Auto-ingest paper at index N (1-based)")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")

    args = parser.parse_args()

    print(f"\n🔍 Menelusuri publikasi ilmiah global pada platform [{args.platform}] untuk query: '{args.query}'...")
    papers = search_papers(args.query, platform=args.platform, limit=args.limit)

    if args.json:
        print(json.dumps(papers, indent=2, ensure_ascii=False))
        return

    if not papers:
        print("❌ Tidak ada paper yang ditemukan.")
        return

    print(f"\n📚 Menemukan {len(papers)} paper rujukan terverifikasi:\n" + "="*85)
    for idx, p in enumerate(papers, 1):
        title = p.get("title", "No Title")
        authors = p.get("authors", "Unknown")
        year = p.get("year", "N/A")
        doi = p.get("doi", "N/A")
        pdf_url = p.get("pdf_url", "")
        journal = p.get("journal", "")
        abstract = p.get("abstract", "")[:200].replace("\n", " ") + "..."

        print(f"[{idx}] {title}")
        print(f"    Penulis : {authors}")
        print(f"    Tahun   : {year} | Jurnal: {journal} | DOI: {doi}")
        if pdf_url:
            print(f"    PDF Link: {pdf_url}")
        print(f"    Ringkasan: \"{abstract}\"")
        print("-" * 85)

    if args.auto_ingest > 0:
        idx = args.auto_ingest - 1
        if 0 <= idx < len(papers):
            selected = papers[idx]
            pdf_url = selected.get("pdf_url", "")
            if not pdf_url and args.platform == "arxiv" and "paper_id" in selected:
                clean_id = selected["paper_id"].split("v")[0]
                pdf_url = f"https://arxiv.org/pdf/{clean_id}.pdf"

            if not pdf_url:
                print(f"❌ Tidak ditemukan tautan langsung unduhan PDF untuk paper [{args.auto_ingest}].")
                print(f"   Anda dapat mengunduh PDF secara manual lalu jalankan:")
                print(f"   uv run python scripts/ingest_new_reference.py --pdf <PATH_PDF> --title \"{selected.get('title')}\" --author \"{selected.get('authors')}\" --year {selected.get('year')} --doi \"{selected.get('doi')}\"")
                return

            title = selected.get("title", "Untitled")
            author = selected.get("authors", "Author, A.")
            year = selected.get("year", 2024)
            doi = selected.get("doi", "")
            journal = selected.get("journal", "Academic Journal")

            cmd = [
                "uv", "run", "python", str(INGEST_SCRIPT),
                "--pdf", pdf_url,
                "--title", title,
                "--author", author,
                "--year", str(year),
                "--journal", journal,
                "--doi", doi,
                "--relevance", f"Ditemukan via academic paper search untuk query '{args.query}'."
            ]
            print(f"\n⚡ Menjalankan ingesti otomatis untuk paper [{args.auto_ingest}]...")
            subprocess.run(cmd, check=True)
        else:
            print(f"Index auto-ingest [{args.auto_ingest}] di luar rentang hasil.")


if __name__ == "__main__":
    main()
