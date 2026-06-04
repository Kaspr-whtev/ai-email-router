from fastapi import FastAPI
import time
import requests

from v1.schemas import MessageRequest
from v1.schemas import ClassificationRequest
from v1.tools import send_email

app = FastAPI(
    title="AI Email Router",
    docs_url="/api/v1/docs",
    openapi_url="/api/v1/openapi.json"
)

@app.on_event("startup")
async def wait_for_model():
    print("Waiting for Ollama model...")

    while True:
        try:
            response = requests.get(
                "http://ollama:11434/api/tags",
                timeout=5,
            )

            models = response.json()["models"]

            if any(m["name"] == "llama3.2:3b" for m in models):
                print("Model available")
                break

        except Exception:
            pass

        time.sleep(2)

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

@app.post("/api/v1/classify")
def classify(request: ClassificationRequest):

    prompt = f"""
Wybierz jeden dział dla wiadomości.

Dostępne działy:

- human-resources@example.com
- help-desk@example.com
- it@example.com
- kadry@example.com
- other@example.com

Wiadomość:

{request.message}

Odpowiedz wyłącznie adresem email działu.
"""

    response = requests.post(
        "http://ollama:11434/api/generate",
        json={
            "model": "qwen3:4b",
            "prompt": prompt,
            "stream": False
        }
    )

    result = response.json()

    return {
        "department": result["response"]
    }