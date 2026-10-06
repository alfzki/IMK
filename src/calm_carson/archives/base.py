"""
calm_carson.archives.base
Abstract base class for all archive search and retrieval providers.
"""

from __future__ import annotations

import logging
import os
import re
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

import requests

from .models import ArchiveTier, ItemCategory, PaperRecord

logger = logging.getLogger(__name__)

DEFAULT_USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"


def verify_pdf_stream(first_chunk: bytes) -> bool:
    """Verifies that the initial bytes of a stream correspond to a genuine PDF document (%PDF-)."""
    if not first_chunk:
        return False
    # PDF specification: starts with %PDF- (optionally preceded by UTF-8 BOM or whitespace/nulls)
    clean = first_chunk.lstrip(b"\x00\xef\xbb\xbf\r\n\t ")
    return clean.startswith(b"%PDF-")


class BaseArchiveProvider(ABC):
    """Abstract base provider for searching and resolving scientific documents and books."""

    name: str = "base"
    display_name: str = "Base Provider"
    tier: ArchiveTier = ArchiveTier.TIER_1_ACADEMIC
    category: str = ItemCategory.PAPER
    enabled_by_default: bool = True

    def __init__(self, timeout: int = 15):
        self.timeout = timeout
        self.headers = {
            "User-Agent": DEFAULT_USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,application/json,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9,id;q=0.8",
        }

    @abstractmethod
    def search(
        self,
        query: str,
        limit: int = 10,
        min_year: Optional[int] = None,
        max_year: Optional[int] = None,
    ) -> List[PaperRecord]:
        """Executes a search query against the archive."""
        pass

    def resolve_pdf(self, record: PaperRecord) -> Optional[str]:
        """
        Attempts to resolve or extract a direct PDF download link for a given record.
        Default implementation returns the existing pdf_url if present.
        """
        return record.pdf_url

    def download_file(
        self,
        url: str,
        output_path: str,
        verify_pdf: bool = True,
        headers: Optional[Dict[str, str]] = None,
    ) -> bool:
        """Downloads a file stream safely, verifying PDF header bytes if requested."""
        req_headers = dict(self.headers)
        if headers:
            req_headers.update(headers)

        try:
            resp = requests.get(url, headers=req_headers, timeout=self.timeout * 2, stream=True, allow_redirects=True)
            if resp.status_code != 200:
                logger.debug("Download failed with HTTP %s for url: %s", resp.status_code, url)
                return False

            first_chunk = next(resp.iter_content(chunk_size=2048), b"")
            if verify_pdf and not verify_pdf_stream(first_chunk):
                logger.debug("Verification failed: Not a genuine PDF stream (received: %s...)", first_chunk[:50])
                return False

            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
            temp_path = output_path + ".tmp"
            
            with open(temp_path, "wb") as f:
                f.write(first_chunk)
                for chunk in resp.iter_content(chunk_size=16384):
                    if chunk:
                        f.write(chunk)

            # Check if file size is non-trivial (> 2KB)
            if os.path.getsize(temp_path) < 2048:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                return False

            if os.path.exists(output_path):
                os.remove(output_path)
            os.rename(temp_path, output_path)
            return True

        except Exception as e:
            logger.debug("Error downloading %s: %s", url, e)
            temp_path = output_path + ".tmp"
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except OSError:
                    pass
            return False
