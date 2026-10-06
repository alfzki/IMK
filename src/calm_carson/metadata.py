"""
calm_carson.metadata
Automated Paper Metadata Extractor & BibTeX Citation Generator
Integrates local PDF and Markdown documents with Crossref, Semantic Scholar,
OpenAlex, and Politeknik Statistika STIS theses database.
"""

import csv
import glob
import json
import logging
import os
import re
import urllib.parse
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pypdf
import requests
from tqdm import tqdm

# Suppress noisy PDF parser warnings
logging.getLogger("pypdf").setLevel(logging.ERROR)

POLITE_EMAIL = "alifzakiansyahassyauqi@gmail.com"
USER_AGENT = f"calm-carson-researcher/1.0 (mailto:{POLITE_EMAIL})"
CROSSREF_API_URL = "https://api.crossref.org/works"
SEMANTIC_SCHOLAR_API_URL = "https://api.semanticscholar.org/graph/v1/paper"
OPENALEX_API_URL = "https://api.openalex.org/works"


# ==============================================================================
# Normalization & Helpers
# ==============================================================================

def clean_doi(raw_doi: str) -> str:
    """Cleans and standardizes a DOI string."""
    if not raw_doi:
        return ""
    doi = raw_doi.strip()
    doi = re.sub(r"^https?://(dx\.)?doi\.org/", "", doi, flags=re.IGNORECASE)
    doi = re.sub(r"^doi:\s*", "", doi, flags=re.IGNORECASE)
    doi = re.sub(r"[.,;:)\]>'\"]+$", "", doi)
    return doi.strip()


def extract_doi_from_text(text: str) -> Optional[str]:
    """Extracts the first valid DOI from freeform text."""
    if not text:
        return None
    match = re.search(r"\b(10\.\d{4,9}/[-._;()/:A-Za-z0-9]+)", text)
    if match:
        doi = clean_doi(match.group(1))
        if "/" in doi and len(doi.split("/", 1)[1]) > 1:
            return doi
    return None


def extract_arxiv_id_from_text(text: str) -> Optional[str]:
    """Extracts an arXiv ID from freeform text."""
    if not text:
        return None
    match = re.search(r"(?:arxiv[:\s/]*)([0-9]{4}\.[0-9]{4,5}(?:v[0-9]+)?)", text, re.IGNORECASE)
    if match:
        return match.group(1)
    return None


def clean_jats_xml(text: str) -> str:
    """Strips JATS XML tags (such as <jats:p>) from Crossref abstracts."""
    if not text:
        return ""
    clean = re.sub(r"<[^>]+>", " ", text)
    clean = re.sub(r"\s+", " ", clean).strip()
    return clean


def normalize_title_for_comparison(title: str) -> str:
    """Normalizes a title string for fuzzy comparison."""
    if not title:
        return ""
    title = re.sub(r"[*_#`\"'’‘“”()]", " ", title)
    title = re.sub(r"[^a-zA-Z0-9\s]", " ", title.lower())
    return " ".join(title.split())


def compute_title_similarity(title1: str, title2: str) -> float:
    """
    Computes a composite similarity score between two titles combining
    Jaccard word similarity, subset token containment, and substring matching.
    """
    norm1 = normalize_title_for_comparison(title1)
    norm2 = normalize_title_for_comparison(title2)
    if not norm1 or not norm2:
        return 0.0

    if norm1 == norm2:
        return 1.0
    if norm1 in norm2 or norm2 in norm1:
        return 0.95

    w1 = set(norm1.split())
    w2 = set(norm2.split())
    if not w1 or not w2:
        return 0.0

    intersection = len(w1.intersection(w2))
    union = len(w1.union(w2))
    jaccard = intersection / union if union > 0 else 0.0

    min_len = min(len(w1), len(w2))
    overlap = intersection / min_len if min_len > 0 else 0.0

    if overlap >= 0.70 and min_len >= 4:
        return max(jaccard, overlap * 0.9)

    return jaccard


def clean_filename_to_title(filename: str) -> str:
    """Extracts a plausible title candidate from a filename."""
    stem = Path(filename).stem
    stem = re.sub(r"^(INTL_)?\d{4}_", "", stem)
    title = stem.replace("_", " ").replace("-", " ")
    return re.sub(r"\s+", " ", title).strip()


