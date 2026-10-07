from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from app_factory import BASE_DIR, create_application
from presentation.search_ui import SearchUI


if hasattr(sys.stdout, "reconfigure"):
    # Windows may otherwise use a legacy code page and fail on Vietnamese paths.
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def run_demo() -> None:
    app = create_application()
    ui = app
    sample_image = BASE_DIR / "dataset" / "images" / "nike_black_running_shoes.png"

    ui.render_results(
        "Text Search",
        "black running shoes",
        app.search_text("black running shoes"),
    )
    ui.render_results(
        "Voice Search (simulated speech-to-text)",
        "find running shoes under 110 dollars",
        app.search_voice("find running shoes under 110 dollars"),
    )
    ui.render_results(
        "Image Search",
        str(sample_image),
        app.search_image(sample_image),
    )
    ui.render_results(
        "Multimodal Search",
        f"black shoes + {sample_image.name}",
        app.search_multimodal("black shoes", sample_image),
    )
    ui.render_order(app.search_order("find my order O001"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Multimodal e-commerce search prototype")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("demo", help="run all demonstration modes")

    text_parser = subparsers.add_parser("text")
    text_parser.add_argument("query")
    voice_parser = subparsers.add_parser("voice")
    voice_parser.add_argument("transcript")
    image_parser = subparsers.add_parser("image")
    image_parser.add_argument("path", type=Path)
    multi_parser = subparsers.add_parser("multimodal")
    multi_parser.add_argument("query")
    multi_parser.add_argument("path", type=Path)
    order_parser = subparsers.add_parser("order")
    order_parser.add_argument("query")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.command in (None, "demo"):
        run_demo()
        return

    app = create_application()
    ui = app
    if args.command == "text":
        ui.render_results("Text Search", args.query, app.search_text(args.query))
    elif args.command == "voice":
        ui.render_results("Voice Search", args.transcript, app.search_voice(args.transcript))
    elif args.command == "image":
        ui.render_results("Image Search", str(args.path), app.search_image(args.path))
    elif args.command == "multimodal":
        ui.render_results(
            "Multimodal Search",
            f"{args.query} + {args.path}",
            app.search_multimodal(args.query, args.path),
        )
    elif args.command == "order":
        ui.render_order(app.search_order(args.query))


if __name__ == "__main__":
    main()

