from fastapi import APIRouter
from schemas import ChatbotRequest, ChatbotResponse

router = APIRouter()

@router.post("/chat", response_model=ChatbotResponse)
def chatbot_endpoint(request: ChatbotRequest):
    return ChatbotResponse(
        reply=(
            "For Christmas, you might consider the following gift ideas from Nestlé:\n\n"
            "1. **KITKAT Advent Calendar**: Countdown to Christmas with KITKAT treats. [Buy in Store](https://www.madewithnestle.ca/kitkat) [1]\n"
            "2. **Quality Street Holiday Tin**: Perfect for sharing. [See all products](https://www.madewithnestle.ca/quality-street) [2]"
        ),
        references=[
            "https://www.madewithnestle.ca/kitkat",
            "https://www.madewithnestle.ca/quality-street"
        ]
    )
