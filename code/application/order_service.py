import re

from data_access.order_repository import OrderRepository
from domain.models import Order


class OrderService:
    def __init__(self, repository: OrderRepository) -> None:
        self.repository = repository

    def search_order(self, text: str, customer_id: str = "C001") -> Order | None:
        match = re.search(r"\bO\d+\b", text.upper())
        if match:
            return self.repository.find_order(match.group())
        if "latest" in text.lower() or "newest" in text.lower():
            return self.repository.latest_for_customer(customer_id)
        return None
