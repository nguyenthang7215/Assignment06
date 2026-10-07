"""Small-corpus latent semantic embeddings for optional semantic retrieval."""
from __future__ import annotations

import numpy as np
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize

from domain.models import Product


class SemanticTextIndex:
    def __init__(self, products: list[Product]) -> None:
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
        matrix = self.vectorizer.fit_transform(product.searchable_text() for product in products)
        dimensions = min(8, min(matrix.shape) - 1)
        self.reducer = TruncatedSVD(n_components=dimensions, random_state=42)
        vectors = normalize(self.reducer.fit_transform(matrix))
        self.vectors = {product.id: vector for product, vector in zip(products, vectors)}

    def search(self, text: str) -> dict[int, float]:
        query = self.vectorizer.transform([text])
        if query.nnz == 0:
            return {}
        vector = normalize(self.reducer.transform(query))[0]
        return {product_id: max(0.0, float(np.dot(vector, product_vector))) for product_id, product_vector in self.vectors.items()}
