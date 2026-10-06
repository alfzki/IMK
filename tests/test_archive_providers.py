"""
Unit tests for multi-archive providers, cascading paper downloader, and archive manager.
"""

import os
import tempfile
import unittest
from unittest.mock import MagicMock, patch

from calm_carson.archives.base import verify_pdf_stream
from calm_carson.archives.downloader import CascadingPaperDownloader
from calm_carson.archives.manager import ArchiveManager
from calm_carson.archives.models import (
    ArchiveTier,
    DownloadResult,
    ItemCategory,
    PaperRecord,
)
from calm_carson.archives.providers.annas_archive import AnnasArchiveProvider
from calm_carson.archives.providers.core import CoreProvider
from calm_carson.archives.providers.gutenberg import GutenbergProvider
from calm_carson.archives.providers.internet_archive import InternetArchiveProvider
from calm_carson.archives.providers.ipfs import IPFSGatewayProvider
from calm_carson.archives.providers.libgen import LibGenProvider
from calm_carson.archives.providers.scihub import SciHubProvider
from calm_carson.archives.providers.semantic_scholar import SemanticScholarProvider
from calm_carson.archives.providers.zlibrary import ZLibraryProvider


class TestArchiveModels(unittest.TestCase):
    """Tests PaperRecord normalization, conversion, and deduplication logic."""

    def test_paper_record_creation_and_dict(self):
        rec = PaperRecord(
            id="test_001",
            title="Privacy-Preserving Data Dissemination for Official Statistics",
            authors=["Alice Smith", "Bob Jones", "Charlie Brown"],
            year=2023,
            venue="IEEE Transactions on Dependable and Secure Computing",
            doi="10.1109/TDSC.2023.123456",
            url="https://doi.org/10.1109/TDSC.2023.123456",
            pdf_url="https://example.com/paper.pdf",
            abstract="A comprehensive study on statistical disclosure control.",
            citation_count=42,
            source="Semantic Scholar",
            source_tier=ArchiveTier.TIER_1_ACADEMIC,
            category=ItemCategory.PAPER,
            is_oa=True,
        )

        d = rec.to_dict()
        self.assertEqual(d["id"], "test_001")
        self.assertEqual(d["title"], "Privacy-Preserving Data Dissemination for Official Statistics")
        self.assertEqual(d["authors"], "Alice Smith, Bob Jones, Charlie Brown")
        self.assertEqual(d["year"], 2023)
        self.assertEqual(d["citations"], 42)
        self.assertTrue(d["is_oa"])

        # Test from_dict roundtrip
        rec2 = PaperRecord.from_dict(d)
        self.assertEqual(rec2.id, rec.id)
        self.assertEqual(rec2.title, rec.title)
        self.assertEqual(rec2.year, rec.year)
        self.assertEqual(rec2.citation_count, 42)

    def test_normalized_title_and_authors(self):
        rec = PaperRecord(
            id="1",
            title="  Zero-Trust Architecture: A Survey (2024)! ",
            authors=["A", "B", "C", "D", "E", "F"],
        )
        self.assertEqual(rec.get_normalized_title(), "zero trust architecture a survey 2024")
        self.assertTrue(rec.get_authors_string(max_authors=3).endswith("et al."))


class TestPdfVerification(unittest.TestCase):
    """Tests PDF magic byte stream validation."""

    def test_valid_pdf_headers(self):
        self.assertTrue(verify_pdf_stream(b"%PDF-1.4\n%...\x00"))
        self.assertTrue(verify_pdf_stream(b"%PDF-1.7\r\n"))
        self.assertTrue(verify_pdf_stream(b"\x00\x00%PDF-2.0"))

    def test_invalid_pdf_headers(self):
        self.assertFalse(verify_pdf_stream(b"<!DOCTYPE html><html><body>Error 403</body></html>"))
        self.assertFalse(verify_pdf_stream(b'{"error": "Rate limit exceeded"}'))
        self.assertFalse(verify_pdf_stream(b""))
        self.assertFalse(verify_pdf_stream(b"Random binary junk without PDF marker"))


