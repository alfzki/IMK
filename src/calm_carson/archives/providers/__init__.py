"""
calm_carson.archives.providers
Archive search and download providers across Tier 1, 2, 3, and 4.
"""

from .annas_archive import AnnasArchiveProvider
from .core import CoreProvider
from .gutenberg import GutenbergProvider
from .internet_archive import InternetArchiveProvider
from .ipfs import IPFSGatewayProvider
from .libgen import LibGenProvider
from .scihub import SciHubProvider
from .semantic_scholar import SemanticScholarProvider
from .zlibrary import ZLibraryProvider

__all__ = [
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
