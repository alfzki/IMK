"""
calm_carson.search.dense
Dense semantic embedding engine using Transformers and PyTorch with CUDA acceleration.
Provides mean-pooled, L2-normalized 384-dimensional dense vectors.
"""

import json
import os
from typing import List, Optional, Tuple

import numpy as np
import torch
from transformers import AutoModel, AutoTokenizer


def mean_pooling(model_output, attention_mask: torch.Tensor) -> torch.Tensor:
    """Computes attention-weighted mean pooling across token representations."""
    token_embeddings = model_output[0]
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
    sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    return sum_embeddings / sum_mask


class DenseEmbeddingEngine:
    """
    Computes and searches dense semantic embeddings using multilingual MiniLM.
    Automatically accelerates with NVIDIA CUDA GPU when available.
    """

    DEFAULT_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

    def __init__(self, model_name: str = DEFAULT_MODEL, device: Optional[str] = None):
        self.model_name = model_name

        if device:
            self.device = device
        else:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

        if self.device == "cuda":
            self.model = self.model.half().to("cuda")
        else:
            self.model = self.model.to("cpu")

        self.model.eval()

        self.doc_ids: List[str] = []
        self.embeddings: Optional[np.ndarray] = None  # Shape: (N, 384)

    def encode(self, texts: List[str], batch_size: int = 32, show_progress: bool = False) -> np.ndarray:
        """Encodes a list of text strings into normalized numpy vectors."""
        if not texts:
            return np.empty((0, 384), dtype=np.float32)

        all_embeddings = []
        iterator = range(0, len(texts), batch_size)
        if show_progress:
            from tqdm import tqdm
            iterator = tqdm(iterator, desc="Generating Dense Embeddings")

        for start_idx in iterator:
            batch_texts = texts[start_idx : start_idx + batch_size]
            encoded_input = self.tokenizer(
                batch_texts,
                padding=True,
                truncation=True,
                max_length=512,
                return_tensors="pt",
            ).to(self.device)

            with torch.no_grad():
                model_output = self.model(**encoded_input)
                pooled = mean_pooling(model_output, encoded_input["attention_mask"])
                normalized = torch.nn.functional.normalize(pooled, p=2, dim=1)

            all_embeddings.append(normalized.cpu().to(torch.float32).numpy())

        return np.vstack(all_embeddings)

    def encode_query(self, query: str) -> np.ndarray:
        """Encodes a single query string into a 1D vector of shape (384,)."""
        return self.encode([query])[0]

    def set_corpus_embeddings(self, doc_ids: List[str], embeddings: np.ndarray):
        """Sets the active corpus vectors in memory."""
        self.doc_ids = list(doc_ids)
        self.embeddings = embeddings.astype(np.float32)

    def search(self, query: str, top_k: int = 10) -> List[Tuple[str, float, int]]:
        """
        Calculates cosine similarity of query against indexed corpus.
        Returns: List of (doc_id, cosine_score, rank_1_indexed)
        """
        if self.embeddings is None or len(self.doc_ids) == 0:
            return []

        q_vec = self.encode_query(query)  # Shape: (384,)
        # Since embeddings and q_vec are L2-normalized, cosine similarity = dot product
        scores = np.dot(self.embeddings, q_vec)  # Shape: (N,)

        top_indices = np.argsort(-scores)[:top_k]
        results = []
        for rank, idx in enumerate(top_indices, start=1):
            results.append((self.doc_ids[idx], float(scores[idx]), rank))

        return results

    def save(self, output_dir: str):
        """Saves embeddings array and ID mapping."""
        os.makedirs(output_dir, exist_ok=True)
        if self.embeddings is not None:
            npy_path = os.path.join(output_dir, "embeddings.npy")
            np.save(npy_path, self.embeddings)

        ids_path = os.path.join(output_dir, "doc_ids.json")
        with open(ids_path, "w", encoding="utf-8") as f:
            json.dump(self.doc_ids, f, ensure_ascii=False)

    def load(self, output_dir: str) -> bool:
        """Loads embeddings array and ID mapping from disk."""
        npy_path = os.path.join(output_dir, "embeddings.npy")
        ids_path = os.path.join(output_dir, "doc_ids.json")

        if os.path.exists(npy_path) and os.path.exists(ids_path):
            self.embeddings = np.load(npy_path).astype(np.float32)
            with open(ids_path, "r", encoding="utf-8") as f:
                self.doc_ids = json.load(f)
            return True
        return False
