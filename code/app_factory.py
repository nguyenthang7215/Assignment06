from __future__ import annotations

from pathlib import Path
import os

from application.image_service import ImageService
from application.query_service import QueryService
from application.ranking_service import RankingService
from application.order_service import OrderService
from presentation.search_ui import SearchUI
from application.search_service import SearchService
from application.speech_service import SpeechService
from data_access.order_repository import OrderRepository
from data_access.product_repository import ProductRepository
from data_access.vector_index import VectorIndex
from data_access.sqlite_vector_index import SQLiteVectorIndex


BASE_DIR = Path(__file__).resolve().parent
DATASET_DIR = BASE_DIR / "dataset"


def create_application() -> SearchUI:
    product_repository = ProductRepository(DATASET_DIR / "products.json")
    order_repository = OrderRepository(DATASET_DIR / "orders.json")
    image_service = ImageService(os.environ.get("SEARCH_IMAGE_ENCODER", "color"))
    vectors = {
        product.id: image_service.encode(DATASET_DIR / "images" / product.image)
        for product in product_repository.all_products()
    }
    vector_index = (SQLiteVectorIndex(DATASET_DIR / "vectors.sqlite", vectors)
                    if os.environ.get("SEARCH_VECTOR_BACKEND") == "sqlite" else VectorIndex(vectors))
    semantic_index = None
    if os.environ.get("SEARCH_TEXT_MODE") == "semantic":
        from application.semantic_text_index import SemanticTextIndex
        semantic_index = SemanticTextIndex(product_repository.all_products())
    search_service = SearchService(product_repository, vector_index,
                                   RankingService(), semantic_index)
    return SearchUI(
        query_service=QueryService(),
        speech_service=SpeechService(),
        search_service=search_service,
        order_service=OrderService(order_repository),
        image_service=image_service,
    )
