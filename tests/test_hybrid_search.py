"""
Unit Tests for calm_carson.search (Hierarchical Chunker, BM25, Dense, and Hybrid RRF)
"""

import os
import shutil
import tempfile
import unittest

from calm_carson.search.bm25 import BM25Index, tokenize_technical_text
from calm_carson.search.chunker import HierarchicalMarkdownChunker
from calm_carson.search.dense import DenseEmbeddingEngine
from calm_carson.search.hybrid import MarkdownHybridSearchEngine


class TestHierarchicalMarkdownChunker(unittest.TestCase):
    def setUp(self):
        self.chunker = HierarchicalMarkdownChunker(min_chunk_size=100, max_chunk_size=500)

    def test_breadcrumb_and_heading_hierarchy(self):
        sample_md = """# Judul Utama Dokumen

Ini adalah paragraf pengantar pada tingkat dokumen.

## Bab I Pendahuluan

Teks pendahuluan membahas latar belakang masalah Satu Data Indonesia.

### 1.1 Identifikasi Masalah

Masalah interoperabilitas metadata SIMETRIS dan gateway pertukaran data API.

## Bab II Tinjauan Pustaka

Pembahasan mengenai Zero Trust Architecture dan standar NIST SP 800-207.
"""
        chunks = self.chunker.chunk_text(sample_md, doc_path="proposals/test_doc.md")
        self.assertGreater(len(chunks), 0)

        # Verify that breadcrumbs contain hierarchy
        breadcrumbs = [c.breadcrumb for c in chunks]
        self.assertTrue(any("Bab I Pendahuluan" in b for b in breadcrumbs))
        self.assertTrue(any("1.1 Identifikasi Masalah" in b for b in breadcrumbs))
        self.assertTrue(any("Bab II Tinjauan Pustaka" in b for b in breadcrumbs))

        # Check that contextual header is prepended to content
        for c in chunks:
            self.assertTrue(c.content.startswith("[Konteks:"))
            self.assertEqual(c.doc_path, "proposals/test_doc.md")
            self.assertGreaterEqual(c.end_line, c.start_line)


class TestBM25Index(unittest.TestCase):
    def test_technical_tokenization(self):
        text = "Pengujian VAPT RESTful API dengan ISO-25010 dan algoritma trasgoDP."
        tokens = tokenize_technical_text(text)
        self.assertIn("vapt", tokens)
        self.assertIn("restful", tokens)
        self.assertIn("iso-25010", tokens)
        self.assertIn("iso", tokens)
        self.assertIn("25010", tokens)
        self.assertIn("trasgodp", tokens)
        self.assertIn("trasgo", tokens)
        self.assertIn("dp", tokens)

    def test_keyword_search_ranking(self):
        index = BM25Index()
        docs = [
            ("d1", "Implementasi arsitektur microservices dan API security gateway."),
            ("d2", "Pengujian penetrasi VAPT RESTful API pada aplikasi SIPADU-NG."),
            ("d3", "Diferensial privasi untuk perlindungan data mikro sensus penduduk.")
        ]
        index.index_documents(docs)

        # Query exact technical term
        res = index.search("VAPT SIPADU-NG", top_k=3)
        self.assertGreater(len(res), 0)
        self.assertEqual(res[0][0], "d2")  # Rank #1 must be d2


class TestDenseEmbeddingEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = DenseEmbeddingEngine()

    def test_dense_encoding_and_semantic_matching(self):
        texts = [
            "Pengujian kerentanan celah keamanan jaringan dan pentest web",
            "Kebijakan tata kelola interoperabilitas Satu Data Indonesia",
            "Mekanisme noise Laplace untuk privasi diferensial data tabel"
        ]
        embs = self.engine.encode(texts)
        self.assertEqual(embs.shape, (3, 384))

        self.engine.set_corpus_embeddings(["c1", "c2", "c3"], embs)
        # Query semantically close to c1 (security / cyber) without using exact words
        query = "analisis eksploitasi peretasan sistem komputer"
        res = self.engine.search(query, top_k=1)
        self.assertEqual(res[0][0], "c1")


class TestHybridSearchEngine(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.index_dir = os.path.join(self.temp_dir, "search_index")

        # Create mock markdown structure
        self.corpus_dir = os.path.join(self.temp_dir, "corpus")
        os.makedirs(os.path.join(self.corpus_dir, "proposals"), exist_ok=True)
        os.makedirs(os.path.join(self.corpus_dir, "literature"), exist_ok=True)

        doc1_content = """# Proposal Zero Trust Gateway

## Arsitektur Keamanan

Sistem Ingestion Gateway menerapkan arsitektur Zero Trust dengan validasi skema JSON dan penapisan DLP.
"""
        with open(os.path.join(self.corpus_dir, "proposals", "doc1.md"), "w") as f:
            f.write(doc1_content)

        doc2_content = """# Telaah Differential Privacy

## Teori Matematika

Penggunaan mekanisme Laplace dan Gaussian untuk menyuntikkan noise acak pada data agregat statistik.
"""
        with open(os.path.join(self.corpus_dir, "literature", "doc2.md"), "w") as f:
            f.write(doc2_content)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_hybrid_indexing_and_search(self):
        engine = MarkdownHybridSearchEngine(index_dir=self.index_dir)
        num_chunks = engine.index_corpus(base_dir=self.corpus_dir, subdirs=["proposals", "literature"], include_root_md=False)
        self.assertGreater(num_chunks, 0)

        # Test Hybrid Search
        results = engine.search("Zero Trust Gateway validasi skema", top_k=2, mode="hybrid")
        self.assertGreater(len(results), 0)
        top = results[0]
        self.assertIn("doc1.md", top.doc_path)
        self.assertIsNotNone(top.rrf_score)
        self.assertIsNotNone(top.dense_score)
        self.assertIsNotNone(top.sparse_score)

        # Test Directory Filtering
        filtered_results = engine.search("mekanisme privasi", top_k=2, filter_dir="literature")
        for r in filtered_results:
            self.assertTrue(r.doc_path.startswith("literature"))


if __name__ == "__main__":
    unittest.main()
