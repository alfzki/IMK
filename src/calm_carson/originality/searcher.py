"""Global literature searcher for querying academic publications from OpenAlex, arXiv, and local corpora."""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

logger = logging.getLogger(__name__)

# Indonesian to English academic concept mappings
CONCEPT_TRANSLATIONS = [
    (r"\bprivasi\s+diferensial\b", "differential privacy"),
    (r"\bdata\s+mikro\b", "microdata tabular"),
    (r"\bperlindungan\s+data\s+pribadi\b|\buu\s+pdp\b", "privacy regulation data protection"),
    (r"\baudit\s+trail\b|\bjejak\s+audit\b", "cryptographic audit trail"),
    (r"\bfalsifikasi\s+survei\b|\bkecurangan\s+pencacah\b|\bpencacahan\b", "survey falsification curbstoning"),
    (r"\bparadatak\b|\bdwell-time\b|\bwaktu\s+pengisian\b", "paradata response time dwell-time"),
    (r"\bdeteksi\s+anomali\b", "anomaly detection machine learning"),
    (r"\bsatu\s+data\s+indonesia\b|\bsdi\b", "open government data interoperability"),
    (r"\binteroperabilitas\b", "api interoperability zero-trust"),
    (r"\bvalidasi\s+metadata\b|\bkualitas\s+metadata\b", "metadata quality assessment validation"),
    (r"\bpenilaian\s+kerentanan\b|\buji\s+penetrasi\b|\bvapt\b", "vulnerability assessment penetration testing owasp"),
    (r"\bcapi\b|\bcawi\b", "computer assisted personal interviewing CAPI"),
    (r"\bwebgis\b|\bspasial\b", "webgis spatial statistics mapping"),
    (r"\bdiseminasi\s+data\b", "statistical data dissemination knowledge graph"),
    (r"\brancang\s+bangun\b|\bpengembangan\s+sistem\b", "system design implementation"),
    (r"\bkeamanan\s+siber\b|\bkeamanan\s+api\b", "api security authentication"),
]

STOPWORDS_QUERY = {
    "yang", "di", "dan", "untuk", "dengan", "pada", "oleh", "dari", "dalam", "sebagai",
    "studi", "kasus", "berbasis", "analisis", "penerapan", "pengembangan", "rancang",
    "bangun", "evaluasi", "stis", "bps", "indonesia", "using", "the", "and", "for", "with",
}


def reconstruct_inverted_index(inverted_index: Optional[Dict[str, List[int]]]) -> str:
    """Reconstructs continuous text from OpenAlex's abstract_inverted_index format."""
    if not inverted_index:
        return ""
    pos_word = []
    for word, positions in inverted_index.items():
        for pos in positions:
            pos_word.append((pos, word))
    pos_word.sort(key=lambda x: x[0])
    text = " ".join(w for _, w in pos_word)
    return re.sub(r"\s+", " ", text).strip()