def generate_citekey(author_str: str, year: Any, title_str: str) -> str:
    """Generates a standardized BibTeX citekey, e.g., 'Garfinkel2018Issues'."""
    first_author = "Unknown"
    if author_str:
        parts = re.split(r"[,;]|(?:\sand\s)", author_str)
        if parts:
            first = parts[0].strip()
            subparts = first.split()
            if subparts:
                first_author = subparts[0].replace(",", "")
    
    first_author_clean = re.sub(r"[^a-zA-Z]", "", first_author).capitalize()
    year_str = str(year) if year else "nodate"
    
    first_word = "paper"
    if title_str:
        words = [w for w in re.sub(r"[^a-zA-Z0-9\s]", "", title_str).split() if len(w) > 2]
        stop_words = {"the", "and", "for", "with", "from", "analisis", "pengembangan", "pada"}
        for w in words:
            if w.lower() not in stop_words:
                first_word = w.capitalize()
                break
        if not first_word and words:
            first_word = words[0].capitalize()
            
    return f"{first_author_clean}{year_str}{first_word}"


# ==============================================================================
# Document Parsers
# ==============================================================================

class DocumentInfo:
    def __init__(self, filepath: str):
        self.filepath: str = filepath
        self.doi: Optional[str] = None
        self.arxiv_id: Optional[str] = None
        self.title: Optional[str] = None
        self.authors: Optional[str] = None
        self.abstract: Optional[str] = None
        self.year: Optional[int] = None
        self.doc_type: str = "unknown"
        self.raw_text_snippet: str = ""


def parse_pdf_document(pdf_path: str) -> DocumentInfo:
    """Extracts identifiers, metadata, and multi-line title from a PDF document."""
    info = DocumentInfo(pdf_path)
    info.doc_type = "pdf"
    
    try:
        reader = pypdf.PdfReader(pdf_path)
        meta = reader.metadata or {}
        
        meta_doi = meta.get("/DOI") or meta.get("DOI")
        if meta_doi:
            info.doi = clean_doi(str(meta_doi))
            
        meta_arxiv = meta.get("/arXivID") or meta.get("arXivID")
        if meta_arxiv:
            info.arxiv_id = extract_arxiv_id_from_text(str(meta_arxiv))
            
        meta_title = meta.get("/Title") or meta.get("Title")
        if meta_title:
            t = str(meta_title).strip()
            if t and not re.search(r"^(untitled|microsoft word|latex|default)$", t, re.IGNORECASE):
                info.title = t
                
        meta_author = meta.get("/Author") or meta.get("Author")
        if meta_author:
            info.authors = str(meta_author).strip()

        num_pages_to_scan = min(3, len(reader.pages))
        extracted_pages = []
        for i in range(num_pages_to_scan):
            try:
                page_text = reader.pages[i].extract_text() or ""
                extracted_pages.append(page_text)
            except Exception:
                continue
                
        full_intro_text = "\n".join(extracted_pages)
        info.raw_text_snippet = full_intro_text[:1200]
        
        if not info.doi:
            info.doi = extract_doi_from_text(full_intro_text)
            
        if not info.arxiv_id:
            info.arxiv_id = extract_arxiv_id_from_text(full_intro_text)
            
        if info.arxiv_id and not info.doi:
            info.doi = f"10.48550/arXiv.{info.arxiv_id}"

        if not info.title and extracted_pages:
            lines = [l.strip() for l in extracted_pages[0].split("\n") if l.strip()]
            title_lines = []
            for line in lines:
                if re.search(r"(program studi|politeknik|universitas|diajukan|disusun|oleh\s*:|^\d{7,10}$|abstract|keywords|surat persetujuan)", line, re.IGNORECASE):
                    break
                if re.search(r"\b\d{9}\b", line):
                    break
                title_lines.append(line)
                if len(title_lines) >= 6:
                    break
            
            candidate_title = " ".join(title_lines).strip()
            if len(candidate_title) > 10:
                info.title = re.sub(r"\s+", " ", candidate_title)
                
    except Exception as e:
        print(f"    [!] Peringatan: Gagal membaca file PDF '{pdf_path}': {e}")

    if not info.title:
        info.title = clean_filename_to_title(pdf_path)

    return info


