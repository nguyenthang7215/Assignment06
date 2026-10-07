from __future__ import annotations

from application.ranking_service import RankingService
from data_access.product_repository import ProductRepository
from data_access.vector_index import VectorIndex
from domain.models import Candidate, QueryRepresentation


class SearchService:
    """Retrieve candidates, then delegate their ordering to RankingService."""

    def __init__(
        self,
        repository: ProductRepository,
        vector_index: VectorIndex,
        ranking_service: RankingService,
        semantic_index=None,
    ) -> None:
        self.repository = repository
        self.vector_index = vector_index
        self.ranking_service = ranking_service
        self.semantic_index = semantic_index

    def search(self, query: QueryRepresentation, top_k: int = 5):
        if query.type in ("text", "voice"):
            candidates = self.retrieve_text(query)
            weights = (1.0, 0.0)
        elif query.type == "image":
            candidates = self.retrieve_image(query)
            weights = (0.0, 1.0)
        elif query.type == "multimodal":
            candidates = self.retrieve_multimodal(query)
            weights = (0.5, 0.5)
        else:
            raise ValueError(f"Unsupported product query type: {query.type}")
        return self.ranking_service.rank(candidates, *weights, top_k)

    @staticmethod
    def _allowed(product, filters: dict[str, object]) -> bool:
        if "max_price" in filters and product.price > float(filters["max_price"]):
            return False
        if "color" in filters and product.color.lower() != filters["color"]:
            return False
        if "category" in filters and product.category.lower() != filters["category"]:
            return False
        if "brand" in filters and str(filters["brand"]) not in product.name.lower().split():
            return False
        return True

    def retrieve_text(self, query: QueryRepresentation) -> list[Candidate]:
        words = set(query.normalized_text.split())
        semantic_scores = self.semantic_index.search(query.normalized_text) if self.semantic_index and words else None
        candidates: list[Candidate] = []
        for product in self.repository.all_products():
            if not self._allowed(product, query.filters):
                continue
            searchable = product.searchable_text()
            matches = sum(1 for word in words if word in searchable)
            if semantic_scores is not None:
                score = semantic_scores.get(product.id, 0.0)
                allowed = score > 0.01
            else:
                score = matches / len(words) if words else 1.0
                allowed = not words or matches == len(words)
            if allowed:
                candidates.append(Candidate(product=product, text_score=score))
        return candidates

    def retrieve_image(self, query: QueryRepresentation) -> list[Candidate]:
        if query.image_vector is None:
            raise ValueError("An image query requires an encoded image vector.")
        similarities = self.vector_index.search(query.image_vector)
        return [
            Candidate(product=product, image_score=similarities[product.id])
            for product in self.repository.all_products()
            if self._allowed(product, query.filters)
        ]

    def retrieve_multimodal(self, query: QueryRepresentation) -> list[Candidate]:
        text_candidates = {c.product.id: c for c in self.retrieve_text(query)}
        image_candidates = {c.product.id: c for c in self.retrieve_image(query)}
        product_ids = set(text_candidates) | set(image_candidates)
        candidates: list[Candidate] = []
        for product_id in product_ids:
            text_candidate = text_candidates.get(product_id)
            image_candidate = image_candidates.get(product_id)
            product = (text_candidate or image_candidate).product  # type: ignore[union-attr]
            candidates.append(
                Candidate(
                    product=product,
                    text_score=text_candidate.text_score if text_candidate else 0.0,
                    image_score=image_candidate.image_score if image_candidate else 0.0,
                )
            )
        return candidates
