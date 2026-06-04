from fastapi import FastAPI

from v1.schemas import MessageRequest
from v1.tools import send_email

app = FastAPI(
    title="AI Email Router",
    docs_url="/api/v1/docs",
    openapi_url="/api/v1/openapi.json"
)


@app.get("/")
def health():
    return {"status": "ok"}
    
@app.post("/api/v1/messages")
def route_message(request: MessageRequest):

    send_email(
        to_email="other@example.com",
        sender_email=request.email,
        message_text=request.message
    )

    return {
        "status": "sent"
    }