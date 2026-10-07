from __future__ import annotations

import re
import unicodedata
from pathlib import Path

from domain.models import QueryRepresentation


class QueryService:
    STOP_WORDS = {
        "a", "an", "the", "me", "my", "please", "show", "find", "search",
        "for", "product", "products", "dollar", "dollars", "usd",
    }
    KNOWN_COLORS = {"black", "white", "blue", "red", "brown", "gray", "green"}
    KNOWN_CATEGORIES = {"shoes", "bag", "headphones", "watch"}
    CATEGORY_ALIASES = {"shoe": "shoes", "bags": "bag", "headphone": "headphones", "watches": "watch"}
    KNOWN_BRANDS = {"nike", "adidas"}

    @staticmethod
    def _normalize(text: str) -> str:
        ascii_text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
        tokens = re.findall(r"[a-z0-9]+", ascii_text.lower())
        return " ".join(token for token in tokens if token not in QueryService.STOP_WORDS)

    def _filters(self, text: str) -> dict[str, object]:
        normalized = self._normalize(text)
        filters: dict[str, object] = {}
        price_match = re.search(r"(?:under|below|less than|max)\s*\$?\s*(\d+(?:\.\d+)?)", text.lower())
        if price_match:
            filters["max_price"] = float(price_match.group(1))
        for color in self.KNOWN_COLORS:
            if color in normalized.split():
                filters["color"] = color
                break
        for category in self.KNOWN_CATEGORIES:
            if category in normalized.split():
                filters["category"] = category
                break
        if "category" not in filters:
            for alias, category in self.CATEGORY_ALIASES.items():
                if alias in normalized.split():
                    filters["category"] = category
                    break
        for brand in self.KNOWN_BRANDS:
            if brand in normalized.split():
                filters["brand"] = brand
                break
        return filters

    @staticmethod
    def _search_terms(normalized: str, filters: dict[str, object]) -> str:
        tokens = normalized.split()
        ignored = {"under", "below", "less", "than", "max"}
        ignored.update(str(value) for key, value in filters.items() if key in {"color", "category", "brand"})
        ignored.update(QueryService.CATEGORY_ALIASES)
        if "max_price" in filters:
            ignored.add(str(int(filters["max_price"])))
        return " ".join(token for token in tokens if token not in ignored)

    def text_query(self, text: str) -> QueryRepresentation:
        if not text or not text.strip():
            raise ValueError("The text query cannot be empty.")
        normalized = self._normalize(text)
        filters = self._filters(text)
        return QueryRepresentation(
            type="text",
            raw_input=text,
            normalized_text=self._search_terms(normalized, filters),
            filters=filters,
        )

    def voice_query(self, transcript: str) -> QueryRepresentation:
        text_query = self.text_query(transcript)
        return QueryRepresentation(
            type="voice",
            raw_input=transcript,
            normalized_text=text_query.normalized_text,
            filters=text_query.filters,
        )

    def image_query(self, image_path: Path) -> QueryRepresentation:
        return QueryRepresentation(
            type="image", raw_input=str(image_path), image_path=Path(image_path)
        )

    def multimodal_query(self, text: str, image_path: Path) -> QueryRepresentation:
        text_query = self.text_query(text)
        return QueryRepresentation(
            type="multimodal",
            raw_input=f"text={text}; image={image_path}",
            normalized_text=text_query.normalized_text,
            image_path=Path(image_path),
            filters=text_query.filters,
        )
