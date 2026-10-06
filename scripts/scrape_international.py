#!/usr/bin/env python3
"""
International Literature & Multi-Archive Scraper
Fetches scientific papers, preprints, and public-domain monographs from:
- OpenAlex & arXiv (Core baseline)
- Semantic Scholar (AI/CS/Stat graph)
- CORE (Connecting Repositories - world's largest open access repository aggregator)
- Internet Archive / Open Library (Digital texts, proceedings, books)
- Project Gutenberg (Public domain textbooks & classic treatises)
- Sci-Hub & Library Genesis (Paywall resolver fallback & shadow catalog)
- Anna's Archive (Aggregated meta-search)
- IPFS (Decentralized content transport)
- Z-Library (via open public proxy)
"""

import argparse
import csv
import json
import os
import re
import shutil
import sys
import time
from typing import Dict, List, Optional

# Auto-reexec into project .venv if run with system python
try:
    import pyalex
    from pyalex import Works
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
    print("Error: Missing required packages (pyalex, requests, tqdm).")
    print("Please run using: uv run python " + " ".join(sys.argv))
    sys.exit(1)

# Ensure scripts and src directory are in sys.path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
src_dir = os.path.join(project_root, "src")
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from calm_carson.archives import ArchiveManager, CascadingPaperDownloader, PaperRecord

# Configure pyalex polite pool
pyalex.config.email = "alifzakiansyahassyauqi@gmail.com"


def trigger_md_conversion(pdf_path: str, output_base_dir: str = "literature/markdowns"):
    """Converts a downloaded PDF to Markdown using convert_pdf_to_md module (Marker GPU)."""
    try:
        from convert_pdf_to_md import convert_pdf_to_markdown
        print(f"        [*] Mengonversi PDF ke Markdown via Marker (GPU RTX 4050)...")
        md_file = convert_pdf_to_markdown(pdf_path, output_base_dir=output_base_dir)
        if md_file:
            print(f"        [+] Markdown tersimpan: {md_file}")
    except Exception as e:
        print(f"        [!] Konversi Markdown dilewati: {e}")


TOPIC_PRESETS = {
    "1": {
        "name": "Deteksi Anomali & Anti-Falsifikasi Entri Survei Lapangan (CAPI)",
        "openalex_title": "survey falsification",
        "openalex_general": "survey data collection paradata anomaly detection curbstoning",
        "arxiv_query": 'all:"survey falsification" OR all:"curbstoning"',
    },
    "2": {
        "name": "Secure Ingestion Gateway & Metadata Satu Data Indonesia (SDI)",
        "openalex_title": "API gateway metadata",
        "openalex_general": "data ingestion API gateway metadata schema validation zero trust",
        "arxiv_query": 'all:"API gateway" AND all:"metadata"',
    },
    "3": {
        "name": "Layanan Data Mikro & Dynamic Differential Privacy (UU PDP)",
        "openalex_title": "differential privacy microdata",
        "openalex_general": "differential privacy statistical disclosure control census microdata",
        "arxiv_query": 'all:"differential privacy" AND all:"microdata"',
    }
}


def invert_abstract(inverted_index: Optional[Dict[str, List[int]]]) -> str:
    """Reconstructs full text abstract from OpenAlex inverted index structure."""
    if not inverted_index:
        return ""
    pos_word = []
    for word, positions in inverted_index.items():
        for pos in positions:
            pos_word.append((pos, word))
    pos_word.sort(key=lambda x: x[0])
    text = " ".join(w for _, w in pos_word)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def sanitize_filename(title: str, max_len: int = 80) -> str:
    """Cleans a string to make it safe for filenames."""
    clean = re.sub(r'[\\/*?:"<>|]', "", title)
    clean = re.sub(r"\s+", "_", clean).strip("_")
    return clean[:max_len]


