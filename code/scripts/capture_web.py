"""Capture reproducible web screenshots after starting `py web.py`."""
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT.parent / "screenshots"
OUT.mkdir(exist_ok=True)
CHROME = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(executable_path=str(CHROME), headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 1000}, device_scale_factor=1)
    page.goto("http://127.0.0.1:5000/", wait_until="networkidle")
    page.screenshot(path=str(OUT / "01-home.png"), full_page=True)

    page.locator("#query").fill("black running shoes")
    page.locator(".submit").click()
    page.locator(".product-card").first.wait_for()
    assert "Nike Black Running Shoes" in page.locator(".product-card").first.inner_text()
    page.screenshot(path=str(OUT / "02-text-results.png"), full_page=True)
    page.locator(".results").screenshot(path=str(OUT / "02-text-detail.png"))

    page.locator('[data-mode="voice"]').click()
    page.locator("#query").fill("find blue sports shoes")
    page.locator(".submit").click()
    assert "Blue Sports Shoes" in page.locator(".product-card").first.inner_text()
    page.screenshot(path=str(OUT / "03-voice-results.png"), full_page=True)
    page.locator(".results").screenshot(path=str(OUT / "03-voice-detail.png"))

    page.locator('[data-mode="image"]').click()
    page.locator("#image").set_input_files(str(ROOT / "dataset" / "images" / "black_leather_bag.png"))
    page.locator(".submit").click()
    assert "Black Leather Bag" in page.locator(".product-card").first.inner_text()
    page.screenshot(path=str(OUT / "04-image-results.png"), full_page=True)
    page.locator(".results").screenshot(path=str(OUT / "04-image-detail.png"))

    page.locator('[data-mode="multimodal"]').click()
    page.locator("#query").fill("black shoes")
    page.locator("#image").set_input_files(str(ROOT / "dataset" / "images" / "nike_black_running_shoes.png"))
    page.locator(".submit").click()
    assert "Nike Black Running Shoes" in page.locator(".product-card").first.inner_text()
    page.screenshot(path=str(OUT / "05-multimodal-results.png"), full_page=True)
    page.locator(".results").screenshot(path=str(OUT / "05-multimodal-detail.png"))

    page.locator('[data-mode="order"]').click()
    page.locator("#query").fill("find order O001")
    page.locator(".submit").click()
    assert "Shipped" in page.locator(".order-card").inner_text()
    page.screenshot(path=str(OUT / "06-order-results.png"), full_page=True)
    page.locator(".results").screenshot(path=str(OUT / "06-order-detail.png"))
    browser.close()

print(f"Saved six screenshots in {OUT}")
