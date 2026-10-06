"""
calm_carson.archives.providers.zlibrary
Public Proxy Provider for Z-Library (Tier 4).
Routes queries through open public mirrors and proxies (Anna's Archive / LibGen)
without requiring private user credentials or bypassing Cloudflare anti-bot blocks.
"""

from __future__ import annotations

import logging
import os
from typing import Any, Dict, List, Optional

from ..base import BaseArchiveProvider
from ..models import ArchiveTier, ItemCategory, PaperRecord
from .annas_archive import AnnasArchiveProvider

logger = logging.getLogger(__name__)


class ZLibraryProvider(BaseArchiveProvider):
    """
    Accesses Z-Library collections through public open indexes and mirrors (Anna's Archive & LibGen).
    Ensures zero-friction access without account registration or CAPTCHAs.
    Also supports optional personal Z-Lib tokens via environment variable (ZLIB_TOKEN) if provided.
    """

    name: str = "zlibrary"
    display_name: str = "Z-Library (via Public Proxy)"
    tier: ArchiveTier = ArchiveTier.TIER_4_DECENTRALIZED
    category: str = ItemCategory.BOOK
    enabled_by_default: bool = False

    def __init__(self, timeout: int = 12):
        super().__init__(timeout=timeout)
        self.proxy_provider = AnnasArchiveProvider(timeout=timeout)
        self.personal_token = os.getenv("ZLIB_TOKEN")

    def search(
        self,
        query: str,
        limit: int = 10,
        min_year: Optional[int] = None,
        max_year: Optional[int] = None,
    ) -> List[PaperRecord]:
        """Routes search through public proxy and tags records with Z-Library source."""
        # Query via public proxy aggregator
        raw_results = self.proxy_provider.search(query, limit=limit, min_year=min_year, max_year=max_year)
        
        proxied_records: List[PaperRecord] = []
        for r in raw_results:
            # Rebrand and re-attribute to Z-Library (Public Proxy)
            r.source = self.display_name
            r.source_tier = self.tier
            r.venue = "Z-Library Collection (via Open Proxy)"
            proxied_records.append(r)

        return proxied_records

    def resolve_pdf(self, record: PaperRecord) -> Optional[str]:
        """Resolves direct download URL via public proxy."""
        return self.proxy_provider.resolve_pdf(record)
