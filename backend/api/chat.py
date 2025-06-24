from fastapi import APIRouter
from models.chat import ChatbotRequest, ChatbotResponse
from sentence_transformers import SentenceTransformer
from transformers import pipeline
from pathlib import Path
import numpy as np
import json
import re
from utils.graph_facts import get_graph_facts

router = APIRouter()

# Load model for embeddings
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Load summarizer (lightweight)
summarizer = pipeline("summarization", model="t5-small", tokenizer="t5-small")

# Load metadata
META_PATH = Path("embeddings/index_metadata.json")
metadata = []
stored_embeddings = np.array([])

if META_PATH.exists() and META_PATH.stat().st_size > 0:
    with open(META_PATH, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    # Normalize stored embeddings
    stored_embeddings = np.array([entry["embedding"] for entry in metadata]).astype(
        "float32"
    )
    stored_embeddings = stored_embeddings / np.linalg.norm(
        stored_embeddings, axis=1, keepdims=True
    )
else:
    print(
        "Warning: embeddings/index_metadata.json not found or empty. Run the /refresh endpoint first."
    )

# Constants
SIMILARITY_THRESHOLD = 0.4
TOP_K = 5
QUESTION_PATTERNS = re.compile(
    r"^(what|how|why|where|when|who|can|does|is|are|should|could|would|do)\b",
    re.IGNORECASE,
)

SMALL_TALK_PATTERNS = {
    "hello": "Hello! How can I help you today?",
    "hi": "Hi there! What can I assist you with?",
    "how are you": "I'm just a bot, but I'm here and ready to help!",
    "what's up": "I'm here to answer your questions. Feel free to ask!",
    "thank you": "You're welcome!",
    "thanks": "Happy to help!",
    "bye": "Goodbye! Have a great day!",
    "good morning": "Good morning! Hope you're having a great start to your day.",
    "good evening": "Good evening! How can I assist you?",
    "who made you?": "I was developed by a human... but don't worry, I'm well trained!",
    "tell me a joke": "Why do programmers hate nature? Too many bugs!",
    "who are you?": "I'm your friendly AI chatbot, here to assist you with your questions."
}


def detect_small_talk(query: str) -> str:
    lower_query = query.lower().strip()
    for pattern, response in SMALL_TALK_PATTERNS.items():
        if lower_query == pattern:
            return response
    return ""

@router.post("/chat", response_model=ChatbotResponse)
def chatbot_endpoint(request: ChatbotRequest):
    query = request.message.strip()
    if not query:
        return ChatbotResponse(reply="Please enter a valid message.", references=[])

    # Check for small talk
    small_talk_response = detect_small_talk(query)
    if small_talk_response:
        return ChatbotResponse(reply=small_talk_response, references=[])
    
    # Generate embedding for query
    query_vec = embedding_model.encode([query])[0]
    query_vec = query_vec / np.linalg.norm(query_vec)

    # Calculate cosine similarities
    similarities = np.dot(stored_embeddings, query_vec)
    top_indices = similarities.argsort()[-TOP_K:][::-1]

    chunks = []
    reference_map = {}
    seen_texts = set()
    query_keywords = set(query.lower().split())

    for idx in top_indices:
        similarity = similarities[idx]
        if similarity < SIMILARITY_THRESHOLD:
            continue

        match = metadata[idx]
        text = match["content"].strip()
        source = match["source"].strip()

        # Filter irrelevant or duplicate content
        if (
            text in seen_texts
            or len(text) < 40
            or text.count(" ") < 3
            or QUESTION_PATTERNS.match(text)
            or not any(word in text.lower() for word in query_keywords)
        ):
            continue

        seen_texts.add(text)

        if source not in reference_map:
            reference_map[source] = len(reference_map) + 1

        chunks.append((text, source))

    # Include relevant Graph facts
    graph_facts = []
    known_node_ids = {"kitkat", "carnation", "sustainability", "nestle"}
    for node_id in known_node_ids:
        if node_id in query.lower():
            try:
                graph_facts.extend(get_graph_facts(node_id))
            except Exception as e:
                print(f"[Warning] Failed to fetch graph facts for '{node_id}': {e}")

    # Summarize extracted content
    combined_text = " ".join(text for text, _ in chunks)
    summary = ""
    if combined_text:
        try:
            input_length = len(combined_text.split())
            max_new_tokens = max(
                30, min(120, int(input_length * 0.6))
            )  # Limit for summary output

            summary = summarizer(
                combined_text, max_new_tokens=max_new_tokens, do_sample=False
            )[0]["summary_text"]
        except Exception:
            summary = combined_text[:300]

    # Build reference block
    used_sources = []
    reference_lines = []
    for text, source in chunks:
        ref_num = reference_map[source]
        if source not in used_sources:
            used_sources.append(source)
        reference_lines.append(f"{text} [{ref_num}]")

    reference_block = "\n\n".join(reference_lines)
    graph_block = "\n".join(graph_facts)

    # Final reply formatting
    if graph_facts:
        full_reply = f"{graph_block}\n\n{summary}\n\n{reference_block}".strip()
    else:
        full_reply = f"{summary}\n\n{reference_block}".strip()

    if not full_reply:
        return ChatbotResponse(
            reply="I'm sorry, I couldn't find anything relevant. Please try rephrasing your question.",
            references=[],
        )

    # Sort references by their assigned number
    ordered_refs = [
        url
        for url, num in sorted(reference_map.items(), key=lambda x: x[1])
        if url in used_sources
    ]

    return ChatbotResponse(
        reply=full_reply[:1].upper() + full_reply[1:], references=ordered_refs
    )