def search_openalex(
    query: str,
    title_query: Optional[str] = None,
    min_year: int = 2021,
    max_year: int = 2026,
    limit: int = 10
) -> List[Dict]:
    """Queries OpenAlex API using pyalex for scientific literature."""
    print(f"[*] [OpenAlex] Mencari publikasi di database ilmiah ({min_year}–{max_year})...")
    results = []
    seen_ids = set()

    from_date = f"{min_year}-01-01"
    to_date = f"{max_year}-12-31"

    # Step 1: Search by title if available (high precision)
    if title_query:
        try:
            works_title = (
                Works()
                .filter(title={"search": title_query})
                .filter(from_publication_date=from_date, to_publication_date=to_date)
                .sort(cited_by_count="desc")
                .get(per_page=limit)
            )
            for w in works_title:
                w_id = w.get("id")
                if w_id and w_id not in seen_ids:
                    seen_ids.add(w_id)
                    results.append(w)
        except Exception as e:
            print(f"    [i] Info: Title query '{title_query}' catatan: {e}")

    # Step 2: Supplement with general search if limit not yet reached
    if len(results) < limit and query:
        try:
            needed = limit - len(results)
            works_gen = (
                Works()
                .search(query)
                .filter(from_publication_date=from_date, to_publication_date=to_date)
                .sort(cited_by_count="desc")
                .get(per_page=needed * 2)
            )
            for w in works_gen:
                w_id = w.get("id")
                if w_id and w_id not in seen_ids:
                    seen_ids.add(w_id)
                    results.append(w)
                if len(results) >= limit:
                    break
        except Exception as e:
            print(f"    [i] Info: General query catatan: {e}")

    processed = []
    for w in results[:limit]:
        authors = []
        for authorship in w.get("authorships", []):
            author_obj = authorship.get("author", {})
            if author_obj.get("display_name"):
                authors.append(author_obj["display_name"])

        primary_loc = w.get("primary_location") or {}
        source_obj = primary_loc.get("source") or {}
        venue_name = source_obj.get("display_name") or "Jurnal / Konferensi Terindeks"

        oa_obj = w.get("open_access") or {}
        oa_url = oa_obj.get("oa_url") or primary_loc.get("pdf_url")

        topics_list = [t.get("display_name", "") for t in w.get("topics", []) if t.get("display_name")]

        clean_doi = (w.get("doi") or "").replace("https://doi.org/", "")

        record = {
            "id": w.get("id", "").replace("https://openalex.org/", ""),
            "source": "OpenAlex",
            "source_tier": 1,
            "category": "paper",
            "title": w.get("title") or "Untitled",
            "authors": ", ".join(authors[:5]) + (" et al." if len(authors) > 5 else ""),
            "authors_list": authors,
            "year": w.get("publication_year"),
            "venue": venue_name,
            "doi": clean_doi,
            "citations": w.get("cited_by_count", 0),
            "is_oa": oa_obj.get("is_oa", False),
            "pdf_url": oa_url or "",
            "abstract": invert_abstract(w.get("abstract_inverted_index")),
            "keywords": ", ".join(topics_list[:4]),
            "url": w.get("doi") or w.get("id") or "",
        }
        processed.append(record)

    print(f"[+] [OpenAlex] Berhasil mengambil {len(processed)} artikel bereputasi.")
    return processed


