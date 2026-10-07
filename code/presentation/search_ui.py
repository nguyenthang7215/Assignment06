from __future__ import annotations

from domain.models import Order, RankedResult
from pathlib import Path
from dataclasses import replace
from application.image_service import ImageService
from presentation.voice_input import VoiceInput
from presentation.image_upload import ImageUpload
from presentation.search_result_view import SearchResultView
from application.query_service import QueryService
from application.speech_service import SpeechService
from application.search_service import SearchService
from application.order_service import OrderService


class SearchUI:
    """Presentation controller using services without accessing repositories."""

    def __init__(self, query_service: QueryService, speech_service: SpeechService,
                 search_service: SearchService,
                 order_service: OrderService, image_service: ImageService) -> None:
        self.query_service = query_service
        self.speech_service = speech_service
        self.search_service = search_service
        self.order_service = order_service
        self.image_service = image_service
        self.voice_input = VoiceInput()
        self.image_upload = ImageUpload()
        self.result_view = SearchResultView()

    def search_text(self, text: str, top_k: int = 5) -> list[RankedResult]:
        return self.search_service.search(self.query_service.text_query(text), top_k)

    def search_voice(self, transcript: str, top_k: int = 5) -> list[RankedResult]:
        text = self.speech_service.transcribe(self.voice_input.collect(transcript))
        return self.search_service.search(self.query_service.voice_query(text), top_k)

    def search_image(self, image_path: Path, top_k: int = 5) -> list[RankedResult]:
        image_path = self.image_upload.collect(image_path)
        vector = self.image_service.encode(image_path)
        query = replace(self.query_service.image_query(image_path), image_vector=vector)
        return self.search_service.search(query, top_k)

    def search_multimodal(self, text: str, image_path: Path,
                          top_k: int = 5) -> list[RankedResult]:
        image_path = self.image_upload.collect(image_path)
        vector = self.image_service.encode(image_path)
        query = replace(self.query_service.multimodal_query(text, image_path),
                        image_vector=vector)
        return self.search_service.search(query, top_k)

    def search_order(self, text: str, customer_id: str = "C001") -> Order | None:
        return self.order_service.search_order(text, customer_id)

    def render_results(self, title: str, query: str, results: list[RankedResult]) -> None:
        self.result_view.render_results(title, query, results)

    def render_order(self, order: Order | None) -> None:
        self.result_view.render_order(order)

