"""
calm_carson.archives.providers.scihub
Provider for Sci-Hub paper PDF resolution via active mirror rotation (Tier 3).
"""

from __future__ import annotations

import logging
import re
from typing import Any, Dict, List, Optional

import requests

from ..base import BaseArchiveProvider, verify_pdf_stream
from ..models import ArchiveTier, ItemCategory, PaperRecord

logger = logging.getLogger(__name__)

SCIHUB_MIRRORS = [
    "https://sci-hub.ru",
    "https://sci-hub.st",
]


class SciHubProvider(BaseArchiveProvider):
    """
    Resolves paywalled academic papers by DOI through Sci-Hub mirror failover.
    Activated explicitly via --sources or as an automatic cascading fallback.
    """

    name: str = "scihub"
    display_name: str = "Sci-Hub"
    tier: ArchiveTier = ArchiveTier.TIER_3_SHADOW_RESOLVER
    category: str = ItemCategory.PAPER
    enabled_by_default: bool = False

    def __init__(self, timeout: int = 6):
        super().__init__(timeout=timeout)
        self.mirrors = list(SCIHUB_MIRRORS)

    def search(
        self,
        query: str,
        limit: int = 10,
        min_year: Optional[int] = None,
        max_year: Optional[int] = None,
    ) -> List[PaperRecord]:
        """
        Sci-Hub is primarily a DOI-based paper resolver rather than a keyword search engine.
        If the query contains a DOI, resolves and returns the record directly.
        """
        doi_match = re.search(r"\b(10\.\d{4,9}/[-._;()/:A-Za-z0-9]+)\b", query)
        if not doi_match:
            logger.info("Sci-Hub requires a DOI for direct retrieval. Keyword search should use OpenAlex/CORE/S2.")
            return []

        doi = doi_match.group(1)
        pdf_url = self._resolve_doi_to_pdf(doi)
        if pdf_url:
            return [
                PaperRecord(
                    id=f"scihub_{doi}",
                    title=f"Publication (DOI: {doi})",
                    authors=["Sci-Hub Archive Record"],
                    year=None,
                    venue="Sci-Hub Academic Resolver",
                    doi=doi,
                    url=f"https://doi.org/{doi}",
                    pdf_url=pdf_url,
                    abstract=f"Tautan PDF paper berhasil diresolusi melalui mirror Sci-Hub untuk DOI {doi}.",
                    source=self.display_name,
                    source_tier=self.tier,
                    category=ItemCategory.PAPER,
                    is_oa=True,
                )
            ]
        return []

    def resolve_pdf(self, record: PaperRecord) -> Optional[str]:
        """Resolves direct PDF link for a paper record using its DOI."""
        doi = record.doi
        if not doi and record.url:
            m = re.search(r"\b(10\.\d{4,9}/[-._;()/:A-Za-z0-9]+)\b", record.url)
            if m:
                doi = m.group(1)

        if not doi:
            return None

        return self._resolve_doi_to_pdf(doi)

    def _resolve_doi_to_pdf(self, doi: str) -> Optional[str]:
        """Tries active mirrors in order to extract the direct PDF stream URL."""
        for mirror in self.mirrors:
            try:
                target_url = f"{mirror}/{doi}"
                resp = requests.get(target_url, headers=self.headers, timeout=self.timeout, allow_redirects=True)
                if resp.status_code != 200:
                    continue

                html = resp.text

                # 1. Search meta citation_pdf_url
                meta_match = re.search(r'<meta[^>]+name=[\x27"]citation_pdf_url[\x27"][^>]+content=[\x27"]([^\x27"]+)[\x27"]', html, re.I)
                pdf_link = meta_match.group(1) if meta_match else None

                # 2. Search embed or iframe or object
                if not pdf_link:
                    embed_match = re.search(r'<(?:embed|iframe|object)[^>]+(?:src|data)=[\x27"]([^\x27"]+\.pdf[^\x27"]*)[\x27"]', html, re.I)
                    if embed_match:
                        pdf_link = embed_match.group(1)

                # 3. Search download button link
                if not pdf_link:
                    dl_match = re.search(r'class=[\x27"]download[\x27"][^>]*>\s*<a\s+href=[\x27"]([^\x27"]+)[\x27"]', html, re.I)
                    if dl_match:
                        pdf_link = dl_match.group(1)

                if pdf_link:
                    # Normalize protocol-relative URL (e.g. //sci-hub.red/...)
                    if pdf_link.startswith("//"):
                        pdf_link = "https:" + pdf_link
                    elif pdf_link.startswith("/"):
                        pdf_link = mirror.rstrip("/") + pdf_link

                    logger.info("Sci-Hub berhasil meresolusi DOI %s -> %s", doi, pdf_link)
                    return pdf_link

            except Exception as e:
                logger.debug("Sci-Hub mirror %s failed: %s", mirror, e)

        return None
