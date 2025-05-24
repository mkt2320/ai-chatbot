from fastapi import APIRouter
from schemas import ChatbotRequest, ChatbotResponse
from sentence_transformers import SentenceTransformer
import numpy as np
import json
from pathlib import Path

router = APIRouter()

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load metadata with embeddings
META_PATH = Path("embeddings/index_metadata.json")
with open(META_PATH, "r", encoding="utf-8") as f:
    metadata = json.load(f)

# Prepare normalized embeddings
stored_embeddings = np.array([entry["embedding"] for entry in metadata]).astype("float32")
stored_embeddings = stored_embeddings / np.linalg.norm(stored_embeddings, axis=1, keepdims=True)

SIMILARITY_THRESHOLD = 0.4
TOP_K = 5

@router.post("/chat", response_model=ChatbotResponse)
def chatbot_endpoint(request: ChatbotRequest):
    query = request.message.strip()
    if not query:
        return ChatbotResponse(reply="Please enter a valid message.", references=[])

    query_embedding = model.encode([query])[0]
    query_embedding = query_embedding / np.linalg.norm(query_embedding)

    similarities = np.dot(stored_embeddings, query_embedding)
    top_indices = similarities.argsort()[-TOP_K:][::-1]

    reply_chunks = []
    references = []
    seen_texts = set()
    reference_map = {}

    for idx in top_indices:
        similarity = similarities[idx]
        if similarity < SIMILARITY_THRESHOLD:
            continue

        match = metadata[idx]
        text = match["content"].strip()
        source = match["source"].strip()

        if text in seen_texts:
            continue
        seen_texts.add(text)

        if source not in reference_map:
            reference_map[source] = len(reference_map) + 1

        ref_number = reference_map[source]
        reply_chunks.append(f"{text} [{ref_number}]")
        references.append(source)

    if not reply_chunks:
        return ChatbotResponse(
            reply="I'm sorry, I couldn't find anything relevant. Please try rephrasing your question.",
            references=[]
        )

    reply = "\n\n".join(reply_chunks)
    sorted_sources = [url for url, _ in sorted(reference_map.items(), key=lambda item: item[1])]

    return ChatbotResponse(reply=reply, references=sorted_sources)