def search_arxiv(query: str, min_year: int = 2021, max_year: int = 2026, limit: int = 10) -> List[Dict]:
    """Queries arXiv API for preprints with polite handling."""
    print(f"[*] [arXiv] Mencari preprint di arXiv.org: '{query}'...")
    results = []
    
    try:
        import urllib.request, urllib.parse, xml.etree.ElementTree as ET
        params = {
            "search_query": query,
            "start": "0",
            "max_results": str(limit * 2),
            "sortBy": "relevance",
            "sortOrder": "descending",
        }
        url = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode(params)
        headers = {
            "User-Agent": "calm-carson-researcher/1.0 (mailto:alifzakiansyahassyauqi@gmail.com)",
        }
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=6) as resp:
            content = resp.read()
            if b"Rate exceeded" in content:
                print("    [i] Info: arXiv rate limit sedang aktif. Mengandalkan OpenAlex.")
                return results

            root = ET.fromstring(content)
            entries = root.findall("{http://www.w3.org/2005/Atom}entry")
            for e in entries:
                published_str = e.find("{http://www.w3.org/2005/Atom}published").text[:4]
                pub_year = int(published_str) if published_str.isdigit() else 2021
                if pub_year < min_year or pub_year > max_year:
                    continue

                title = e.find("{http://www.w3.org/2005/Atom}title").text.strip().replace("\n", " ")
                summary = e.find("{http://www.w3.org/2005/Atom}summary").text.strip().replace("\n", " ")
                authors = [a.find("{http://www.w3.org/2005/Atom}name").text for a in e.findall("{http://www.w3.org/2005/Atom}author")]
                
                pdf_link = ""
                for link in e.findall("{http://www.w3.org/2005/Atom}link"):
                    if link.attrib.get("title") == "pdf":
                        pdf_link = link.attrib.get("href")
                
                entry_id = e.find("{http://www.w3.org/2005/Atom}id").text
                arxiv_id = entry_id.split("/")[-1]

                record = {
                    "id": arxiv_id,
                    "source": "arXiv",
                    "source_tier": 1,
                    "category": "preprint",
                    "title": title,
                    "authors": ", ".join(authors[:5]) + (" et al." if len(authors) > 5 else ""),
                    "authors_list": authors,
                    "year": pub_year,
                    "venue": "arXiv Preprint",
                    "doi": f"10.48550/arXiv.{arxiv_id}",
                    "citations": "-",
                    "is_oa": True,
                    "pdf_url": pdf_link,
                    "abstract": summary,
                    "keywords": "Computer Science / Statistics",
                    "url": entry_id,
                }
                results.append(record)
                if len(results) >= limit:
                    break

        print(f"[+] [arXiv] Ditemukan {len(results)} preprint relevan.")
    except Exception as e:
        print(f"    [i] Catatan: arXiv API dilewati ({e}). OpenAlex mencakup preprint & journal.")

    return results


