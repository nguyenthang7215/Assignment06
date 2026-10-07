from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Literal


QueryType = Literal["text", "voice", "image", "multimodal", "order"]


@dataclass(frozen=True)
class Product:
    id: int
    name: str
    category: str
    color: str
    price: float
    stock: int
    description: str
    image: str
    popularity: float = 0.0

    def searchable_text(self) -> str:
        return " ".join(
            (self.name, self.category, self.color, self.description)
        ).lower()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Order:
    order_id: str
    customer_id: str
    date: str
    status: str
    total: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class QueryRepresentation:
    type: QueryType
    raw_input: str
    normalized_text: str = ""
    image_path: Path | None = None
    filters: dict[str, Any] = field(default_factory=dict)
    image_vector: Any = None


@dataclass(frozen=True)
class Candidate:
    product: Product
    text_score: float = 0.0
    image_score: float = 0.0


@dataclass(frozen=True)
class RankedResult:
    product: Product
    score: float
    text_score: float
    image_score: float
    business_score: float
    reason: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "product": self.product.to_dict(),
            "score": round(self.score, 4),
            "text_score": round(self.text_score, 4),
            "image_score": round(self.image_score, 4),
            "business_score": round(self.business_score, 4),
            "reason": self.reason,
        }

