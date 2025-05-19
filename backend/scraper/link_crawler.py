import asyncio
import os
import json
from pathlib import Path
from urllib.parse import urlparse
from dotenv import load_dotenv
from playwright.async_api import async_playwright
from urls import URLS_TO_SCRAPE

# Load .env
load_dotenv()
HEADLESS_MODE = os.getenv("SCRAPER_HEADLESS", "true").lower() == "true"

CRAWLED_DATA_DIR = Path(__file__).parent / "crawled_data"
CRAWLED_DATA_DIR.mkdir(parents=True, exist_ok=True)
DISCOVERED_LINKS_PATH = CRAWLED_DATA_DIR / "discovered_links.json"
PERSISTENT_PROFILE_DIR = Path(__file__).parent / ".pw_profile"
BASE_DOMAIN = "www.madewithnestle.ca"

async def extract_internal_links(playwright, url):
    browser = await playwright.chromium.launch_persistent_context(
        user_data_dir=str(PERSISTENT_PROFILE_DIR),
        headless=HEADLESS_MODE,
        viewport={"width": 1280, "height": 800},
        args=["--start-maximized"]
    )
    page = await browser.new_page()
    await page.goto(url, wait_until="networkidle", timeout=90000)
    await page.wait_for_timeout(3000)

    links = await page.evaluate("""
        () => Array.from(document.querySelectorAll("a[href]"))
            .map(a => a.href)
            .filter(href => href.startsWith("https://www.madewithnestle.ca"))
    """)

    await browser.close()
    return links

async def crawl_seed_urls():
    all_links = set()

    async with async_playwright() as playwright:
        for seed_url in URLS_TO_SCRAPE:
            try:
                print(f"[→] Crawling: {seed_url}")
                found_links = await extract_internal_links(playwright, seed_url)
                for link in found_links:
                    parsed = urlparse(link)
                    if parsed.netloc == BASE_DOMAIN:
                        cleaned = link.split("?")[0].rstrip("/")
                        all_links.add(cleaned)
            except Exception as e:
                print(f"[x] Failed to extract from {seed_url}: {e}")

    sorted_links = sorted(all_links)
    with open(DISCOVERED_LINKS_PATH, "w", encoding="utf-8") as f:
        json.dump(sorted_links, f, indent=2)

    print(f"[-->] Found {len(sorted_links)} internal links -> saved to {DISCOVERED_LINKS_PATH.name}")

if __name__ == "__main__":
    asyncio.run(crawl_seed_urls())
