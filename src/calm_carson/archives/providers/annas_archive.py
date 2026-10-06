"""
calm_carson.archives.providers.annas_archive
Provider for querying Anna's Archive meta-search engine (Tier 3).
Aggregates LibGen, Sci-Hub, Z-Library, and Internet Archive.
"""

from __future__ import annotations

import logging
import re
from typing import Any, Dict, List, Optional
from urllib.parse import quote_plus

import requests

from ..base import BaseArchiveProvider
from ..models import ArchiveTier, ItemCategory, PaperRecord

logger = logging.getLogger(__name__)

ANNAS_ARCHIVE_MIRRORS = [
    "https://annas-archive.gs",
    "https://annas-archive.li",
    "https://annas-archive.org",
]


class AnnasArchiveProvider(BaseArchiveProvider):
    """
    Integrates with Anna's Archive meta-search engine.
    Also acts as a zero-login public proxy for Z-Library and DuXiu materials.
    """

    name: str = "annas_archive"
    display_name: str = "Anna's Archive"
    tier: ArchiveTier = ArchiveTier.TIER_3_SHADOW_RESOLVER
    category: str = ItemCategory.BOOK
    enabled_by_default: bool = False

    def __init__(self, timeout: int = 12):
        super().__init__(timeout=timeout)
        self.mirrors = list(ANNAS_ARCHIVE_MIRRORS)

    def search(
        self,
        query: str,
        limit: int = 10,
        min_year: Optional[int] = None,
        max_year: Optional[int] = None,
    ) -> List[PaperRecord]:
        """Searches Anna's Archive active mirrors."""
        records: List[PaperRecord] = []

        for mirror in self.mirrors:
            try:
                search_url = f"{mirror}/search?q={quote_plus(query)}"
                resp = requests.get(search_url, headers=self.headers, timeout=self.timeout)
                if resp.status_code != 200:
                    continue

                extracted = self._parse_annas_html(resp.text, mirror)
                for rec in extracted:
                    if min_year and rec.year and rec.year < min_year:
                        continue
                    if max_year and rec.year and rec.year > max_year:
                        continue
                    records.append(rec)
                    if len(records) >= limit:
                        break

                if records:
                    break

            except Exception as e:
                logger.debug("Anna's Archive mirror %s failed: %s", mirror, e)

        return records[:limit]

    def _parse_annas_html(self, html: str, mirror: str) -> List[PaperRecord]:
        """Extracts items from Anna's Archive search results."""
        records: List[PaperRecord] = []
        md5_items = re.findall(r'href=[\x27"](?:/)?md5/([a-fA-F0-9]{32})[\x27"]', html)
        seen_md5 = set()

        for md5 in md5_items:
            if md5 in seen_md5:
                continue
            seen_md5.add(md5)

            chunk_pos = html.find(f"md5/{md5}")
            context = html[max(0, chunk_pos - 100):min(len(html), chunk_pos + 600)]

            title = f"Document (MD5: {md5[:8]})"
            title_m = re.search(r'<h3[^>]*>([^<]+)</h3>', context)
            if title_m:
                title = title_m.group(1).strip()

            author_m = re.search(r'italic[^>]*>([^<]+)</div>', context)
            authors = [author_m.group(1).strip()] if author_m else ["Anna's Archive Index"]

            year_m = re.search(r'\b(19\d{2}|20[0-2]\d)\b', context)
            year = int(year_m.group(1)) if year_m else None

            detail_url = f"{mirror}/md5/{md5}"

            records.append(
                PaperRecord(
                    id=f"anna_{md5}",
                    title=title,
                    authors=authors,
                    year=year,
                    venue="Anna's Archive (Aggregated Multi-Archive)",
                    doi=None,
                    url=detail_url,
                    pdf_url=detail_url,
                    abstract=f"Arsip teragregasi (LibGen, Z-Lib, Sci-Hub, IA). Hash MD5: {md5}",
                    source=self.display_name,
                    source_tier=self.tier,
                    category=ItemCategory.BOOK,
                    is_oa=True,
                    extra={"md5": md5, "mirror": mirror},
                )
            )

        return records

    def resolve_pdf(self, record: PaperRecord) -> Optional[str]:
        """Resolves partner or IPFS download link from Anna's Archive detail page."""
        md5 = record.extra.get("md5")
        mirror = record.extra.get("mirror") or self.mirrors[0]

        if not md5 and record.pdf_url and "md5/" in record.pdf_url:
            m = re.search(r'md5/([a-fA-F0-9]{32})', record.pdf_url)
            if m:
                md5 = m.group(1)

        if not md5:
            return None

        detail_url = f"{mirror}/md5/{md5}"
        try:
            resp = requests.get(detail_url, headers=self.headers, timeout=self.timeout)
            if resp.status_code == 200:
                # Look for IPFS or partner download links
                ipfs_m = re.search(r'href=[\x27"](https?://[^"\x27]*ipfs[^"\x27]*)[\x27"]', resp.text)
                if ipfs_m:
                    return ipfs_m.group(1)

                partner_m = re.search(r'href=[\x27"](https?://[^"\x27]*(?:slow\.download|partner)[^"\x27]*)[\x27"]', resp.text)
                if partner_m:
                    return partner_m.group(1)

        except Exception as e:
            logger.debug("Failed to resolve Anna's Archive detail page %s: %s", detail_url, e)

        return None
