from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from schemas import ChatbotRequest, ChatbotResponse

app = FastAPI()

# Allow frontend access to backend API 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# POST /chat endpoint: returns placeholder chatbot response
@app.post("/chat", response_model=ChatbotResponse)
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
