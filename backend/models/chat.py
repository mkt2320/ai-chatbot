from pydantic import BaseModel
from typing import List


class ChatbotRequest(BaseModel):
    message: str


class ChatbotResponse(BaseModel):
    reply: str
    references: List[str]
