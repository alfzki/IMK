"""
calm_carson.archives.providers.internet_archive
Provider for querying the Internet Archive & Open Library (Tier 2).
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

import requests

from ..base import BaseArchiveProvider
from ..models import ArchiveTier, ItemCategory, PaperRecord

logger = logging.getLogger(__name__)

INTERNET_ARCHIVE_SEARCH_URL = "https://archive.org/advancedsearch.php"
OPEN_LIBRARY_SEARCH_URL = "https://openlibrary.org/search.json"


class InternetArchiveProvider(BaseArchiveProvider):
    """Integrates with Internet Archive & Open Library for public digital books, proceedings, and papers."""

    name: str = "internet_archive"
    display_name: str = "Internet Archive"
    tier: ArchiveTier = ArchiveTier.TIER_2_PUBLIC_LIB
    category: str = ItemCategory.BOOK
    enabled_by_default: bool = True

    def search(
        self,
        query: str,
        limit: int = 10,
        min_year: Optional[int] = None,
        max_year: Optional[int] = None,
    ) -> List[PaperRecord]:
        """Queries Internet Archive Advanced Search API."""
        records: List[PaperRecord] = []

        q_terms = [f"(title:({query}) OR {query})", "mediatype:(texts)"]
        if min_year:
            q_terms.append(f"year:>={min_year}")
        if max_year:
            q_terms.append(f"year:<={max_year}")
        full_query = " AND ".join(q_terms)

        params = {
            "q": full_query,
            "fl[]": ["identifier", "title", "creator", "year", "description", "downloads", "mediatype"],
            "sort[]": "downloads desc",
            "rows": min(limit * 2, 40),
            "page": 1,
            "output": "json",
        }

        try:
            resp = requests.get(
                INTERNET_ARCHIVE_SEARCH_URL,
                params=params,
                headers=self.headers,
                timeout=self.timeout,
            )
            if resp.status_code == 200:
                docs = resp.json().get("response", {}).get("docs", [])
                for d in docs:
                    rec = self._parse_ia_doc(d)
                    if rec:
                        if min_year and rec.year and rec.year < min_year:
                            continue
                        if max_year and rec.year and rec.year > max_year:
                            continue
                        records.append(rec)
                        if len(records) >= limit:
                            break

            # If results are sparse, supplement with Open Library book search
            if len(records) < limit:
                ol_records = self._search_open_library(query, limit - len(records), min_year, max_year)
                records.extend(ol_records)

        except Exception as e:
            logger.warning("Failed to query Internet Archive: %s", e)

        return records[:limit]

    def _parse_ia_doc(self, doc: Dict[str, Any]) -> Optional[PaperRecord]:
        """Parses an Internet Archive document object."""
        title = (doc.get("title") or "").strip()
        ident = (doc.get("identifier") or "").strip()
        if not title or not ident:
            return None

        raw_creator = doc.get("creator")
        authors = []
        if isinstance(raw_creator, list):
            authors = [str(c).strip() for c in raw_creator if c]
        elif isinstance(raw_creator, str):
            authors = [c.strip() for c in raw_creator.split(";") if c.strip()]

        year = None
        raw_year = doc.get("year")
        if raw_year and str(raw_year).isdigit():
            year = int(raw_year)

        pdf_url = f"https://archive.org/download/{ident}/{ident}.pdf"
        landing_url = f"https://archive.org/details/{ident}"
        desc = doc.get("description") or ""
        if isinstance(desc, list):
            desc = " ".join(desc)

        return PaperRecord(
            id=ident,
            title=title,
            authors=authors if authors else ["Internet Archive Contributor"],
            year=year,
            venue="Internet Archive Digital Library",
            doi=None,
            url=landing_url,
            pdf_url=pdf_url,
            abstract=str(desc).strip()[:500],
            citation_count=doc.get("downloads"),
            source=self.display_name,
            source_tier=self.tier,
            category=ItemCategory.BOOK,
            is_oa=True,
            extra={"identifier": ident},
        )

    def _search_open_library(
        self,
        query: str,
        needed: int,
        min_year: Optional[int] = None,
        max_year: Optional[int] = None,
    ) -> List[PaperRecord]:
        """Queries Open Library Book Search as enrichment."""
        results: List[PaperRecord] = []
        try:
            params = {"q": query, "limit": needed * 2}
            resp = requests.get(OPEN_LIBRARY_SEARCH_URL, params=params, headers=self.headers, timeout=self.timeout)
            if resp.status_code == 200:
                docs = resp.json().get("docs", [])
                for d in docs:
                    title = d.get("title", "").strip()
                    if not title:
                        continue
                    authors = d.get("author_name", [])
                    year = d.get("first_publish_year")
                    if min_year and year and year < min_year:
                        continue
                    if max_year and year and year > max_year:
                        continue

                    key = d.get("key", "").replace("/works/", "")
                    ia_ids = d.get("ia", [])
                    pdf_url = f"https://archive.org/download/{ia_ids[0]}/{ia_ids[0]}.pdf" if ia_ids else None

                    results.append(
                        PaperRecord(
                            id=key or title,
                            title=title,
                            authors=authors[:5] if authors else ["Open Library Author"],
                            year=int(year) if year else None,
                            venue=f"Open Library Book (Publisher: {', '.join(d.get('publisher', [])[:2])})",
                            doi=None,
                            url=f"https://openlibrary.org/works/{key}" if key else None,
                            pdf_url=pdf_url,
                            abstract=f"Edisi: {d.get('edition_count', 1)} | Bahasa: {', '.join(d.get('language', [])[:3])}",
                            citation_count=d.get("readinglog_count"),
                            source="Open Library",
                            source_tier=self.tier,
                            category=ItemCategory.BOOK,
                            is_oa=bool(pdf_url),
                            extra={"isbn": d.get("isbn", [])[:3]},
                        )
                    )
                    if len(results) >= needed:
                        break
        except Exception as e:
            logger.debug("Open Library search skipped: %s", e)
        return results
