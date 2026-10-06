"""
calm_carson.search.hybrid
Hybrid Retrieval Engine combining dense semantic vector search (MiniLM on CUDA)
and sparse BM25Okapi keyword search with Reciprocal Rank Fusion (RRF).
"""

import glob
import json
import os
import sqlite3
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from calm_carson.search.bm25 import BM25Index
from calm_carson.search.chunker import HierarchicalMarkdownChunker, MarkdownChunk
from calm_carson.search.dense import DenseEmbeddingEngine


@dataclass
class SearchResult:
    chunk_id: str
    doc_path: str
    doc_title: str
    breadcrumb: str
    content: str
    raw_content: str
    start_line: int
    end_line: int
    rrf_score: float
    dense_score: Optional[float] = None
    dense_rank: Optional[int] = None
    sparse_score: Optional[float] = None
    sparse_rank: Optional[int] = None

    def to_dict(self) -> Dict:
        return asdict(self)


class MarkdownHybridSearchEngine:
    """
    Orchestrates hierarchical chunking, local dense vector indexing,
    BM25 sparse indexing, and Reciprocal Rank Fusion retrieval.
    """

    DEFAULT_INDEX_DIR = "literature/search_index"

    def __init__(
        self,
        index_dir: str = DEFAULT_INDEX_DIR,
        device: Optional[str] = None,
        lazy_load_dense: bool = False,
    ):
        self.index_dir = index_dir
        self.db_path = os.path.join(index_dir, "index.db")
        self.bm25_path = os.path.join(index_dir, "bm25_index.json")

        self.chunker = HierarchicalMarkdownChunker()
        self.bm25 = BM25Index()
        self._dense_engine: Optional[DenseEmbeddingEngine] = None
        self._device = device

        if not lazy_load_dense:
            self._ensure_dense_engine()

        # Try loading index if it exists
        if os.path.exists(self.db_path) and os.path.exists(self.bm25_path):
            self.load_index()

    def _ensure_dense_engine(self) -> DenseEmbeddingEngine:
        if self._dense_engine is None:
            self._dense_engine = DenseEmbeddingEngine(device=self._device)
        return self._dense_engine

    def _init_db(self, conn: sqlite3.Connection):
        """Initializes SQLite database schema for document chunks."""
        with conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    doc_path TEXT PRIMARY KEY,
                    doc_title TEXT,
                    mtime REAL,
                    chunk_count INTEGER
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS chunks (
                    chunk_id TEXT PRIMARY KEY,
                    doc_path TEXT,
                    doc_title TEXT,
                    breadcrumb TEXT,
                    content TEXT,
                    raw_content TEXT,
                    start_line INTEGER,
                    end_line INTEGER
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_chunks_doc ON chunks(doc_path)")

    def index_corpus(
        self,
        base_dir: str = ".",
        subdirs: Optional[List[str]] = None,
        include_root_md: bool = True,
        batch_size: int = 32,
    ) -> int:
        """
        Scans, chunks, and indexes all Markdown files across target directories.
        """
        if subdirs is None:
            subdirs = ["proposals", "literature", "brainstorming", "docs"]

        all_md_files: List[str] = []
        for s in subdirs:
            pattern = os.path.join(base_dir, s, "**/*.md")
            all_md_files.extend(glob.glob(pattern, recursive=True))

        if include_root_md:
            root_pattern = os.path.join(base_dir, "*.md")
            all_md_files.extend(glob.glob(root_pattern))

        # Filter out git/venv paths
        filtered_files = []
        for f in sorted(set(all_md_files)):
            norm = os.path.normpath(f)
            if ".venv" in norm or ".git" in norm or ".system_generated" in norm:
                continue
            filtered_files.append(norm)

        print(f"[*] Ditemukan {len(filtered_files)} berkas Markdown untuk diindeks.")

        # 1. Chunk all files
        all_chunks: List[MarkdownChunk] = []
        doc_stats: List[Tuple[str, str, float, int]] = []

        for fpath in filtered_files:
            rel_path = os.path.relpath(fpath, base_dir)
            chunks = self.chunker.chunk_file(fpath, base_dir=base_dir)
            if chunks:
                all_chunks.extend(chunks)
                doc_stats.append((
                    rel_path,
                    chunks[0].doc_title,
                    os.path.getmtime(fpath),
                    len(chunks),
                ))

        print(f"[+] Total {len(all_chunks)} potongan teks (chunks) berhasil dibuat.")

        # 2. Build Sparse BM25 Index
        print("[*] Membangun indeks BM25...")
        bm25_docs = [(c.chunk_id, c.content) for c in all_chunks]
        self.bm25.index_documents(bm25_docs)

        # 3. Build Dense Embeddings
        print(f"[*] Menghasilkan vektor semantik ({self._ensure_dense_engine().device})...")
        chunk_texts = [c.content for c in all_chunks]
        chunk_ids = [c.chunk_id for c in all_chunks]
        embeddings = self._dense_engine.encode(chunk_texts, batch_size=batch_size, show_progress=True)
        self._dense_engine.set_corpus_embeddings(chunk_ids, embeddings)

        # 4. Save to Disk & SQLite
        os.makedirs(self.index_dir, exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        self._init_db(conn)

        with conn:
            conn.execute("DELETE FROM documents")
            conn.execute("DELETE FROM chunks")

            conn.executemany(
                "INSERT INTO documents VALUES (?, ?, ?, ?)",
                doc_stats,
            )

            chunk_records = [
                (
                    c.chunk_id,
                    c.doc_path,
                    c.doc_title,
                    c.breadcrumb,
                    c.content,
                    c.raw_content,
                    c.start_line,
                    c.end_line,
                )
                for c in all_chunks
            ]
            conn.executemany(
                "INSERT INTO chunks VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                chunk_records,
            )
        conn.close()

        # Save BM25 state
        self.bm25.save(self.bm25_path)

        # Save Dense embeddings
        self._dense_engine.save(self.index_dir)

        print(f"[+] Indeks hybrid berhasil disimpan ke direktori: {self.index_dir}")
        return len(all_chunks)

    def load_index(self) -> bool:
        """Loads index metadata, BM25 index, and dense vectors from disk."""
        if not os.path.exists(self.db_path) or not os.path.exists(self.bm25_path):
            return False

        try:
            self.bm25.load(self.bm25_path)
            self._ensure_dense_engine().load(self.index_dir)
            return True
        except Exception as e:
            print(f"[!] Gagal memuat indeks: {e}")
            return False

    def get_stats(self) -> Dict:
        """Returns statistics regarding indexed documents and chunks."""
        if not os.path.exists(self.db_path):
            return {"status": "unindexed"}

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM documents")
        total_docs = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM chunks")
        total_chunks = cursor.fetchone()[0]
        conn.close()

        has_dense = self._dense_engine is not None and self._dense_engine.embeddings is not None

        return {
            "status": "ready",
            "index_dir": self.index_dir,
            "total_documents": total_docs,
            "total_chunks": total_chunks,
            "bm25_terms_count": len(self.bm25.inverted_index),
            "dense_embeddings_shape": self._dense_engine.embeddings.shape if has_dense else None,
            "dense_device": self._dense_engine.device if self._dense_engine else "none",
        }

    def search(
        self,
        query: str,
        top_k: int = 5,
        mode: str = "hybrid",
        filter_dir: Optional[str] = None,
        rrf_k: int = 60,
        dense_weight: float = 0.5,
        sparse_weight: float = 0.5,
    ) -> List[SearchResult]:
        """
        Executes hybrid, dense-only, or sparse-only retrieval.
        Returns: Ranked list of SearchResult objects.
        """
        if not os.path.exists(self.db_path):
            print("[-] Indeks belum dibuat. Jalankan index_corpus() terlebih dahulu.")
            return []

        # Connect to SQLite for chunk metadata
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        candidates_k = max(top_k * 5, 40)

        # 1. Sparse Search
        sparse_results: Dict[str, Tuple[float, int]] = {}
        if mode in ["hybrid", "sparse"]:
            s_raw = self.bm25.search(query, top_k=candidates_k)
            for doc_id, score, rank in s_raw:
                sparse_results[doc_id] = (score, rank)

        # 2. Dense Search
        dense_results: Dict[str, Tuple[float, int]] = {}
        if mode in ["hybrid", "dense"]:
            self._ensure_dense_engine()
            d_raw = self._dense_engine.search(query, top_k=candidates_k)
            for doc_id, score, rank in d_raw:
                dense_results[doc_id] = (score, rank)

        # 3. Fusion & Ranking
        scored_chunk_ids: List[Tuple[str, float]] = []

        if mode == "sparse":
            for cid, (score, rank) in sparse_results.items():
                scored_chunk_ids.append((cid, score))
            scored_chunk_ids.sort(key=lambda x: x[1], reverse=True)

        elif mode == "dense":
            for cid, (score, rank) in dense_results.items():
                scored_chunk_ids.append((cid, score))
            scored_chunk_ids.sort(key=lambda x: x[1], reverse=True)

        else:  # hybrid RRF
            all_ids = set(sparse_results.keys()).union(dense_results.keys())
            for cid in all_ids:
                d_rank = dense_results.get(cid, (0.0, 9999))[1]
                s_rank = sparse_results.get(cid, (0.0, 9999))[1]

                rrf_score = 0.0
                if cid in dense_results:
                    rrf_score += dense_weight / (rrf_k + d_rank)
                if cid in sparse_results:
                    rrf_score += sparse_weight / (rrf_k + s_rank)

                scored_chunk_ids.append((cid, rrf_score))

            scored_chunk_ids.sort(key=lambda x: x[1], reverse=True)

        # 4. Fetch Full Chunk Metadata & Apply Optional Filtering
        final_results: List[SearchResult] = []

        for cid, main_score in scored_chunk_ids:
            cursor.execute(
                "SELECT doc_path, doc_title, breadcrumb, content, raw_content, start_line, end_line FROM chunks WHERE chunk_id = ?",
                (cid,),
            )
            row = cursor.fetchone()
            if not row:
                continue

            doc_path, doc_title, breadcrumb, content, raw_content, start_line, end_line = row

            # Apply directory filter if specified
            if filter_dir and not doc_path.startswith(filter_dir):
                continue

            d_info = dense_results.get(cid)
            s_info = sparse_results.get(cid)

            res = SearchResult(
                chunk_id=cid,
                doc_path=doc_path,
                doc_title=doc_title,
                breadcrumb=breadcrumb,
                content=content,
                raw_content=raw_content,
                start_line=start_line,
                end_line=end_line,
                rrf_score=main_score,
                dense_score=d_info[0] if d_info else None,
                dense_rank=d_info[1] if d_info else None,
                sparse_score=s_info[0] if s_info else None,
                sparse_rank=s_info[1] if s_info else None,
            )
            final_results.append(res)

            if len(final_results) >= top_k:
                break

        conn.close()
        return final_results
