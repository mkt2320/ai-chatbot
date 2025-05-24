from pathlib import Path
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List
import os

# Initialize sentence-transformers model
MODEL_NAME = "all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_NAME)

# Paths
SCRAPED_DIR = Path("scraper/scraped_data") 
OUTPUT_DIR = Path("embeddings")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Storage
embedding_vectors: List[List[float]] = []
metadata_records = []

# Loop through scraped JSON files
for file_path in SCRAPED_DIR.glob("*.json"):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        url = data.get("url")
        paragraphs = data.get("paragraphs", [])

        for para in paragraphs:
            if not para.strip():
                continue
            embedding = model.encode(para)
            embedding_vectors.append(embedding.tolist())
            metadata_records.append({
                "source": url,
                "content": para,
                "embedding": embedding.tolist()
            })

# Build FAISS index
dimension = len(embedding_vectors[0])
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embedding_vectors).astype("float32"))

# Save index and metadata
faiss.write_index(index, str(OUTPUT_DIR / "index.faiss"))
with open(OUTPUT_DIR / "index_metadata.json", "w", encoding="utf-8") as f:
    json.dump(metadata_records, f, indent=2)

print(f"[->] Embedded {len(metadata_records)} chunks. Saved to {OUTPUT_DIR}")