def generate_markdown_report(papers: List[Dict], md_path: str, topic_label: str = ""):
    """Generates a structured literature review markdown table."""
    lines = []
    lines.append(f"# Rekapitulasi Literatur Internasional & Multi-Arsip: {topic_label or 'Hasil Penelusuran'}\n")
    lines.append(f"*Total Karya Terekam*: **{len(papers)} artikel/buku**\n")
    lines.append("| No | Tahun | Judul Karya | Penulis | Sumber / Venue | Kategori | Sitasi | Akses PDF | Tautan / DOI |")
    lines.append("|---|---|---|---|---|---|---|---|---|")
    
    for i, p in enumerate(papers, 1):
        title = (p.get("title") or "").replace("|", "-")
        authors = (p.get("authors") or "").replace("|", "-")
        venue = (p.get("venue") or "").replace("|", "-")
        src = p.get("source", "-")
        cat = p.get("category", "paper").capitalize()
        cites = str(p.get("citations", "-"))
        y = str(p.get("year", ""))
        oa_badge = f"[PDF Tersedia]({p['pdf_url']})" if p.get("pdf_url") else "Restricted"
        url_link = f"[Buka Artikel]({p['url']})" if p.get("url") else "-"
        lines.append(f"| {i} | {y} | **{title}** | {authors} | **{src}** ({venue}) | {cat} | {cites} | {oa_badge} | {url_link} |")

    lines.append("\n---\n")
    lines.append("## Ringkasan Abstrak & Kontribusi Utama\n")
    for i, p in enumerate(papers, 1):
        lines.append(f"### {i}. {p['title']} ({p['year'] or 'Tahun tidak diketahui'})")
        lines.append(f"- **Penulis**: {p['authors']}")
        lines.append(f"- **Sumber**: {p.get('source')} | **Kategori**: {p.get('category', 'paper').capitalize()}")
        lines.append(f"- **Venue**: {p['venue']} | **Sitasi**: {p.get('citations', '-')}")
        lines.append(f"- **DOI / URL**: {p.get('doi') or p.get('url')}")
        if p.get("pdf_url"):
            lines.append(f"- **Direct PDF**: [Download Link]({p['pdf_url']})")
        lines.append(f"- **Abstrak / Deskripsi**:\n  > {p.get('abstract') or 'Tidak ada abstrak yang tersedia.'}\n")

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    parser = argparse.ArgumentParser(
        description="Scraper & Multi-Archive Searcher Paper Internasional & Koleksi Terbuka"
    )
    parser.add_argument("--query", type=str, default=None, help="Kata kunci pencarian kustom")
    parser.add_argument(
        "--topic",
        type=str,
        default=None,
        choices=["1", "2", "3", "survey-fraud", "sdi-gateway", "microdata-privacy"],
        help="Pilih preset topik skripsi (1, 2, atau 3)",
    )
    parser.add_argument(
        "--source", "--sources",
        dest="sources",
        type=str,
        default="default",
        help="Sumber data: default (OA+arXiv+S2+CORE+IA), academic, libraries, books, shadow (SciHub+LibGen+Anna+ZLib), all, atau koma-terpisah (default: default)",
    )
    parser.add_argument(
        "--include-books",
        action="store_true",
        help="Sertakan buku/monograf klasik (Project Gutenberg & IA Books), dikecualikan dari batas ketat 5 tahun",
    )
    parser.add_argument("--min-year", type=int, default=2021, help="Tahun publikasi minimal (default: 2021)")
    parser.add_argument("--max-year", type=int, default=2026, help="Tahun publikasi maksimal (default: 2026)")
    parser.add_argument("--limit", type=int, default=10, help="Jumlah maksimal hasil per sumber (default: 10)")
    parser.add_argument("--output-dir", type=str, default="literature", help="Direktori output data (default: literature)")
    parser.add_argument("--download-pdf", action="store_true", help="Download otomatis seluruh paper yang memiliki PDF atau via cascading fallback")
    parser.add_argument("--no-fallback", action="store_true", help="Matikan cascading fallback ke Sci-Hub/LibGen/IPFS jika Open Access link gagal")
    parser.add_argument("--no-convert-md", action="store_true", help="Jangan otomatis mengonversi PDF terunduh ke Markdown")

    args = parser.parse_args()

    topic_map = {
        "1": "1", "survey-fraud": "1",
        "2": "2", "sdi-gateway": "2",
        "3": "3", "microdata-privacy": "3"
    }

    selected_topic_key = topic_map.get(args.topic)
    preset = TOPIC_PRESETS.get(selected_topic_key) if selected_topic_key else None
    
    query = args.query
    title_query = None
    if not query and preset:
        query = preset["openalex_general"]
        title_query = preset["openalex_title"]
    elif not query:
        print("[-] Masukkan kata kunci via --query atau pilih preset via --topic [1|2|3]")
        sys.exit(1)

    topic_label = preset["name"] if preset else f"Pencarian: '{query}'"

    # Determine which sources are active
    raw_sources = args.sources.lower()
    active_sources = [s.strip() for s in raw_sources.split(",") if s.strip()]

    all_papers: List[Dict] = []

    # 1. OpenAlex
    include_oa = "openalex" in active_sources or raw_sources in ["all", "default", "academic"]
    if include_oa:
        oa_papers = search_openalex(
            query=query,
            title_query=title_query,
            min_year=args.min_year,
            max_year=args.max_year,
            limit=args.limit
        )
        all_papers.extend(oa_papers)

    # 2. arXiv
    include_arxiv = "arxiv" in active_sources or raw_sources in ["all", "default", "academic"]
    if include_arxiv:
        ar_query = preset["arxiv_query"] if preset else f'all:"{query}"'
        ar_papers = search_arxiv(
            query=ar_query,
            min_year=args.min_year,
            max_year=args.max_year,
            limit=args.limit
        )
        all_papers.extend(ar_papers)

    # 3. Multi-Archive Manager (Semantic Scholar, CORE, Internet Archive, Gutenberg, Sci-Hub, LibGen, Anna's Archive, IPFS, Z-Library)
    archive_mgr = ArchiveManager(
        downloader_output_dir=os.path.join(args.output_dir, "pdfs"),
        enable_fallback_download=not args.no_fallback,
    )

    # Filter sources meant for ArchiveManager
    mgr_sources_list = [s for s in active_sources if s not in ["openalex", "arxiv"]]
    mgr_sources_str = ",".join(mgr_sources_list) if mgr_sources_list else raw_sources

    # Check if ArchiveManager has providers to query
    if raw_sources in ["all", "default", "academic", "libraries", "books", "shadow"] or mgr_sources_list:
        print(f"[*] [ArchiveManager] Menjalankan pencarian multi-arsip paralel: '{raw_sources}'...")
        mgr_records = archive_mgr.search(
            query=query,
            sources=mgr_sources_str,
            limit_per_source=args.limit,
            min_year=args.min_year,
            max_year=args.max_year,
            include_books=args.include_books,
        )
        for rec in mgr_records:
            all_papers.append(rec.to_dict())

    # Deduplicate all papers across all sources
    seen_titles = set()
    seen_dois = set()
    deduped_papers = []

    for p in all_papers:
        doi = p.get("doi", "").lower().strip()
        norm_title = re.sub(r"[^a-zA-Z0-9]", "", p["title"].lower())

        if doi and doi in seen_dois:
            continue
        if norm_title and norm_title in seen_titles:
            continue

        if doi:
            seen_dois.add(doi)
        if norm_title:
            seen_titles.add(norm_title)

        deduped_papers.append(p)

    print(f"\n[+] Total {len(deduped_papers)} karya unik berhasil dihimpun dari seluruh arsip.")

    os.makedirs(args.output_dir, exist_ok=True)

    # Export JSON
    suffix = f"_topic_{selected_topic_key}" if selected_topic_key else ""
    json_path = os.path.join(args.output_dir, f"international_papers{suffix}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(deduped_papers, f, ensure_ascii=False, indent=2)
    print(f"[+] Database disimpan ke JSON: {json_path}")

    # Export CSV
    csv_path = os.path.join(args.output_dir, f"international_papers{suffix}.csv")
    if deduped_papers:
        all_keys = set()
        for p in deduped_papers:
            all_keys.update(p.keys())
        primary_order = [
            "id", "year", "title", "authors", "source", "source_tier", "category",
            "venue", "doi", "citations", "is_oa", "pdf_url", "url", "abstract", "keywords"
        ]
        fieldnames = [k for k in primary_order if k in all_keys] + [k for k in sorted(all_keys) if k not in primary_order]
        with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(deduped_papers)
        print(f"[+] Spreadsheet disimpan ke CSV: {csv_path}")

    # Export Markdown Report
    md_path = os.path.join(args.output_dir, f"international_papers{suffix}.md")
    generate_markdown_report(deduped_papers, md_path, topic_label)
    print(f"[+] Ringkasan telaah disimpan ke Markdown: {md_path}")

    # Optional PDF download with cascading fallback
    if args.download_pdf:
        print("\n[*] Mengunduh berkas PDF melalui Cascading Multi-Tier Downloader...")
        downloaded_count = 0
        pdf_dir = os.path.join(args.output_dir, "pdfs")
        downloader = CascadingPaperDownloader(
            output_dir=pdf_dir,
            enable_fallback=not args.no_fallback,
        )

        for p in tqdm(deduped_papers, desc="Downloading Papers"):
            rec = PaperRecord.from_dict(p)
            res = downloader.download_paper(rec)
            if res.success:
                downloaded_count += 1
                if not args.no_convert_md and res.filepath:
                    trigger_md_conversion(res.filepath, os.path.join(args.output_dir, "markdowns"))
            time.sleep(0.3)

        print(f"[+] Sukses mengunduh {downloaded_count} PDF ke {pdf_dir}/")


if __name__ == "__main__":
    main()