class TestArchiveProvidersParsing(unittest.TestCase):
    """Tests mock response parsing across all archive providers."""

    def test_semantic_scholar_parsing(self):
        provider = SemanticScholarProvider()
        raw_item = {
            "paperId": "s2_abc123",
            "title": "Machine Learning in Survey Falsification",
            "authors": [{"name": "Dr. Jane Doe"}, {"name": "John Doe"}],
            "year": 2024,
            "publicationVenue": {"name": "Journal of Official Statistics"},
            "abstract": "Detecting curbstoning paradata.",
            "citationCount": 15,
            "externalIds": {"DOI": "10.1234/jos.2024.01"},
            "openAccessPdf": {"url": "https://jos.org/paper.pdf"},
        }
        rec = provider._parse_item(raw_item)
        self.assertIsNotNone(rec)
        self.assertEqual(rec.title, "Machine Learning in Survey Falsification")
        self.assertEqual(rec.authors, ["Dr. Jane Doe", "John Doe"])
        self.assertEqual(rec.year, 2024)
        self.assertEqual(rec.doi, "10.1234/jos.2024.01")
        self.assertEqual(rec.pdf_url, "https://jos.org/paper.pdf")
        self.assertTrue(rec.is_oa)

    def test_core_parsing(self):
        provider = CoreProvider()
        raw_item = {
            "id": 998877,
            "title": "Open Government Data Interoperability Framework",
            "authors": [{"name": "Univ Researcher"}],
            "yearPublished": 2023,
            "downloadUrl": "https://core.ac.uk/download/998877.pdf",
            "doi": "10.5555/core.998877",
            "abstract": "Framework for Satu Data Indonesia.",
            "citationCount": 5,
        }
        rec = provider._parse_item(raw_item)
        self.assertIsNotNone(rec)
        self.assertEqual(rec.title, "Open Government Data Interoperability Framework")
        self.assertEqual(rec.pdf_url, "https://core.ac.uk/download/998877.pdf")
        self.assertEqual(rec.year, 2023)
        self.assertTrue(rec.is_oa)

    def test_internet_archive_parsing(self):
        provider = InternetArchiveProvider()
        raw_doc = {
            "identifier": "principles-of-statistics-1950",
            "title": "Principles of Statistics",
            "creator": "Bulmer, M. G.",
            "year": "1965",
            "description": "Foundational classic textbook on mathematical statistics.",
            "downloads": 1200,
        }
        rec = provider._parse_ia_doc(raw_doc)
        self.assertIsNotNone(rec)
        self.assertEqual(rec.id, "principles-of-statistics-1950")
        self.assertEqual(rec.title, "Principles of Statistics")
        self.assertEqual(rec.year, 1965)
        self.assertEqual(rec.category, ItemCategory.BOOK)
        self.assertEqual(
            rec.pdf_url,
            "https://archive.org/download/principles-of-statistics-1950/principles-of-statistics-1950.pdf",
        )

    def test_gutenberg_parsing(self):
        provider = GutenbergProvider()
        raw_book = {
            "id": 1234,
            "title": "The Grammar of Science",
            "authors": [{"name": "Pearson, Karl", "birth_year": 1857}],
            "subjects": ["Science -- Methodology", "Mathematical statistics"],
            "languages": ["en"],
            "download_count": 850,
            "formats": {
                "application/pdf": "https://www.gutenberg.org/ebooks/1234.pdf",
                "text/html": "https://www.gutenberg.org/ebooks/1234.html",
            },
        }
        rec = provider._parse_book(raw_book)
        self.assertIsNotNone(rec)
        self.assertEqual(rec.title, "The Grammar of Science")
        self.assertEqual(rec.authors, ["Karl Pearson"])
        self.assertEqual(rec.category, ItemCategory.BOOK)
        self.assertEqual(rec.pdf_url, "https://www.gutenberg.org/ebooks/1234.pdf")

    def test_scihub_html_parsing(self):
        provider = SciHubProvider()
        mock_html = """
        <html>
        <head>
          <meta name="citation_pdf_url" content="//sci-hub.ru/storage/triplet/1234/paper.pdf">
        </head>
        <body>
          <div class="download"><a href="//sci-hub.ru/storage/triplet/1234/paper.pdf"></a></div>
        </body>
        </html>
        """
        with patch("requests.get") as mock_get:
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.text = mock_html
            mock_get.return_value = mock_resp

            rec = PaperRecord(
                id="sh_test",
                title="Paywalled Paper",
                doi="10.1145/12345.67890",
            )
            resolved_url = provider.resolve_pdf(rec)
            self.assertEqual(resolved_url, "https://sci-hub.ru/storage/triplet/1234/paper.pdf")

    def test_libgen_html_parsing(self):
        provider = LibGenProvider()
        mock_search_html = """
        <table>
          <tr>
            <td><a href="/ads.php?md5=a1b2c3d4e5f678901234567890123456" title="Deep Learning for Paradata Anomaly Detection">Deep Learning for Paradata Anomaly Detection</a></td>
            <td>Goodfellow, Ian</td>
            <td>2023</td>
          </tr>
        </table>
        """
        records = provider._parse_search_page(mock_search_html, "https://libgen.li")
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].extra["md5"], "a1b2c3d4e5f678901234567890123456")

    def test_annas_archive_parsing(self):
        provider = AnnasArchiveProvider()
        mock_anna_html = """
        <div>
          <a href="/md5/fedcba9876543210fedcba9876543210">
            <h3 class="font-bold">Statistical Disclosure Control Monograph</h3>
          </a>
          <div class="italic text-gray-500">Hundepool, Anco</div>
        </div>
        """
        records = provider._parse_annas_html(mock_anna_html, "https://annas-archive.gs")
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].title, "Statistical Disclosure Control Monograph")
        self.assertEqual(records[0].extra["md5"], "fedcba9876543210fedcba9876543210")

    def test_zlibrary_proxy_delegation(self):
        zlib = ZLibraryProvider()
        self.assertFalse(zlib.enabled_by_default)
        self.assertEqual(zlib.tier, ArchiveTier.TIER_4_DECENTRALIZED)
        # Verify proxy provider is configured
        self.assertIsInstance(zlib.proxy_provider, AnnasArchiveProvider)


