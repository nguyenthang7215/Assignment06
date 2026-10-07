from __future__ import annotations

import json
from pathlib import Path

from domain.models import Order


class OrderRepository:
    def __init__(self, dataset_path: Path) -> None:
        self.dataset_path = Path(dataset_path)
        with self.dataset_path.open(encoding="utf-8") as stream:
            self._orders = [Order(**record) for record in json.load(stream)]

    def find_order(self, order_id: str) -> Order | None:
        wanted = order_id.strip().upper()
        return next((o for o in self._orders if o.order_id.upper() == wanted), None)

    def latest_for_customer(self, customer_id: str) -> Order | None:
        orders = [o for o in self._orders if o.customer_id == customer_id]
        return max(orders, key=lambda order: order.date, default=None)

