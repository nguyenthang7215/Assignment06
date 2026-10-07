"""Persistent SQLite vector store with exact cosine search for small catalogs."""
from __future__ import annotations

import sqlite3
from pathlib import Path

import numpy as np

from data_access.vector_index import VectorIndex


class SQLiteVectorIndex(VectorIndex):
    def __init__(self, path: Path, vectors: dict[int, np.ndarray]) -> None:
        self.path = Path(path)
        with sqlite3.connect(self.path) as db:
            db.execute("CREATE TABLE IF NOT EXISTS product_vectors (product_id INTEGER PRIMARY KEY, dim INTEGER NOT NULL, vector BLOB NOT NULL)")
            db.executemany(
                "INSERT OR REPLACE INTO product_vectors VALUES (?, ?, ?)",
                ((product_id, len(vector), np.asarray(vector, dtype=np.float32).tobytes()) for product_id, vector in vectors.items()),
            )
            db.commit()

    def search(self, query_vector: np.ndarray) -> dict[int, float]:
        result = {}
        with sqlite3.connect(self.path) as db:
            for product_id, dim, blob in db.execute("SELECT product_id, dim, vector FROM product_vectors"):
                vector = np.frombuffer(blob, dtype=np.float32)
                if dim != len(query_vector):
                    continue
                result[product_id] = self.cosine_similarity(query_vector, vector)
        return result
