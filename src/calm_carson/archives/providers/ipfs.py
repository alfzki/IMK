"""
calm_carson.archives.providers.ipfs
Provider and transport layer for decentralized IPFS content resolution (Tier 4).
"""

from __future__ import annotations

import logging
import re
from typing import Any, Dict, List, Optional

import requests

from ..base import BaseArchiveProvider, verify_pdf_stream
from ..models import ArchiveTier, ItemCategory, PaperRecord

logger = logging.getLogger(__name__)

PUBLIC_IPFS_GATEWAYS = [
    "https://cloudflare-ipfs.com",
    "https://ipfs.io",
    "https://gateway.pinata.cloud",
    "https://dweb.link",
]


class IPFSGatewayProvider(BaseArchiveProvider):
    """
    Decentralized transport resolver for fetching publications and datasets
    stored on IPFS via public gateway rotation.
    """

    name: str = "ipfs"
    display_name: str = "IPFS Gateway"
    tier: ArchiveTier = ArchiveTier.TIER_4_DECENTRALIZED
    category: str = ItemCategory.PAPER
    enabled_by_default: bool = False

    def __init__(self, timeout: int = 10):
        super().__init__(timeout=timeout)
        self.gateways = list(PUBLIC_IPFS_GATEWAYS)

    def search(
        self,
        query: str,
        limit: int = 10,
        min_year: Optional[int] = None,
        max_year: Optional[int] = None,
    ) -> List[PaperRecord]:
        """
        IPFS is an address-by-content (CID) decentralized storage protocol,
        not a centralized keyword search engine.
        If the query contains a CID hash, resolves it directly.
        """
        cid_match = re.search(r"\b(Qm[1-9A-HJ-NP-Za-km-z]{44}|bafy[a-z0-9]{55})\b", query)
        if not cid_match:
            return []

        cid = cid_match.group(1)
        return [
            PaperRecord(
                id=f"ipfs_{cid}",
                title=f"IPFS Content Object ({cid[:12]}...)",
                authors=["Decentralized IPFS Contributor"],
                year=None,
                venue="InterPlanetary File System (IPFS)",
                doi=None,
                url=f"{self.gateways[0]}/ipfs/{cid}",
                pdf_url=f"{self.gateways[0]}/ipfs/{cid}",
                abstract=f"Dokumen biner terdesentralisasi di jaringan IPFS dengan CID: {cid}",
                source=self.display_name,
                source_tier=self.tier,
                category=ItemCategory.PAPER,
                is_oa=True,
                ipfs_cid=cid,
            )
        ]

    def resolve_pdf(self, record: PaperRecord) -> Optional[str]:
        """Resolves active gateway URL for a record containing an IPFS CID."""
        cid = record.ipfs_cid
        if not cid and record.pdf_url:
            m = re.search(r"/ipfs/([a-zA-Z0-9]+)", record.pdf_url)
            if m:
                cid = m.group(1)

        if not cid:
            return None

        # Test gateways with lightweight HEAD request
        for gw in self.gateways:
            gw_url = f"{gw}/ipfs/{cid}"
            try:
                resp = requests.head(gw_url, headers=self.headers, timeout=5, allow_redirects=True)
                if resp.status_code == 200:
                    return gw_url
            except Exception:
                continue

        # Default to first gateway if HEAD is blocked
        return f"{self.gateways[0]}/ipfs/{cid}"
