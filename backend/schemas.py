from pydantic import BaseModel
from typing import List

# Incoming request schema
class ChatbotRequest(BaseModel):
    message: str              # User message bubble request

# Outgoing response schema
class ChatbotResponse(BaseModel):
    reply: str                # For bot message bubble response
    references: List[str]     # Reference links used in bot message bubble response