def parse_markdown_document(md_path: str) -> DocumentInfo:
    """Extracts identifiers, title, and abstract from a Markdown file or folder."""
    info = DocumentInfo(md_path)
    info.doc_type = "markdown"

    actual_md_file = md_path
    meta_json_file = None

    if os.path.isdir(md_path):
        md_files = glob.glob(os.path.join(md_path, "*.md"))
        if md_files:
            actual_md_file = md_files[0]
        json_files = glob.glob(os.path.join(md_path, "*_meta.json"))
        if json_files:
            meta_json_file = json_files[0]
    else:
        stem = Path(md_path).stem
        parent = os.path.dirname(md_path)
        possible_meta = os.path.join(parent, f"{stem}_meta.json")
        if os.path.exists(possible_meta):
            meta_json_file = possible_meta

    if meta_json_file and os.path.exists(meta_json_file):
        try:
            with open(meta_json_file, "r", encoding="utf-8") as f:
                meta_data = json.load(f)
                toc = meta_data.get("table_of_contents", [])
                if toc and isinstance(toc, list) and len(toc) > 0:
                    first_toc_title = toc[0].get("title", "")
                    if first_toc_title:
                        info.title = first_toc_title.replace("\n", " ").strip()
        except Exception:
            pass

    if os.path.isfile(actual_md_file):
        try:
            with open(actual_md_file, "r", encoding="utf-8") as f:
                content = f.read()

            info.raw_text_snippet = content[:1500]
            info.doi = extract_doi_from_text(content[:3000])
            info.arxiv_id = extract_arxiv_id_from_text(content[:3000])
            if info.arxiv_id and not info.doi:
                info.doi = f"10.48550/arXiv.{info.arxiv_id}"

            if not info.title:
                h1_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
                if h1_match:
                    raw_h1 = h1_match.group(1).strip()
                    info.title = re.sub(r"[*_`]", "", raw_h1).strip()

            abs_match = re.search(
                r"(?:####?\s*Abstract|##\s*Abstrak|####?\s*Abstrak)\s*\n+([\s\S]*?)(?:\n##|\n####|\n\n\n)",
                content,
                re.IGNORECASE,
            )
            if abs_match:
                info.abstract = abs_match.group(1).strip()

        except Exception as e:
            print(f"    [!] Peringatan: Gagal membaca file Markdown '{actual_md_file}': {e}")

    if not info.title:
        info.title = clean_filename_to_title(actual_md_file)

    return info


# ==============================================================================
# Academic API Clients & Local Theses Resolver
# ==============================================================================

