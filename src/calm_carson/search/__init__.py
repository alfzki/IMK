"""
calm_carson.search
Hybrid Retrieval Package combining dense semantic vector search and sparse BM25
for Markdown document corpora.
"""

from calm_carson.search.bm25 import BM25Index, tokenize_technical_text
from calm_carson.search.chunker import HierarchicalMarkdownChunker, MarkdownChunk
from calm_carson.search.dense import DenseEmbeddingEngine
from calm_carson.search.hybrid import MarkdownHybridSearchEngine, SearchResult

__all__ = [
    "HierarchicalMarkdownChunker",
    "MarkdownChunk",
    "BM25Index",
    "tokenize_technical_text",
    "DenseEmbeddingEngine",
    "MarkdownHybridSearchEngine",
    "SearchResult",
]
