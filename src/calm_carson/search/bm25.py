"""
calm_carson.search.bm25
Sparse BM25Okapi search engine tuned for scientific and technical terminology
across Indonesian and English statistical computing documents.
"""

import json
import math
import os
import re
from collections import Counter, defaultdict
from typing import Dict, List, Optional, Set, Tuple


INDONESIAN_STOPWORDS: Set[str] = {
    "dan", "di", "ke", "dari", "yang", "ini", "itu", "untuk", "pada", "adalah",
    "dengan", "sebagai", "dalam", "oleh", "akan", "bisa", "dapat", "juga",
    "karena", "maka", "atau", "tentang", "serta", "bagi", "sampai", "antara",
    "namun", "tetapi", "secara", "terhadap", "setelah", "sebelum", "ketika",
    "saat", "apakah", "yaitu", "yakni", "selain", "melalui", "agar", "supaya",
    "masih", "sudah", "telah", "sedang", "hanya", "para", "suatu", "setiap"
}

ENGLISH_STOPWORDS: Set[str] = {
    "a", "an", "the", "and", "or", "but", "if", "while", "of", "at", "by",
    "for", "with", "about", "against", "between", "into", "through", "during",
    "before", "after", "above", "below", "to", "from", "up", "down", "in",
    "out", "on", "off", "over", "under", "again", "further", "then", "once",
    "here", "there", "when", "where", "why", "how", "all", "any", "both",
    "each", "few", "more", "most", "other", "some", "such", "no", "nor",
    "not", "only", "own", "same", "so", "than", "too", "very", "s", "t",
    "can", "will", "just", "don", "should", "now"
}

STOPWORDS = INDONESIAN_STOPWORDS.union(ENGLISH_STOPWORDS)


def tokenize_technical_text(text: str, remove_stopwords: bool = True) -> List[str]:
    """
    Tokenizes technical text preserving compound words, acronyms, hyphenated terms,
    and camelCase / snake_case identifiers.
    """
    if not text:
        return []

    # 1. Normalize markdown links and formatting characters
    cleaned = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
    cleaned = re.sub(r"[*_`#~|]", " ", cleaned)

    # 2. Extract technical patterns (e.g. 'iso-25010', 'sha-256', 'vapt', 'sipadu-ng')
    # Matches words with hyphens, underscores, or digits
    raw_tokens = re.findall(r"\b[a-zA-Z0-9]+(?:[-_][a-zA-Z0-9]+)*\b", cleaned)

    tokens = []
    for token in raw_tokens:
        lower = token.lower()
        if len(lower) < 2:
            continue

        if remove_stopwords and lower in STOPWORDS:
            continue

        tokens.append(lower)

        # If token has hyphen or underscore, also add constituent words
        if "-" in lower or "_" in lower:
            parts = re.split(r"[-_]", lower)
            for p in parts:
                if len(p) >= 2 and (not remove_stopwords or p not in STOPWORDS):
                    tokens.append(p)

        # If camelCase (e.g. trasgoDP, openDP, microData), split and add
        camel_parts = re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?=[A-Z][a-z]|\d|\W|$)|\d+", token)
        if len(camel_parts) > 1:
            for cp in camel_parts:
                cpl = cp.lower()
                if len(cpl) >= 2 and (not remove_stopwords or cpl not in STOPWORDS):
                    tokens.append(cpl)

    return tokens


class BM25Index:
    """
    BM25Okapi Information Retrieval Index.
    """

    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.doc_ids: List[str] = []
        self.doc_lengths: Dict[str, int] = {}
        self.avg_doc_len: float = 0.0
        self.corpus_size: int = 0
        # term -> {doc_id: term_frequency}
        self.inverted_index: Dict[str, Dict[str, int]] = defaultdict(dict)
        # term -> idf
        self.idf_cache: Dict[str, float] = {}

    def index_documents(self, documents: List[Tuple[str, str]]):
        """
        Indexes a list of (doc_id, text) tuples.
        """
        self.doc_ids = []
        self.doc_lengths = {}
        self.inverted_index = defaultdict(dict)
        self.idf_cache = {}

        total_length = 0
        for doc_id, text in documents:
            tokens = tokenize_technical_text(text)
            doc_len = len(tokens)
            self.doc_ids.append(doc_id)
            self.doc_lengths[doc_id] = doc_len
            total_length += doc_len

            counts = Counter(tokens)
            for term, count in counts.items():
                self.inverted_index[term][doc_id] = count

        self.corpus_size = len(self.doc_ids)
        self.avg_doc_len = total_length / self.corpus_size if self.corpus_size > 0 else 0.0

        # Precompute IDF for all indexed terms
        for term, postings in self.inverted_index.items():
            doc_freq = len(postings)
            # Standard Lucene/BM25Okapi IDF with smoothing
            self.idf_cache[term] = math.log(1.0 + (self.corpus_size - doc_freq + 0.5) / (doc_freq + 0.5))

    def search(self, query: str, top_k: int = 10) -> List[Tuple[str, float, int]]:
        """
        Searches the index with a query string.
        Returns: List of (doc_id, bm25_score, rank_1_indexed)
        """
        query_tokens = tokenize_technical_text(query)
        if not query_tokens or self.corpus_size == 0:
            return []

        scores: Dict[str, float] = defaultdict(float)

        for term in query_tokens:
            if term not in self.inverted_index:
                continue

            idf = self.idf_cache.get(term, 0.0)
            postings = self.inverted_index[term]

            for doc_id, tf in postings.items():
                doc_len = self.doc_lengths.get(doc_id, self.avg_doc_len)
                denom = tf + self.k1 * (1.0 - self.b + self.b * (doc_len / (self.avg_doc_len or 1.0)))
                num = tf * (self.k1 + 1.0)
                scores[doc_id] += idf * (num / denom if denom > 0 else 0.0)

        sorted_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [(doc_id, score, rank) for rank, (doc_id, score) in enumerate(sorted_results[:top_k], start=1)]

    def save(self, filepath: str):
        """Serializes the index state to JSON."""
        state = {
            "k1": self.k1,
            "b": self.b,
            "corpus_size": self.corpus_size,
            "avg_doc_len": self.avg_doc_len,
            "doc_ids": self.doc_ids,
            "doc_lengths": self.doc_lengths,
            "inverted_index": {t: dict(p) for t, p in self.inverted_index.items()},
            "idf_cache": self.idf_cache,
        }
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False)

    def load(self, filepath: str):
        """Loads index state from JSON."""
        with open(filepath, "r", encoding="utf-8") as f:
            state = json.load(f)
        self.k1 = state["k1"]
        self.b = state["b"]
        self.corpus_size = state["corpus_size"]
        self.avg_doc_len = state["avg_doc_len"]
        self.doc_ids = state["doc_ids"]
        self.doc_lengths = state["doc_lengths"]
        self.inverted_index = {t: dict(p) for t, p in state["inverted_index"].items()}
        self.idf_cache = state["idf_cache"]
