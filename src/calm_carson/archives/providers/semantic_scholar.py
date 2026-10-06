"""
calm_carson.archives.providers.semantic_scholar
Provider for querying the Semantic Scholar Academic Graph REST API (Tier 1).
"""

from __future__ import annotations

import logging
import re
from typing import Any, Dict, List, Optional

import requests

from ..base import BaseArchiveProvider
from ..models import ArchiveTier, ItemCategory, PaperRecord

logger = logging.getLogger(__name__)

SEMANTIC_SCHOLAR_SEARCH_URL = "https://api.semanticscholar.org/graph/v1/paper/search"
SEMANTIC_SCHOLAR_PAPER_URL = "https://api.semanticscholar.org/graph/v1/paper"


class SemanticScholarProvider(BaseArchiveProvider):
    """Integrates with Semantic Scholar Graph API for academic journals and conferences."""

    name: str = "semanticscholar"
    display_name: str = "Semantic Scholar"
    tier: ArchiveTier = ArchiveTier.TIER_1_ACADEMIC
    category: str = ItemCategory.PAPER
    enabled_by_default: bool = True

    def search(
        self,
        query: str,
        limit: int = 10,
        min_year: Optional[int] = None,
        max_year: Optional[int] = None,
    ) -> List[PaperRecord]:
        """Queries Semantic Scholar Academic Graph."""
        records: List[PaperRecord] = []
        fields = "paperId,title,authors,year,venue,publicationVenue,abstract,citationCount,openAccessPdf,externalIds,url"

        # Check if query looks like a DOI
        doi_match = re.search(r"\b(10\.\d{4,9}/[-._;()/:A-Za-z0-9]+)\b", query)
        if doi_match:
            doi = doi_match.group(1)
            rec = self._lookup_single_paper(f"DOI:{doi}", fields)
            if rec:
                return [rec]

        params: Dict[str, Any] = {
            "query": query,
            "limit": min(limit * 2, 50),
            "fields": fields,
        }
        if min_year and max_year:
            params["year"] = f"{min_year}-{max_year}"
        elif min_year:
            params["year"] = f"{min_year}-"
        elif max_year:
            params["year"] = f"-{max_year}"

        try:
            resp = requests.get(
                SEMANTIC_SCHOLAR_SEARCH_URL,
                params=params,
                headers=self.headers,
                timeout=self.timeout,
            )
            if resp.status_code == 200:
                data = resp.json().get("data", [])
                for item in data:
                    rec = self._parse_item(item)
                    if rec:
                        # Double-check year filter
                        if min_year and rec.year and rec.year < min_year:
                            continue
                        if max_year and rec.year and rec.year > max_year:
                            continue
                        records.append(rec)
                        if len(records) >= limit:
                            break
            elif resp.status_code == 429:
                logger.warning("Semantic Scholar rate limit reached (HTTP 429).")
            else:
                logger.debug("Semantic Scholar error HTTP %s: %s", resp.status_code, resp.text[:100])

        except Exception as e:
            logger.warning("Failed to query Semantic Scholar: %s", e)

        return records

    def _lookup_single_paper(self, paper_id: str, fields: str) -> Optional[PaperRecord]:
        """Fetches a specific paper by DOI, ArXivId, or CorpusId."""
        try:
            url = f"{SEMANTIC_SCHOLAR_PAPER_URL}/{paper_id}"
            resp = requests.get(url, params={"fields": fields}, headers=self.headers, timeout=self.timeout)
            if resp.status_code == 200:
                return self._parse_item(resp.json())
        except Exception as e:
            logger.debug("Semantic Scholar single lookup failed: %s", e)
        return None

    def _parse_item(self, item: Dict[str, Any]) -> Optional[PaperRecord]:
        """Parses Semantic Scholar JSON payload into standard PaperRecord."""
        title = (item.get("title") or "").strip()
        if not title:
            return None

        authors = [a.get("name") for a in item.get("authors", []) if a.get("name")]
        year = item.get("year")
        venue_data = item.get("publicationVenue") or {}
        venue = venue_data.get("name") or item.get("venue") or "Academic Publication"

        ext_ids = item.get("externalIds") or {}
        doi = ext_ids.get("DOI") or (f"10.48550/arXiv.{ext_ids['ArXiv']}" if "ArXiv" in ext_ids else None)

        oa_pdf = item.get("openAccessPdf") or {}
        pdf_url = oa_pdf.get("url")
        is_oa = bool(pdf_url)

        paper_id = item.get("paperId", "")
        url = item.get("url") or (f"https://doi.org/{doi}" if doi else f"https://www.semanticscholar.org/paper/{paper_id}")

        return PaperRecord(
            id=paper_id or doi or title,
            title=title,
            authors=authors if authors else ["Unknown Author"],
            year=int(year) if year else None,
            venue=venue,
            doi=doi,
            url=url,
            pdf_url=pdf_url,
            abstract=(item.get("abstract") or "").strip(),
            citation_count=item.get("citationCount"),
            source=self.display_name,
            source_tier=self.tier,
            category=ItemCategory.PAPER,
            is_oa=is_oa,
            extra={"external_ids": ext_ids},
        )
