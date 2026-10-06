"""
calm_carson.archives.downloader
Cascading Paper Downloader with strict PDF header verification and fallback resolver ladder.
"""

from __future__ import annotations

import logging
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

from .base import BaseArchiveProvider, DEFAULT_USER_AGENT, verify_pdf_stream
from .models import DownloadResult, PaperRecord
from .providers.ipfs import IPFSGatewayProvider
from .providers.libgen import LibGenProvider
from .providers.scihub import SciHubProvider

logger = logging.getLogger(__name__)


def sanitize_filename(title: str, max_len: int = 80) -> str:
    """Sanitizes a string to produce a valid and clean filename."""
    clean = re.sub(r'[\\/*?:"<>|]', "", title)
    clean = re.sub(r"\s+", "_", clean).strip("_")
    return clean[:max_len]


class CascadingPaperDownloader:
    """
    Downloads research papers and monographs using a cascading multi-tier strategy:
    Tier 1: Direct Open Access Link (OpenAlex, arXiv, Semantic Scholar, CORE)
    Tier 2: Public Library Storage (Internet Archive, Gutenberg)
    Tier 3: Paywall Resolver Fallback (Sci-Hub, LibGen)
    Tier 4: Decentralized Transport (IPFS Gateways)
    
    Every download is strictly validated for %PDF- binary headers to eliminate HTML/captcha pages.
    """

    def __init__(
        self,
        output_dir: str = "literature/pdfs",
        enable_fallback: bool = True,
        timeout: int = 8,
    ):
        self.output_dir = Path(output_dir)
        self.enable_fallback = enable_fallback
        self.timeout = timeout

        # Fallback resolvers with snappy timeouts
        self.scihub_provider = SciHubProvider(timeout=timeout)
        self.libgen_provider = LibGenProvider(timeout=timeout)
        self.ipfs_provider = IPFSGatewayProvider(timeout=timeout)

    def download_paper(
        self,
        record: PaperRecord,
        custom_filename: Optional[str] = None,
    ) -> DownloadResult:
        """Attempts to download the paper with automatic cascading resolution."""
        self.output_dir.mkdir(parents=True, exist_ok=True)

        year_str = str(record.year) if record.year else "nodate"
        safe_title = sanitize_filename(record.title)
        filename = custom_filename or f"INTL_{year_str}_{safe_title}.pdf"
        dest_path = str(self.output_dir / filename)

        # If file already exists and is a valid PDF, return early
        if os.path.exists(dest_path) and os.path.getsize(dest_path) > 2048:
            with open(dest_path, "rb") as f:
                head = f.read(50)
                if verify_pdf_stream(head):
                    return DownloadResult(
                        success=True,
                        filepath=dest_path,
                        source_used="Local Cache",
                        filesize_bytes=os.path.getsize(dest_path),
                        was_fallback=False,
                    )

        def _safe_size(p: str) -> int:
            return os.path.getsize(p) if os.path.exists(p) else 0

        # Step 1: Direct primary URL
        if record.pdf_url:
            logger.info("Mencoba unduh langsung dari URL primer: %s", record.pdf_url)
            if self._try_download_url(record.pdf_url, dest_path):
                return DownloadResult(
                    success=True,
                    filepath=dest_path,
                    source_used=record.source or "Primary OA",
                    filesize_bytes=_safe_size(dest_path),
                    was_fallback=False,
                )

        if not self.enable_fallback:
            return DownloadResult(
                success=False,
                error="Primary download failed and fallback is disabled.",
            )

        # Step 2: Fallback to Sci-Hub if DOI is available
        if record.doi:
            logger.info("Primary URL gagal. Mencoba fallback Sci-Hub untuk DOI: %s", record.doi)
            sh_url = self.scihub_provider.resolve_pdf(record)
            if sh_url and self._try_download_url(sh_url, dest_path):
                return DownloadResult(
                    success=True,
                    filepath=dest_path,
                    source_used="Sci-Hub (Fallback)",
                    filesize_bytes=_safe_size(dest_path),
                    was_fallback=True,
                )

        # Step 3: Fallback to LibGen by DOI or Title
        logger.info("Mencoba fallback Library Genesis...")
        lg_url = self.libgen_provider.resolve_pdf(record)
        if lg_url and self._try_download_url(lg_url, dest_path):
            return DownloadResult(
                success=True,
                filepath=dest_path,
                source_used="LibGen (Fallback)",
                filesize_bytes=_safe_size(dest_path),
                was_fallback=True,
            )

        # Step 4: Fallback to IPFS if CID is recorded
        if record.ipfs_cid:
            logger.info("Mencoba fallback IPFS Gateway untuk CID: %s", record.ipfs_cid)
            ipfs_url = self.ipfs_provider.resolve_pdf(record)
            if ipfs_url and self._try_download_url(ipfs_url, dest_path):
                return DownloadResult(
                    success=True,
                    filepath=dest_path,
                    source_used="IPFS Gateway (Fallback)",
                    filesize_bytes=_safe_size(dest_path),
                    was_fallback=True,
                )

        return DownloadResult(
            success=False,
            error="Seluruh rantai unduh (OA, Sci-Hub, LibGen, IPFS) gagal atau berkas bukan PDF valid.",
        )

    def _try_download_url(self, url: str, dest_path: str) -> bool:
        """Executes a single download attempt and verifies genuine PDF bytes."""
        import requests
        headers = {
            "User-Agent": DEFAULT_USER_AGENT,
            "Accept": "application/pdf,*/*",
        }
        try:
            resp = requests.get(url, headers=headers, timeout=self.timeout, stream=True, allow_redirects=True)
            if resp.status_code != 200:
                return False

            stream_iter = resp.iter_content(chunk_size=16384)
            first_chunk = next(stream_iter, b"")
            if not verify_pdf_stream(first_chunk):
                logger.debug("URL %s tidak mengembalikan berkas PDF valid (header: %s...)", url, first_chunk[:30])
                return False

            temp_path = dest_path + ".tmp"
            with open(temp_path, "wb") as f:
                f.write(first_chunk)
                for chunk in stream_iter:
                    if chunk:
                        f.write(chunk)

            if os.path.getsize(temp_path) < 2048:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                return False

            if os.path.exists(dest_path):
                os.remove(dest_path)
            os.rename(temp_path, dest_path)
            return True

        except Exception as e:
            logger.debug("Download error for %s: %s", url, e)
            temp_path = dest_path + ".tmp"
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except OSError:
                    pass
            return False
