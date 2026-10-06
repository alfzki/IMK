"""
calm_carson.archives
Unified multi-archive search and retrieval package for scientific papers and educational monographs.
Supports Semantic Scholar, CORE, Internet Archive, Gutenberg, Sci-Hub, LibGen, Anna's Archive, IPFS, and Z-Library.
"""

from .base import BaseArchiveProvider, verify_pdf_stream
from .downloader import CascadingPaperDownloader
from .manager import ArchiveManager
from .models import ArchiveTier, DownloadResult, ItemCategory, PaperRecord
from .providers import (
    AnnasArchiveProvider,
    CoreProvider,
    GutenbergProvider,
    InternetArchiveProvider,
    IPFSGatewayProvider,
    LibGenProvider,
    SciHubProvider,
    SemanticScholarProvider,
    ZLibraryProvider,
)

__all__ = [
    "ArchiveTier",
    "ItemCategory",
    "PaperRecord",
    "DownloadResult",
    "BaseArchiveProvider",
    "verify_pdf_stream",
    "CascadingPaperDownloader",
    "ArchiveManager",
    "SemanticScholarProvider",
    "CoreProvider",
    "InternetArchiveProvider",
    "GutenbergProvider",
    "SciHubProvider",
    "LibGenProvider",
    "AnnasArchiveProvider",
    "IPFSGatewayProvider",
    "ZLibraryProvider",
]
