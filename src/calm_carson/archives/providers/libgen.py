"""
calm_carson.archives.providers.libgen
Provider for querying and resolving Library Genesis (LibGen) mirrors (Tier 3).
"""

from __future__ import annotations

import logging
import re
from typing import Any, Dict, List, Optional
from urllib.parse import quote_plus, urljoin

import requests

from ..base import BaseArchiveProvider
from ..models import ArchiveTier, ItemCategory, PaperRecord

logger = logging.getLogger(__name__)

LIBGEN_MIRRORS = [
    "https://libgen.li",
    "https://libgen.st",
    "http://libgen.is",
]


class LibGenProvider(BaseArchiveProvider):
    """
    Integrates with Library Genesis for academic books, monographs, and scientific papers.
    Activated explicitly via --sources or as an automatic cascading fallback.
    """

    name: str = "libgen"
    display_name: str = "Library Genesis"
    tier: ArchiveTier = ArchiveTier.TIER_3_SHADOW_RESOLVER
    category: str = ItemCategory.BOOK
    enabled_by_default: bool = False

    def __init__(self, timeout: int = 6):
        super().__init__(timeout=timeout)
        self.mirrors = list(LIBGEN_MIRRORS)

    def search(
        self,
        query: str,
        limit: int = 10,
        min_year: Optional[int] = None,
        max_year: Optional[int] = None,
    ) -> List[PaperRecord]:
        """Searches LibGen mirrors for books and papers."""
        records: List[PaperRecord] = []

        for mirror in self.mirrors:
            try:
                # Check if query is DOI or general text
                is_doi = bool(re.search(r"\b10\.\d{4,9}/", query))
                col = "doi" if is_doi else "t"
                search_url = f"{mirror}/index.php?req={quote_plus(query)}&columns%5B%5D={col}"

                resp = requests.get(search_url, headers=self.headers, timeout=self.timeout)
                if resp.status_code != 200:
                    continue

                extracted = self._parse_search_page(resp.text, mirror)
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
                logger.debug("LibGen mirror %s error: %s", mirror, e)

        return records[:limit]

    def _parse_search_page(self, html: str, mirror: str) -> List[PaperRecord]:
        """Parses LibGen HTML search results table."""
        records: List[PaperRecord] = []

        # Find md5 links: ads.php?md5=... or get.php?md5=...
        md5_matches = re.findall(r'href=[\x27"](?:/)?(ads\.php\?md5=([a-fA-F0-9]{32}))[\x27"]', html)
        seen_md5 = set()

        for rel_link, md5 in md5_matches:
            if md5 in seen_md5:
                continue
            seen_md5.add(md5)

            # Try to extract context around the md5 link
            chunk_start = max(0, html.find(md5) - 300)
            chunk_end = min(len(html), html.find(md5) + 600)
            context = html[chunk_start:chunk_end]

            # Attempt to extract title
            title = f"Document (MD5: {md5[:8]})"
            title_m = re.search(r'<a[^>]+title=[\x27"]([^\x27"]+)[\x27"]', context)
            if title_m and len(title_m.group(1)) > 3:
                title = title_m.group(1).strip()
            else:
                title_alt = re.search(r'>([^<]{10,80})</a>', context)
                if title_alt:
                    title = title_alt.group(1).strip()

            # Attempt year extraction
            year_m = re.search(r'\b(19\d{2}|20[0-2]\d)\b', context)
            year = int(year_m.group(1)) if year_m else None

            # Attempt author extraction
            author_m = re.search(r'author=([^&"\'>]+)', context)
            authors = [author_m.group(1).replace("+", " ").strip()] if author_m else ["LibGen Author"]

            ads_url = f"{mirror}/ads.php?md5={md5}"

            records.append(
                PaperRecord(
                    id=f"libgen_{md5}",
                    title=title,
                    authors=authors,
                    year=year,
                    venue="Library Genesis Archive",
                    doi=None,
                    url=ads_url,
                    pdf_url=ads_url,  # ads.php can be resolved to direct get.php
                    abstract=f"Arsip buku/paper ilmiah terekam di Library Genesis. Hash MD5: {md5}",
                    source=self.display_name,
                    source_tier=self.tier,
                    category=ItemCategory.BOOK,
                    is_oa=True,
                    extra={"md5": md5, "mirror": mirror},
                )
            )

        return records

    def resolve_pdf(self, record: PaperRecord) -> Optional[str]:
        """Resolves direct download URL from LibGen ads.php page or searches by DOI."""
        md5 = record.extra.get("md5")
        mirror = record.extra.get("mirror") or self.mirrors[0]

        if not md5 and record.doi:
            # Query by DOI to find MD5
            hits = self.search(record.doi, limit=1)
            if hits and hits[0].extra.get("md5"):
                md5 = hits[0].extra["md5"]
                mirror = hits[0].extra.get("mirror", mirror)

        if not md5 and record.pdf_url and "md5=" in record.pdf_url:
            m = re.search(r'md5=([a-fA-F0-9]{32})', record.pdf_url)
            if m:
                md5 = m.group(1)

        if not md5:
            return None

        # Query ads page to get get.php link
        ads_url = f"{mirror}/ads.php?md5={md5}"
        try:
            resp = requests.get(ads_url, headers=self.headers, timeout=self.timeout)
            if resp.status_code == 200:
                get_m = re.search(r'href=[\x27"](get\.php\?md5=[^"\x27]+)[\x27"]', resp.text)
                if get_m:
                    direct_url = urljoin(mirror, get_m.group(1))
                    logger.info("LibGen berhasil meresolusi unduhan langsung: %s", direct_url)
                    return direct_url

                # Check if an IPFS link is provided
                ipfs_m = re.search(r'href=[\x27"](https?://[^"\x27]*ipfs[^"\x27]*)[\x27"]', resp.text)
                if ipfs_m:
                    return ipfs_m.group(1)

        except Exception as e:
            logger.debug("Failed to resolve LibGen ads page %s: %s", ads_url, e)

        return None