class GlobalLiteratureSearcher:
    """Searches external academic databases (OpenAlex, arXiv) and local corpus for matching literature."""

    def __init__(self, workspace_root: Optional[Path] = None):
        if workspace_root is None:
            self.workspace_root = Path(__file__).resolve().parent.parent.parent.parent
        else:
            self.workspace_root = Path(workspace_root)

        self.theses_json_path = self.workspace_root / "literature" / "theses_data.json"
        self._init_pyalex()

    def _init_pyalex(self) -> None:
        try:
            import pyalex
            pyalex.config.email = "alifzakiansyahassyauqi@gmail.com"
            self.pyalex_available = True
        except ImportError:
            self.pyalex_available = False
            logger.warning("pyalex is not installed; OpenAlex live searching disabled.")

    def formulate_search_queries(self, idea_text: str) -> List[str]:
        """Converts an Indonesian or English idea/problem statement into targeted academic search queries."""
        text_lower = idea_text.lower()
        translated_text = text_lower

        # Apply concept mapping
        for id_pattern, en_trans in CONCEPT_TRANSLATIONS:
            translated_text = re.sub(id_pattern, en_trans, translated_text)

        # Extract salient technical keywords
        words = re.findall(r"\b[a-zA-Z]{3,}\b", translated_text)
        salient_words = [w for w in words if w not in STOPWORDS_QUERY]

        queries: List[str] = []

        # 1. Primary technical query (first 4-6 salient keywords)
        if salient_words:
            primary_query = " ".join(salient_words[:6])
            queries.append(primary_query)

        # 2. Key phrases
        if "differential privacy" in translated_text:
            queries.append("differential privacy tabular microdata release")
        if "falsification" in translated_text or "curbstoning" in translated_text:
            queries.append("survey falsification interviewer curbstoning paradata")
        if "interoperability" in translated_text or "gateway" in translated_text:
            queries.append("api gateway metadata interoperability zero trust")
        if "webgis" in translated_text or "spatial" in translated_text:
            queries.append("spatial statistics webgis land use remote sensing")

        # Fallback if no specific phrase matched
        if len(queries) <= 1 and len(salient_words) > 3:
            queries.append(" ".join(salient_words[2:7]))

        return list(dict.fromkeys(queries))  # deduplicate preserving order

    def search_openalex(
        self,
        queries: List[str],
        min_year: int = 2021,
        max_year: int = 2026,
        limit_per_query: int = 6,
    ) -> List[Dict[str, Any]]:
        """Queries OpenAlex for relevant peer-reviewed works."""
        if not self.pyalex_available:
            return []

        from pyalex import Works

        works_collected: List[Dict[str, Any]] = []
        seen_dois_or_titles: Set[str] = set()

        from_date = f"{min_year}-01-01"
        to_date = f"{max_year}-12-31"

        for q in queries:
            try:
                # Search OpenAlex
                works = (
                    Works()
                    .search(q)
                    .filter(from_publication_date=from_date, to_publication_date=to_date)
                    .sort(cited_by_count="desc")
                    .get(per_page=limit_per_query)
                )

                for w in works:
                    title = w.get("title") or ""
                    if not title:
                        continue
                    doi = w.get("doi") or ""
                    dedup_key = (doi or title).lower().strip()
                    if dedup_key in seen_dois_or_titles:
                        continue
                    seen_dois_or_titles.add(dedup_key)

                    # Reconstruct abstract
                    abstract_inv = w.get("abstract_inverted_index")
                    abstract = reconstruct_inverted_index(abstract_inv) if abstract_inv else ""

                    # Authors
                    authors = []
                    for authorship in w.get("authorships", []):
                        aname = authorship.get("author", {}).get("display_name")
                        if aname:
                            authors.append(aname)

                    # Venue / Source
                    location = w.get("primary_location") or {}
                    source = location.get("source") or {}
                    venue = source.get("display_name") or w.get("type", "Publication")

                    works_collected.append({
                        "id": w.get("id") or doi or f"openalex_{len(works_collected)}",
                        "title": title.strip(),
                        "authors": authors[:5] if authors else ["Anonymous"],
                        "year": int(w.get("publication_year") or min_year),
                        "venue": venue,
                        "doi": doi or None,
                        "url": location.get("landing_page_url") or doi or None,
                        "abstract": abstract,
                        "citation_count": int(w.get("cited_by_count") or 0),
                        "source_database": "openalex",
                    })
            except Exception as e:
                logger.warning("OpenAlex search error for '%s': %s", q, e)

        return works_collected

    def search_local_theses(self, idea_text: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Cross-check with local STIS theses database for internal baseline comparison."""
        if not self.theses_json_path.exists():
            return []

        try:
            with open(self.theses_json_path, "r", encoding="utf-8") as f:
                theses_list = json.load(f)
        except Exception as e:
            logger.warning("Could not read theses_data.json: %s", e)
            return []

        # Simple keyword overlap scoring
        words = set(re.findall(r"\b[a-zA-Z]{4,}\b", idea_text.lower())) - STOPWORDS_QUERY
        matches = []

        for item in theses_list:
            title = item.get("judul", "")
            abstract = item.get("abstrak", "")
            comb = f"{title} {abstract}".lower()
            score = sum(1 for w in words if w in comb)
            if score >= 2:
                matches.append((score, item))

        matches.sort(key=lambda x: x[0], reverse=True)

        results = []
        for _, item in matches[:limit]:
            results.append({
                "id": item.get("id", ""),
                "title": item.get("judul", "").strip(),
                "authors": [item.get("penulis", "").strip().title()],
                "year": int(item.get("tahun") or 2024),
                "venue": f"Skripsi Polstat STIS ({item.get('peminatan', 'SIS')})",
                "doi": None,
                "url": item.get("url_simpus") or None,
                "abstract": item.get("abstrak", "").strip(),
                "citation_count": int(item.get("jumlah_dibaca") or 0),
                "source_database": "stis_theses",
            })

        return results

    def search_academic_archives(
        self,
        queries: List[str],
        min_year: int = 2021,
        max_year: int = 2026,
        limit_per_query: int = 3,
    ) -> List[Dict[str, Any]]:
        """Queries Semantic Scholar and CORE via ArchiveManager for comprehensive novelty evaluation."""
        try:
            from calm_carson.archives.manager import ArchiveManager
            mgr = ArchiveManager()
        except Exception as e:
            logger.debug("Could not import ArchiveManager: %s", e)
            return []

        results: List[Dict[str, Any]] = []
        seen: Set[str] = set()

        for q in queries:
            try:
                records = mgr.search(
                    query=q,
                    sources="semanticscholar,core",
                    limit_per_source=limit_per_query,
                    min_year=min_year,
                    max_year=max_year,
                )
                for r in records:
                    key = (r.doi or r.get_normalized_title()).lower().strip()
                    if key in seen:
                        continue
                    seen.add(key)
                    results.append({
                        "id": r.id,
                        "title": r.title,
                        "authors": r.authors,
                        "year": r.year or min_year,
                        "venue": r.venue,
                        "doi": r.doi,
                        "url": r.url or r.pdf_url,
                        "abstract": r.abstract,
                        "citation_count": r.citation_count or 0,
                        "source_database": r.source.lower().replace(" ", "_"),
                    })
            except Exception as e:
                logger.debug("Academic archives search error for '%s': %s", q, e)

        return results
