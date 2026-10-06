"""
calm_carson.archives.providers.core
Provider for querying the CORE API v3 (World's Largest Open Access Repository Aggregator - Tier 1).
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

import requests

from ..base import BaseArchiveProvider
from ..models import ArchiveTier, ItemCategory, PaperRecord

logger = logging.getLogger(__name__)

CORE_API_SEARCH_URL = "https://api.core.ac.uk/v3/search/works"


class CoreProvider(BaseArchiveProvider):
    """Integrates with CORE (core.ac.uk) for harvesting university and institutional repositories."""

    name: str = "core"
    display_name: str = "CORE"
    tier: ArchiveTier = ArchiveTier.TIER_1_ACADEMIC
    category: str = ItemCategory.PAPER
    enabled_by_default: bool = True

    def __init__(self, api_key: Optional[str] = None, timeout: int = 15):
        super().__init__(timeout=timeout)
        self.api_key = api_key
        if self.api_key:
            self.headers["Authorization"] = f"Bearer {self.api_key}"

    def search(
        self,
        query: str,
        limit: int = 10,
        min_year: Optional[int] = None,
        max_year: Optional[int] = None,
    ) -> List[PaperRecord]:
        """Queries CORE API v3 for open-access papers."""
        records: List[PaperRecord] = []

        params = {
            "q": query,
            "limit": min(limit * 3, 50),
            "offset": 0,
        }

        try:
            resp = requests.get(
                CORE_API_SEARCH_URL,
                params=params,
                headers=self.headers,
                timeout=self.timeout,
            )
            if resp.status_code == 200:
                data = resp.json()
                results = data.get("results", [])
                for item in results:
                    rec = self._parse_item(item)
                    if rec:
                        if min_year and rec.year and rec.year < min_year:
                            continue
                        if max_year and rec.year and rec.year > max_year:
                            continue
                        records.append(rec)
                        if len(records) >= limit:
                            break
            else:
                logger.debug("CORE API response HTTP %s: %s", resp.status_code, resp.text[:100])

        except Exception as e:
            logger.warning("Failed to query CORE API: %s", e)

        return records

    def _parse_item(self, item: Dict[str, Any]) -> Optional[PaperRecord]:
        """Converts raw CORE work result into standard PaperRecord."""
        title = (item.get("title") or "").strip()
        if not title:
            return None

        authors = []
        for a in item.get("authors", []):
            if isinstance(a, dict) and a.get("name"):
                authors.append(a["name"])
            elif isinstance(a, str):
                authors.append(a)

        year = item.get("yearPublished")
        if not year:
            published_date = item.get("publishedDate") or ""
            if len(published_date) >= 4 and published_date[:4].isdigit():
                year = int(published_date[:4])

        download_url = item.get("downloadUrl")
        source_urls = item.get("sourceFulltextUrls") or []
        pdf_url = download_url or (source_urls[0] if source_urls else None)

        journals = item.get("journals") or []
        venue = journals[0].get("title") if journals and isinstance(journals[0], dict) else item.get("publisher", "CORE Institutional Repository")

        doi = item.get("doi") or None
        rec_id = str(item.get("id") or doi or title)
        links = item.get("links") or []
        landing_url = (links[0].get("url") if links and isinstance(links[0], dict) else None) or (f"https://core.ac.uk/works/{rec_id}")

        return PaperRecord(
            id=rec_id,
            title=title,
            authors=authors if authors else ["Unknown Author"],
            year=int(year) if year else None,
            venue=venue,
            doi=doi,
            url=landing_url,
            pdf_url=pdf_url,
            abstract=(item.get("abstract") or "").strip(),
            citation_count=item.get("citationCount"),
            source=self.display_name,
            source_tier=self.tier,
            category=ItemCategory.PAPER,
            is_oa=bool(pdf_url),
            extra={"oai_ids": item.get("oaiIds", [])},
        )
