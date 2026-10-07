from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from app_factory import BASE_DIR, create_application


@dataclass
class EvaluationRow:
    query: str
    mode: str
    expected_top1: str
    actual_top1: str
    success: bool


def evaluate() -> list[EvaluationRow]:
    app = create_application()
    images = BASE_DIR / "dataset" / "images"
    cases = [
        ("black running shoes", "Text", "Nike Black Running Shoes", lambda: app.search_text("black running shoes")),
        ("running shoes under 110 dollars", "Text", "Adidas White Running Shoes", lambda: app.search_text("running shoes under 110 dollars")),
        ("find blue sports shoes", "Voice", "Blue Sports Shoes", lambda: app.search_voice("find blue sports shoes")),
        ("find black headphones", "Voice", "Black Wireless Headphones", lambda: app.search_voice("find black headphones")),
        ("black_leather_bag.png", "Image", "Black Leather Bag", lambda: app.search_image(images / "black_leather_bag.png")),
        ("green_sports_watch.png", "Image", "Green Sports Watch", lambda: app.search_image(images / "green_sports_watch.png")),
        ("black shoes + sample image", "Multimodal", "Nike Black Running Shoes", lambda: app.search_multimodal("black shoes", images / "nike_black_running_shoes.png")),
        ("nike shoes under 100 dollars", "Text", "No result", lambda: app.search_text("nike shoes under 100 dollars")),
        ("black shoe", "Text", "Nike Black Running Shoes", lambda: app.search_text("black shoe")),
        ("order O001", "Order", "O001", lambda: [app.search_order("order O001")]),
    ]
    rows = []
    for query, mode, expected, search in cases:
        results = search()
        if mode == "Order":
            actual = results[0].order_id if results[0] else "No result"
        else:
            actual = results[0].product.name if results else "No result"
        rows.append(EvaluationRow(query, mode, expected, actual, actual == expected))
    return rows


def main() -> None:
    rows = evaluate()
    output_directory = BASE_DIR / "results"
    output_directory.mkdir(exist_ok=True)
    total = len(rows)
    successful = sum(row.success for row in rows)
    success_rate = successful / total if total else 0.0

    json_payload = {
        "total_queries": total,
        "successful_queries": successful,
        "success_rate": success_rate,
        "rows": [asdict(row) for row in rows],
    }
    (output_directory / "evaluation.json").write_text(
        json.dumps(json_payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    lines = [
        "# Experimental Evaluation",
        "",
        "| Query | Mode | Expected Top-1 | Actual Top-1 | Success |",
        "|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row.query} | {row.mode} | {row.expected_top1} | "
            f"{row.actual_top1} | {'Yes' if row.success else 'No'} |"
        )
    lines.extend(
        [
            "",
            f"- Total queries: **{total}**",
            f"- Successful queries: **{successful}**",
            f"- Success rate: **{success_rate:.2%}**",
            "- Incorrect examples: "
            + (
                "; ".join(
                    f"`{row.query}` returned `{row.actual_top1}`"
                    for row in rows
                    if not row.success
                )
                if successful < total
                else "**None in this controlled test set.**"
            ),
            "",
            "> This is a small, controlled prototype dataset. The result does not imply production-level accuracy.",
        ]
    )
    (output_directory / "evaluation.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Evaluation: {successful}/{total} successful ({success_rate:.2%})")


if __name__ == "__main__":
    main()
