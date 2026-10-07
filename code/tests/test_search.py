from __future__ import annotations

import unittest
from io import BytesIO

from web import app as web_app

from app_factory import BASE_DIR, create_application


class SearchPrototypeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.app = create_application()
        cls.images = BASE_DIR / "dataset" / "images"

    def test_text_search_returns_black_running_shoes(self) -> None:
        results = self.app.search_text("black running shoes")
        self.assertTrue(results)
        self.assertEqual(1, results[0].product.id)

    def test_price_filter_is_applied(self) -> None:
        results = self.app.search_text("running shoes under 110 dollars")
        self.assertTrue(results)
        self.assertTrue(all(result.product.price <= 110 for result in results))
        self.assertEqual(2, results[0].product.id)

    def test_voice_search_uses_text_pipeline(self) -> None:
        results = self.app.search_voice("find blue sports shoes")
        self.assertEqual(4, results[0].product.id)

    def test_image_search_returns_identical_product(self) -> None:
        image = self.images / "black_leather_bag.png"
        results = self.app.search_image(image)
        self.assertEqual(3, results[0].product.id)

    def test_multimodal_search(self) -> None:
        image = self.images / "nike_black_running_shoes.png"
        results = self.app.search_multimodal("black shoes", image)
        self.assertEqual(1, results[0].product.id)

    def test_order_search(self) -> None:
        order = self.app.search_order("find my order O001")
        self.assertIsNotNone(order)
        self.assertEqual("Shipped", order.status)

    def test_latest_order(self) -> None:
        order = self.app.search_order("where is my latest order?", "C001")
        self.assertIsNotNone(order)
        self.assertEqual("O003", order.order_id)

    def test_brand_and_price_constraints_do_not_return_competitors(self) -> None:
        self.assertEqual([], self.app.search_text("nike shoes under 100 dollars"))

    def test_category_and_color_constraints(self) -> None:
        results = self.app.search_text("black shoe")
        self.assertEqual([1], [result.product.id for result in results])

    def test_filter_only_query(self) -> None:
        results = self.app.search_text("under 110 dollars")
        self.assertTrue(results)
        self.assertTrue(all(result.product.price <= 110 for result in results))

    def test_empty_text_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "cannot be empty"):
            self.app.search_text("   ")

    def test_web_search_modes(self) -> None:
        client = web_app.test_client()
        self.assertEqual(200, client.get("/").status_code)
        response = client.post("/search", data={"mode": "text", "query": "black running shoes"})
        self.assertIn(b"Nike Black Running Shoes", response.data)
        response = client.post("/search", data={"mode": "voice", "query": "find blue sports shoes"})
        self.assertIn(b"Blue Sports Shoes", response.data)
        response = client.post("/search", data={"mode": "order", "query": "O001"})
        self.assertIn(b"Shipped", response.data)

    def test_web_image_upload(self) -> None:
        client = web_app.test_client()
        image = (self.images / "black_leather_bag.png").read_bytes()
        response = client.post("/search", data={"mode": "image", "image": (BytesIO(image), "bag.png")})
        self.assertEqual(200, response.status_code)
        self.assertIn(b"Black Leather Bag", response.data)


if __name__ == "__main__":
    unittest.main()