class AcademicResolver:
    """Coordinates queries between Crossref, Semantic Scholar, OpenAlex, and optionally STIS DB."""

    def __init__(self, theses_db_path: str = "literature/theses_data.json", allow_simpus_theses: bool = False):
        self.headers = {"User-Agent": USER_AGENT}
        self.allow_simpus_theses = allow_simpus_theses
        self.theses_db: List[Dict] = []
        if allow_simpus_theses and os.path.exists(theses_db_path):
            try:
                with open(theses_db_path, "r", encoding="utf-8") as f:
                    self.theses_db = json.load(f)
            except Exception as e:
                print(f"[!] Gagal memuat database skripsi STIS: {e}")

    def query_crossref_by_doi(self, doi: str) -> Optional[Dict[str, Any]]:
        """Fetches metadata from Crossref REST API using DOI."""
        clean = clean_doi(doi)
        url = f"{CROSSREF_API_URL}/{urllib.parse.quote(clean)}"
        try:
            resp = requests.get(url, headers=self.headers, timeout=12)
            if resp.status_code == 200:
                item = resp.json().get("message", {})
                return self._parse_crossref_item(item)
        except Exception:
            pass
        return None

    def query_crossref_by_title(self, title: str) -> Optional[Dict[str, Any]]:
        """Searches Crossref by title and returns the best matching paper."""
        params = {"query.title": title, "rows": 3}
        try:
            resp = requests.get(CROSSREF_API_URL, params=params, headers=self.headers, timeout=12)
            if resp.status_code == 200:
                items = resp.json().get("message", {}).get("items", [])
                for item in items:
                    item_titles = item.get("title", [])
                    item_title = item_titles[0] if item_titles else ""
                    if compute_title_similarity(title, item_title) >= 0.5:
                        return self._parse_crossref_item(item)
        except Exception:
            pass
        return None

    def _parse_crossref_item(self, item: Dict) -> Dict[str, Any]:
        """Converts raw Crossref item into a normalized record."""
        titles = item.get("title", [])
        title = titles[0] if titles else ""

        authors = []
        for a in item.get("author", []):
            family = a.get("family", "")
            given = a.get("given", "")
            if family and given:
                authors.append(f"{given} {family}")
            elif family:
                authors.append(family)
            elif given:
                authors.append(given)
        authors_str = ", ".join(authors) if authors else "Unknown"

        year = None
        published = item.get("published", {}) or item.get("published-print", {}) or item.get("published-online", {})
        date_parts = published.get("date-parts", [[]])
        if date_parts and date_parts[0]:
            year = date_parts[0][0]

        containers = item.get("container-title", [])
        venue = containers[0] if containers else item.get("publisher", "")

        volume = item.get("volume", "")
        issue = item.get("issue", "")
        page = item.get("page", "")

        abstract = clean_jats_xml(item.get("abstract", ""))
        doi = item.get("DOI", "")
        url = item.get("URL", f"https://doi.org/{doi}" if doi else "")

        return {
            "title": title,
            "authors": authors_str,
            "year": year,
            "venue": venue,
            "volume": volume,
            "issue": issue,
            "page": page,
            "doi": doi,
            "url": url,
            "abstract": abstract,
            "citation_count": item.get("is-referenced-by-count", 0),
            "publisher": item.get("publisher", ""),
            "api_source": "Crossref",
        }

    def fetch_official_bibtex(self, doi: str) -> Optional[str]:
        """Retrieves official, publisher-verified BibTeX via DOI Content Negotiation."""
        clean = clean_doi(doi)
        if not clean:
            return None
        url = f"https://doi.org/{clean}"
        headers = {
            "Accept": "application/x-bibtex; charset=utf-8",
            "User-Agent": USER_AGENT,
        }
        try:
            resp = requests.get(url, headers=headers, timeout=12, allow_redirects=True)
            if resp.status_code == 200 and resp.text.strip().startswith("@"):
                return resp.text.strip()
        except Exception:
            pass
        return None

    def query_semantic_scholar(self, identifier: str, is_doi: bool = True) -> Optional[Dict[str, Any]]:
        """Queries Semantic Scholar Academic Graph API for rich metadata."""
        fields = "title,authors,year,venue,publicationVenue,abstract,citationCount,externalIds,openAccessPdf"
        try:
            if is_doi:
                url = f"{SEMANTIC_SCHOLAR_API_URL}/{clean_doi(identifier)}"
                resp = requests.get(url, params={"fields": fields}, headers=self.headers, timeout=12)
                if resp.status_code == 200:
                    return self._parse_s2_item(resp.json())
            else:
                search_url = f"{SEMANTIC_SCHOLAR_API_URL}/search"
                params = {"query": identifier, "limit": 3, "fields": fields}
                resp = requests.get(search_url, params=params, headers=self.headers, timeout=12)
                if resp.status_code == 200:
                    data = resp.json().get("data", [])
                    for p in data:
                        if compute_title_similarity(identifier, p.get("title", "")) >= 0.5:
                            return self._parse_s2_item(p)
        except Exception:
            pass
        return None

    def _parse_s2_item(self, item: Dict) -> Dict[str, Any]:
        """Parses Semantic Scholar payload."""
        title = item.get("title", "")
        authors = [a.get("name") for a in item.get("authors", []) if a.get("name")]
        authors_str = ", ".join(authors) if authors else "Unknown"

        venue_data = item.get("publicationVenue") or {}
        venue = venue_data.get("name") or item.get("venue") or ""

        ext_ids = item.get("externalIds", {}) or {}
        doi = ext_ids.get("DOI") or (f"10.48550/arXiv.{ext_ids['ArXiv']}" if "ArXiv" in ext_ids else "")

        oa_pdf = item.get("openAccessPdf") or {}
        pdf_url = oa_pdf.get("url", "")

        return {
            "title": title,
            "authors": authors_str,
            "year": item.get("year"),
            "venue": venue,
            "doi": doi,
            "url": f"https://doi.org/{doi}" if doi else f"https://www.semanticscholar.org/paper/{item.get('paperId')}",
            "abstract": item.get("abstract", "") or "",
            "citation_count": item.get("citationCount", 0),
            "pdf_url": pdf_url,
            "api_source": "Semantic Scholar",
        }

    def query_openalex(self, title: str, doi: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Queries OpenAlex as a robust academic fallback."""
        try:
            if doi:
                url = f"{OPENALEX_API_URL}/https://doi.org/{clean_doi(doi)}"
                resp = requests.get(url, headers=self.headers, timeout=12)
                if resp.status_code == 200:
                    return self._parse_openalex_item(resp.json())

            if title:
                params = {"filter": f"title.search:{title}"}
                resp = requests.get(OPENALEX_API_URL, params=params, headers=self.headers, timeout=12)
                if resp.status_code == 200:
                    results = resp.json().get("results", [])
                    for r in results:
                        if compute_title_similarity(title, r.get("title", "")) >= 0.5:
                            return self._parse_openalex_item(r)
        except Exception:
            pass
        return None

    def _parse_openalex_item(self, item: Dict) -> Dict[str, Any]:
        """Parses OpenAlex work object."""
        title = item.get("title", "")

        authors = []
        for authorship in item.get("authorships", []):
            author_obj = authorship.get("author", {})
            if "display_name" in author_obj:
                authors.append(author_obj["display_name"])
        authors_str = ", ".join(authors[:5]) + (" et al." if len(authors) > 5 else "")

        venue_obj = item.get("primary_location", {}).get("source", {}) or {}
        venue = venue_obj.get("display_name", "")

        doi_raw = item.get("doi", "")
        doi = clean_doi(doi_raw)

        abstract = ""
        inv_index = item.get("abstract_inverted_index")
        if inv_index:
            pos_list = []
            for word, positions in inv_index.items():
                for pos in positions:
                    pos_list.append((pos, word))
            pos_list.sort(key=lambda x: x[0])
            abstract = " ".join(w for _, w in pos_list)

        oa_info = item.get("open_access", {}) or {}

        return {
            "title": title,
            "authors": authors_str or "Unknown",
            "year": item.get("publication_year"),
            "venue": venue,
            "doi": doi,
            "url": doi_raw or item.get("id", ""),
            "abstract": abstract,
            "citation_count": item.get("cited_by_count", 0),
            "pdf_url": oa_info.get("oa_url", ""),
            "api_source": "OpenAlex",
        }

    def match_local_stis_theses(self, title: str, filename_candidate: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Matches a document title or filename candidate against local STIS alumni theses (if permitted)."""
        if not self.allow_simpus_theses or not self.theses_db or not title:
            return None

        best_score = 0.0
        best_thesis = None

        candidates = [title]
        if filename_candidate and filename_candidate != title:
            candidates.append(filename_candidate)

        for cand in candidates:
            for t in self.theses_db:
                stis_title = t.get("judul", "")
                score = compute_title_similarity(cand, stis_title)
                if score > best_score:
                    best_score = score
                    best_thesis = t

        if best_score >= 0.50 and best_thesis:
            penulis = best_thesis.get("penulis", "Mahasiswa STIS")
            tahun = best_thesis.get("tahun")
            pembimbing = best_thesis.get("pembimbing", "")
            peminatan = best_thesis.get("peminatan", "Sistem Informasi Statistik")
            abstrak = best_thesis.get("abstrak", "")

            return {
                "title": best_thesis.get("judul"),
                "authors": penulis,
                "year": tahun,
                "venue": f"Skripsi Sarjana Terapan Komputasi Statistik, Peminatan {peminatan}",
                "institution": "Politeknik Statistika STIS",
                "supervisor": pembimbing,
                "doi": "",
                "url": f"https://simpus.stis.ac.id/repositori/{best_thesis.get('id', '')}",
                "abstract": abstrak,
                "entry_type": "mastersthesis",
                "api_source": "SIMPus Polstat STIS Database",
            }
        return None

    def resolve(
        self,
        doi: Optional[str] = None,
        title: Optional[str] = None,
        filename_hint: Optional[str] = None,
        preferred_api: str = "all",
        allow_simpus_theses: Optional[bool] = None,
    ) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Orchestrates metadata resolution using available APIs and databases.
        By default, SIMPUS skripsi theses are disabled for reference resolution (peer-reviewed papers only).
        Returns: (metadata_dict, official_or_synthesized_bibtex)
        """
        metadata = None
        bibtex = None
        can_use_theses = self.allow_simpus_theses if allow_simpus_theses is None else allow_simpus_theses

        doi = clean_doi(doi) if doi else None

        # 1. Try DOI resolution via Crossref
        if doi and preferred_api in ["all", "crossref"]:
            metadata = self.query_crossref_by_doi(doi)
            if metadata:
                bibtex = self.fetch_official_bibtex(doi)

        # 2. Try Semantic Scholar by DOI
        if doi and (not metadata or not metadata.get("abstract")) and preferred_api in ["all", "semanticscholar"]:
            s2_data = self.query_semantic_scholar(doi, is_doi=True)
            if s2_data:
                if not metadata:
                    metadata = s2_data
                else:
                    if not metadata.get("abstract"):
                        metadata["abstract"] = s2_data.get("abstract", "")
                    metadata["citation_count"] = max(
                        metadata.get("citation_count", 0), s2_data.get("citation_count", 0)
                    )

        # 3. Title-based resolution: Prioritize peer-reviewed academic literature
        if not metadata and title:
            if preferred_api in ["all", "crossref"]:
                metadata = self.query_crossref_by_title(title)
                if metadata and metadata.get("doi"):
                    bibtex = self.fetch_official_bibtex(metadata["doi"])

            if (not metadata or not metadata.get("abstract")) and preferred_api in ["all", "semanticscholar"]:
                s2_title = self.query_semantic_scholar(title, is_doi=False)
                if s2_title:
                    if not metadata:
                        metadata = s2_title
                    else:
                        if not metadata.get("abstract"):
                            metadata["abstract"] = s2_title.get("abstract", "")

            if not metadata and preferred_api in ["all", "openalex"]:
                metadata = self.query_openalex(title=title)
                if metadata and metadata.get("doi") and not bibtex:
                    bibtex = self.fetch_official_bibtex(metadata["doi"])

            # Only check local STIS theses if explicitly permitted
            if not metadata and can_use_theses:
                stis_match = self.match_local_stis_theses(title, filename_candidate=filename_hint)
                if stis_match:
                    metadata = stis_match

        # 4. Generate Synthesized BibTeX if official not available
        if metadata and not bibtex:
            bibtex = self.synthesize_bibtex(metadata)

        return metadata, bibtex

    def synthesize_bibtex(self, record: Dict[str, Any]) -> str:
        """Constructs a clean canonical BibTeX entry."""
        author = record.get("authors", "Unknown")
        year = record.get("year") or "2024"
        title = record.get("title", "Untitled")
        citekey = generate_citekey(author, year, title)

        entry_type = record.get("entry_type") or "article"
        if "skripsi" in str(record.get("venue", "")).lower() or record.get("institution"):
            entry_type = "mastersthesis"

        lines = [f"@{entry_type}{{{citekey},"]
        lines.append(f"  title = {{{title}}},")
        lines.append(f"  author = {{{author}}},")
        lines.append(f"  year = {{{year}}},")

        if entry_type == "mastersthesis":
            lines.append(f"  school = {{{record.get('institution', 'Politeknik Statistika STIS')}}},")
            if record.get("supervisor"):
                lines.append(f"  note = {{Dosen Pembimbing: {record['supervisor']}}},")
            if record.get("venue"):
                lines.append(f"  type = {{{record['venue']}}},")
        else:
            if record.get("venue"):
                lines.append(f"  journal = {{{record['venue']}}},")
            if record.get("volume"):
                lines.append(f"  volume = {{{record['volume']}}},")
            if record.get("issue"):
                lines.append(f"  number = {{{record['issue']}}},")
            if record.get("page"):
                lines.append(f"  pages = {{{record['page']}}},")
            if record.get("publisher"):
                lines.append(f"  publisher = {{{record['publisher']}}},")

        if record.get("doi"):
            lines.append(f"  doi = {{{record['doi']}}},")
        if record.get("url"):
            lines.append(f"  url = {{{record['url']}}},")

        lines.append("}")
        return "\n".join(lines)


# ==============================================================================
# Pipeline & Batch Processing
# ==============================================================================

def extract_paper_metadata(
    target_path_or_query: str,
    resolver: Optional[AcademicResolver] = None,
    preferred_api: str = "all",
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """High-level API: Takes a file path (PDF/Markdown) or DOI/Title string."""
    if resolver is None:
        resolver = AcademicResolver()

    clean_in = clean_doi(target_path_or_query)
    if clean_in.startswith("10.") and "/" in clean_in:
        return resolver.resolve(doi=clean_in, preferred_api=preferred_api)

    if os.path.exists(target_path_or_query):
        path = target_path_or_query
        filename_hint = clean_filename_to_title(path)

        if os.path.isdir(path) or path.endswith(".md"):
            doc_info = parse_markdown_document(path)
        elif path.endswith(".pdf"):
            doc_info = parse_pdf_document(path)
        else:
            doc_info = DocumentInfo(path)
            doc_info.title = filename_hint

        meta, bib = resolver.resolve(
            doi=doc_info.doi,
            title=doc_info.title,
            filename_hint=filename_hint,
            preferred_api=preferred_api,
        )

        if meta:
            meta["source_file"] = os.path.abspath(target_path_or_query)
            if not meta.get("abstract") and doc_info.abstract:
                meta["abstract"] = doc_info.abstract

        return meta, bib

    return resolver.resolve(title=target_path_or_query, preferred_api=preferred_api)


def batch_process_documents(
    input_paths: List[str],
    output_dir: str = "literature",
    bibtex_filename: str = "references.bib",
    preferred_api: str = "all",
    force: bool = False,
) -> List[Dict[str, Any]]:
    """Processes a batch of files/directories, generating JSON, CSV, and BibTeX."""
    resolver = AcademicResolver()
    os.makedirs(output_dir, exist_ok=True)

    json_path = os.path.join(output_dir, "extracted_metadata.json")
    csv_path = os.path.join(output_dir, "extracted_metadata.csv")
    bib_path = os.path.join(output_dir, bibtex_filename)

    existing_records = []
    seen_identifiers = set()
    if os.path.exists(json_path) and not force:
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                existing_records = json.load(f)
                for r in existing_records:
                    key = r.get("doi") or r.get("title", "").lower()
                    if key:
                        seen_identifiers.add(key)
        except Exception:
            pass

    collected_records = list(existing_records)
    collected_bibtex = []

    existing_bibtex_text = ""
    if os.path.exists(bib_path) and not force:
        with open(bib_path, "r", encoding="utf-8") as f:
            existing_bibtex_text = f.read()

    print(f"\n[*] Memulai ekstraksi metadata untuk {len(input_paths)} target...")

    for path in tqdm(input_paths, desc="Processing Documents"):
        try:
            meta, bib = extract_paper_metadata(path, resolver=resolver, preferred_api=preferred_api)
            if meta:
                meta["source_file"] = path
                ident = meta.get("doi") or meta.get("title", "").lower()
                if ident not in seen_identifiers or force:
                    seen_identifiers.add(ident)
                    collected_records.append(meta)

                if bib and bib not in existing_bibtex_text and bib not in collected_bibtex:
                    collected_bibtex.append(bib)
            else:
                print(f"    [-] Metadata tidak ditemukan untuk: {Path(path).name}")
        except Exception as e:
            print(f"    [!] Gagal memproses {path}: {e}")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(collected_records, f, ensure_ascii=False, indent=2)
    print(f"[+] Metadata terstruktur disimpan ke JSON: {json_path}")

    if collected_records:
        csv_fields = [
            "title", "authors", "year", "venue", "doi", "url", 
            "citation_count", "api_source", "source_file", "abstract"
        ]
        with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=csv_fields, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(collected_records)
        print(f"[+] Ringkasan spreadsheet disimpan ke CSV: {csv_path}")

    if collected_bibtex:
        with open(bib_path, "a" if not force and os.path.exists(bib_path) else "w", encoding="utf-8") as f:
            if not os.path.exists(bib_path) or force:
                f.write("% Auto-generated BibTeX database by calm-carson metadata extractor\n\n")
            f.write("\n\n".join(collected_bibtex) + "\n\n")
        print(f"[+] Sitasi standar BibTeX disimpan ke: {bib_path}")

    return collected_records