class TestCascadingDownloader(unittest.TestCase):
    """Tests cascading fallback logic and PDF validation."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_direct_oa_download_success(self):
        downloader = CascadingPaperDownloader(output_dir=self.temp_dir.name)
        rec = PaperRecord(
            id="rec_oa",
            title="Open Access Paper",
            year=2023,
            pdf_url="https://example.com/oa.pdf",
        )

        with patch.object(downloader, "_try_download_url", return_value=True):
            res = downloader.download_paper(rec)
            self.assertTrue(res.success)
            self.assertFalse(res.was_fallback)

    def test_fallback_to_scihub_on_primary_failure(self):
        downloader = CascadingPaperDownloader(output_dir=self.temp_dir.name, enable_fallback=True)
        rec = PaperRecord(
            id="rec_paywall",
            title="Closed Access Paper",
            year=2024,
            doi="10.1000/182",
            pdf_url="https://example.com/dead_link.pdf",
        )

        def mock_try(url, dest):
            # Fail on dead link, succeed on scihub url
            return "sci-hub" in url

        with patch.object(downloader, "_try_download_url", side_effect=mock_try):
            with patch.object(downloader.scihub_provider, "resolve_pdf", return_value="https://sci-hub.ru/storage/paper.pdf"):
                res = downloader.download_paper(rec)
                self.assertTrue(res.success)
                self.assertTrue(res.was_fallback)
                self.assertIn("Sci-Hub", res.source_used)


class TestArchiveManager(unittest.TestCase):
    """Tests ArchiveManager orchestration, source resolution, and deduplication."""

    def test_source_resolution(self):
        mgr = ArchiveManager()
        # Default includes Tier 1 and Tier 2 libraries
        default_sources = mgr.resolve_source_names()
        self.assertIn("semanticscholar", default_sources)
        self.assertIn("core", default_sources)
        self.assertIn("internet_archive", default_sources)
        self.assertNotIn("scihub", default_sources)
        self.assertNotIn("libgen", default_sources)

        # Shadow preset explicitly resolves Tier 3
        shadow_sources = mgr.resolve_source_names("shadow")
        self.assertIn("scihub", shadow_sources)
        self.assertIn("libgen", shadow_sources)
        self.assertIn("annas_archive", shadow_sources)

        # Include books activates gutenberg
        book_sources = mgr.resolve_source_names("default", include_books=True)
        self.assertIn("gutenberg", book_sources)

    def test_deduplication(self):
        mgr = ArchiveManager()
        rec1 = PaperRecord(
            id="s2_1",
            title="Differential Privacy in Census Microdata",
            authors=["John Abowd"],
            year=2022,
            doi="10.1234/dp.2022",
            citation_count=10,
            pdf_url=None,
        )
        rec2 = PaperRecord(
            id="core_2",
            title="Differential Privacy in Census Microdata",
            authors=["J. Abowd"],
            year=2022,
            doi="10.1234/dp.2022",
            citation_count=15,
            pdf_url="https://core.ac.uk/download/1234.pdf",
            is_oa=True,
        )

        deduped = mgr.deduplicate_records([rec1, rec2])
        self.assertEqual(len(deduped), 1)
        # Should enrich with OA link and higher citation count
        self.assertTrue(deduped[0].is_oa)
        self.assertEqual(deduped[0].pdf_url, "https://core.ac.uk/download/1234.pdf")
        self.assertEqual(deduped[0].citation_count, 15)


if __name__ == "__main__":
    unittest.main()
