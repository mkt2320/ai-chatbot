import asyncio
import os
import json
from pathlib import Path
from urllib.parse import urlparse
from datetime import datetime
from dotenv import load_dotenv
from playwright.async_api import async_playwright
from urls import URLS_TO_SCRAPE

# Load .env variables
load_dotenv()
HEADLESS_MODE = os.getenv("SCRAPER_HEADLESS", "true").lower() == "true"

SCRAPED_DATA_DIR = Path(__file__).parent / "scraped_data"
SCRAPED_DATA_DIR.mkdir(parents=True, exist_ok=True)

PERSISTENT_PROFILE_DIR = Path(__file__).parent / ".pw_profile"

def slugify(url: str) -> str:
    slug = urlparse(url).path.strip("/").replace("/", "_")
    return slug or "homepage"

async def scrape_page(playwright, url: str):
    browser = await playwright.chromium.launch_persistent_context(
        user_data_dir=str(PERSISTENT_PROFILE_DIR),
        headless=HEADLESS_MODE,
        viewport={"width": 1280, "height": 800},
        args=["--start-maximized"]
    )
    page = await browser.new_page()
    await page.goto(url, wait_until="networkidle", timeout=90000)
    await page.wait_for_timeout(4000)

    html = await page.content()
    title = await page.title()

    paragraphs = await page.evaluate("""
        () => Array.from(document.querySelectorAll("p, h1, h2, h3, li"))
            .map(el => el.innerText.trim())
            .filter(txt => txt.length > 40)
    """)

    links = await page.evaluate("""
        () => Array.from(document.querySelectorAll("a[href]"))
            .map(a => ({ text: a.innerText.trim(), href: a.href }))
            .filter(a => a.text && a.href)
    """)

    images = await page.evaluate("""
        () => Array.from(document.querySelectorAll("img[src]"))
            .map(img => img.src)
    """)

    tables = await page.evaluate("""
        () => Array.from(document.querySelectorAll("table")).map(table =>
            Array.from(table.rows).map(row =>
                Array.from(row.cells).map(cell => cell.innerText.trim())
            )
        )
    """)

    await browser.close()

    return {
        "url": url,
        "title": title,
        "scraped_at": datetime.utcnow().isoformat(),
        "paragraphs": paragraphs,
        "links": links,
        "images": images,
        "tables": tables,
        "html_preview": html[:1000]
    }

async def scrape_all():
    async with async_playwright() as playwright:
        for url in URLS_TO_SCRAPE:
            try:
                print(f"[->] Scraping: {url}")
                data = await scrape_page(playwright, url)
                file_path = SCRAPED_DATA_DIR / (slugify(url) + ".json")
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)
                print(f"[-->] Saved: {file_path.name}")
            except Exception as e:
                print(f"[x] Failed: {url} -> {e}")

if __name__ == "__main__":
    asyncio.run(scrape_all())
