"""Flask presentation layer for the Assignment 06 prototype."""
from __future__ import annotations

import os
import tempfile
from pathlib import Path

from flask import Flask, render_template, request, send_from_directory

from app_factory import DATASET_DIR, create_application


def create_web_app() -> Flask:
    web = Flask(__name__)
    web.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024
    search_ui = create_application()

    @web.get("/")
    def index():
        return render_template("index.html", mode="text", results=None, order=None)

    @web.get("/images/<path:name>")
    def product_image(name: str):
        return send_from_directory(DATASET_DIR / "images", name)

    @web.post("/search")
    def search():
        mode = request.form.get("mode", "text")
        query = request.form.get("query", "").strip()
        customer_id = request.form.get("customer_id", "C001").strip() or "C001"
        results = None
        order = None
        error = None
        image_name = None
        try:
            if mode == "text":
                results = search_ui.search_text(query)
            elif mode == "voice":
                results = search_ui.search_voice(query)
            elif mode == "order":
                if not query:
                    raise ValueError("Enter an order ID or request the latest order.")
                order = search_ui.search_order(query, customer_id)
            elif mode in ("image", "multimodal"):
                upload = request.files.get("image")
                if upload is None or not upload.filename:
                    raise ValueError("Choose a PNG or JPEG image.")
                suffix = Path(upload.filename).suffix.lower()
                if suffix not in {".png", ".jpg", ".jpeg", ".webp"}:
                    raise ValueError("Only PNG, JPEG and WebP images are supported.")
                image_name = Path(upload.filename).name
                with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as temp:
                    upload.save(temp)
                    temp_path = Path(temp.name)
                try:
                    if mode == "image":
                        results = search_ui.search_image(temp_path)
                    else:
                        results = search_ui.search_multimodal(query, temp_path)
                finally:
                    temp_path.unlink(missing_ok=True)
            else:
                raise ValueError("Unsupported search mode.")
        except (ValueError, OSError) as exc:
            error = str(exc)
        return render_template(
            "index.html", mode=mode, query=query, customer_id=customer_id,
            results=results, order=order, error=error, image_name=image_name,
            searched=True,
        )

    return web


app = create_web_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", "5000")), debug=False)
