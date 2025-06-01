import subprocess
import sys
from fastapi import APIRouter, BackgroundTasks

router = APIRouter()


# Runs crawler, scraper, and embedder in sequence
def run_refresh_pipeline():
    try:
        subprocess.run([sys.executable, "scraper/link_crawler.py"], check=True)
        subprocess.run([sys.executable, "scraper/scraper.py"], check=True)
        subprocess.run([sys.executable, "embeddings/embedder.py"], check=True)
        print("Background crawl + scrape + embed completed!")
    except Exception as e:
        print(f"[x] Background task failed: {e}")


@router.post("/refresh", status_code=202)
def refresh_scraped_data(background_tasks: BackgroundTasks):
    background_tasks.add_task(run_refresh_pipeline)
    return {
        "status": "started",
        "message": "Crawling, scraping, and embedding started in the background.",
    }
