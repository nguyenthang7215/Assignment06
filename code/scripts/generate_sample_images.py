from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "dataset" / "images"

PRODUCTS = {
    "nike_black_running_shoes.png": ("shoe", "black", "white"),
    "adidas_white_running_shoes.png": ("shoe", "white", "gray"),
    "black_leather_bag.png": ("bag", "black", "gray"),
    "blue_sports_shoes.png": ("shoe", "royalblue", "white"),
    "red_casual_shoes.png": ("shoe", "crimson", "white"),
    "brown_travel_bag.png": ("bag", "saddlebrown", "burlywood"),
    "black_wireless_headphones.png": ("headphones", "black", "gray"),
    "white_wireless_headphones.png": ("headphones", "white", "lightgray"),
    "black_smart_watch.png": ("watch", "black", "deepskyblue"),
    "green_sports_watch.png": ("watch", "seagreen", "limegreen"),
}


def draw_product(kind: str, primary: str, accent: str) -> Image.Image:
    image = Image.new("RGB", (320, 240), "#f2f4f7")
    draw = ImageDraw.Draw(image)
    if kind == "shoe":
        draw.polygon([(45, 135), (120, 82), (175, 125), (270, 145), (285, 185), (55, 185)], fill=primary, outline="#222222", width=4)
        draw.polygon([(55, 185), (285, 185), (270, 205), (70, 205)], fill=accent, outline="#222222", width=3)
        draw.line([(125, 115), (190, 145)], fill=accent, width=7)
        draw.line([(140, 105), (205, 140)], fill=accent, width=7)
    elif kind == "bag":
        draw.rounded_rectangle((65, 75, 255, 200), radius=18, fill=primary, outline="#222222", width=5)
        draw.arc((105, 35, 215, 125), 180, 360, fill=accent, width=10)
        draw.rectangle((150, 125, 175, 150), fill=accent)
    elif kind == "headphones":
        draw.arc((75, 35, 245, 190), 180, 360, fill=primary, width=25)
        draw.rounded_rectangle((55, 120, 105, 205), radius=18, fill=primary, outline="#222222", width=4)
        draw.rounded_rectangle((215, 120, 265, 205), radius=18, fill=primary, outline="#222222", width=4)
        draw.rectangle((93, 145, 108, 180), fill=accent)
        draw.rectangle((212, 145, 227, 180), fill=accent)
    else:
        draw.rounded_rectangle((128, 25, 192, 215), radius=18, fill=primary)
        draw.rounded_rectangle((95, 70, 225, 175), radius=28, fill="#222222", outline=primary, width=8)
        draw.ellipse((130, 100, 190, 160), fill=accent)
    return image


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for filename, (kind, primary, accent) in PRODUCTS.items():
        draw_product(kind, primary, accent).save(OUTPUT / filename)
    print(f"Generated {len(PRODUCTS)} sample images in dataset/images")


if __name__ == "__main__":
    main()

