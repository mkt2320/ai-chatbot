import asyncio
import os
import json
from pathlib import Path
from urllib.parse import urlparse
from datetime import datetime
from dotenv import load_dotenv
from playwright.async_api import async_playwright

# Load environment variables
load_dotenv()
HEADLESS_MODE = os.getenv("SCRAPER_HEADLESS", "true").lower() == "true"

SCRAPED_DATA_DIR = Path(__file__).parent / "scraped_data"
SCRAPED_DATA_DIR.mkdir(parents=True, exist_ok=True)
PERSISTENT_PROFILE_DIR = Path(__file__).parent / ".pw_profile"
CRAWLED_LINKS_FILE = Path(__file__).parent / "crawled_data" / "discovered_links.json"


def slugify(url: str) -> str:
    slug = urlparse(url).path.strip("/").replace("/", "_")
    return slug or "homepage"


async def scrape_page(page, url: str):
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=60000)
        await page.wait_for_timeout(1000)  # reduced delay

        html = await page.content()
        title = await page.title()

        paragraphs = await page.evaluate(
            """
            () => Array.from(document.querySelectorAll("p, h1, h2, h3, li"))
                .map(el => el.innerText.trim())
                .filter(txt => txt.length > 40)
        """
        )

        links = await page.evaluate(
            """
            () => Array.from(document.querySelectorAll("a[href]"))
                .map(a => ({ text: a.innerText.trim(), href: a.href }))
                .filter(a => a.text && a.href)
        """
        )

        images = await page.evaluate(
            """
            () => Array.from(document.querySelectorAll("img[src]"))
                .map(img => img.src)
        """
        )

        tables = await page.evaluate(
            """
            () => Array.from(document.querySelectorAll("table")).map(table =>
                Array.from(table.rows).map(row =>
                    Array.from(row.cells).map(cell => cell.innerText.trim())
                )
            )
        """
        )

        data = {
            "url": url,
            "title": title,
            "scraped_at": datetime.utcnow().isoformat(),
            "paragraphs": paragraphs,
            "links": links,
            "images": images,
            "tables": tables,
            "html_preview": html[:1000],
        }

        file_path = SCRAPED_DATA_DIR / (slugify(url) + ".json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"[->] Saved: {file_path.name}")
    except Exception as e:
        print(f"[X] Failed: {url} → {e}")


async def scrape_all():
    if not CRAWLED_LINKS_FILE.exists():
        print(
            "[X] Missing crawled_data/discovered_links.json. Run link_crawler.py first."
        )
        return

    with open(CRAWLED_LINKS_FILE, "r", encoding="utf-8") as f:
        urls = json.load(f)

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch_persistent_context(
            user_data_dir=str(PERSISTENT_PROFILE_DIR),
            headless=HEADLESS_MODE,
            viewport={"width": 1280, "height": 800},
            args=["--start-maximized"],
        )

        # Max 10 concurrent tabs
        semaphore = asyncio.Semaphore(10)

        async def limited_scrape(url):
            async with semaphore:
                page = await browser.new_page()
                await scrape_page(page, url)
                await page.close()

        tasks = [limited_scrape(url) for url in urls]
        await asyncio.gather(*tasks)
        await browser.close()


if __name__ == "__main__":
    asyncio.run(scrape_all())
