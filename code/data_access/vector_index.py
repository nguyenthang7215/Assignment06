from __future__ import annotations

from pathlib import Path

import numpy as np

class VectorIndex:
    """In-memory vector index used by the image retrieval service."""

    def __init__(self, vectors: dict[int, np.ndarray]) -> None:
        self._vectors = dict(vectors)

    @staticmethod
    def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
        denominator = float(np.linalg.norm(a) * np.linalg.norm(b))
        if denominator == 0.0:
            return 0.0
        return float(np.dot(a, b) / denominator)

    def search(self, query_vector: np.ndarray) -> dict[int, float]:
        return {
            product_id: self.cosine_similarity(query_vector, vector)
            for product_id, vector in self._vectors.items()
        }

