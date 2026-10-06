"""
calm_carson.archives.providers.gutenberg
Provider for querying Project Gutenberg via Gutendex REST API (Tier 2 - Public Domain Books & Monographs).
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

import requests

from ..base import BaseArchiveProvider
from ..models import ArchiveTier, ItemCategory, PaperRecord

logger = logging.getLogger(__name__)

GUTENDEX_API_URL = "https://gutendex.com/books/"


class GutenbergProvider(BaseArchiveProvider):
    """
    Integrates with Project Gutenberg for public-domain foundational textbooks,
    mathematical treaties, and monographs.
    Separated specifically for book/monograph citations (which are permissible even when > 5 years old).
    """

    name: str = "gutenberg"
    display_name: str = "Project Gutenberg"
    tier: ArchiveTier = ArchiveTier.TIER_2_PUBLIC_LIB
    category: str = ItemCategory.BOOK
    # Disabled by default in general paper searches, activated when books/monographs are targeted
    enabled_by_default: bool = False

    def search(
        self,
        query: str,
        limit: int = 10,
        min_year: Optional[int] = None,
        max_year: Optional[int] = None,
    ) -> List[PaperRecord]:
        """Queries Gutendex API for public domain books."""
        records: List[PaperRecord] = []
        params = {"search": query}

        try:
            resp = requests.get(
                GUTENDEX_API_URL,
                params=params,
                headers=self.headers,
                timeout=self.timeout,
            )
            if resp.status_code == 200:
                data = resp.json()
                results = data.get("results", [])
                for item in results:
                    rec = self._parse_book(item)
                    if rec:
                        # Gutenberg books are historical/classic domain, so year filters are applied leniently
                        if min_year and rec.year and rec.year < min_year:
                            # If min_year is modern (e.g. 2021) and user explicitly searched gutenberg, allow historical books
                            pass
                        records.append(rec)
                        if len(records) >= limit:
                            break
            else:
                logger.debug("Gutendex returned HTTP %s: %s", resp.status_code, resp.text[:100])

        except Exception as e:
            logger.warning("Failed to query Project Gutenberg (Gutendex): %s", e)

        return records

    def _parse_book(self, item: Dict[str, Any]) -> Optional[PaperRecord]:
        """Converts Gutendex book object to PaperRecord."""
        title = (item.get("title") or "").strip()
        book_id = item.get("id")
        if not title or not book_id:
            return None

        authors = []
        birth_year = None
        for a in item.get("authors", []):
            name = a.get("name")
            if name:
                # Format name: "Last, First" -> "First Last"
                if "," in name:
                    parts = name.split(",", 1)
                    authors.append(f"{parts[1].strip()} {parts[0].strip()}")
                else:
                    authors.append(name)
            if not birth_year and a.get("birth_year"):
                birth_year = a.get("birth_year")

        formats = item.get("formats", {})
        # Prefer direct PDF if available, otherwise EPUB or text link
        pdf_url = formats.get("application/pdf") or formats.get("application/epub+zip") or formats.get("text/html")
        landing_url = f"https://www.gutenberg.org/ebooks/{book_id}"
        subjects = item.get("subjects", [])

        return PaperRecord(
            id=f"gutenberg_{book_id}",
            title=title,
            authors=authors if authors else ["Public Domain Author"],
            year=birth_year,  # Approximate historical anchor
            venue="Project Gutenberg Classic Library",
            doi=None,
            url=landing_url,
            pdf_url=pdf_url,
            abstract=f"Subjek: {', '.join(subjects[:4])} | Bahasa: {', '.join(item.get('languages', []))}",
            citation_count=item.get("download_count"),
            source=self.display_name,
            source_tier=self.tier,
            category=ItemCategory.BOOK,
            is_oa=True,
            extra={"gutendex_id": book_id, "formats": formats},
        )
