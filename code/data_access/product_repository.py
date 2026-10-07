from __future__ import annotations

import json
from pathlib import Path

from domain.models import Product


class ProductRepository:
    """Loads and exposes product data without leaking storage details upward."""

    def __init__(self, dataset_path: Path) -> None:
        self.dataset_path = Path(dataset_path)
        self._products = self._load()

    def _load(self) -> list[Product]:
        with self.dataset_path.open(encoding="utf-8") as stream:
            records = json.load(stream)
        products = [Product(**record) for record in records]
        if len(products) < 10:
            raise ValueError("The assignment requires at least ten products.")
        return products

    def all_products(self) -> list[Product]:
        return list(self._products)

    def find_by_id(self, product_id: int) -> Product | None:
        return next((p for p in self._products if p.id == product_id), None)

