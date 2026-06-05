from fastapi import FastAPI
import time
import requests

from v1.schemas import MessageRequest
from v1.agent import agent, EmailDeps

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

            if any(m["name"] == "llama3.1:8b" for m in models):
                print("Model available")
                break

        except Exception:
            pass

        time.sleep(2)

@app.get("/")
def health():
    return {"status": "ok"}
    
@app.post("/api/v1/route-messages")
async def route_message(request: MessageRequest):

    result = await agent.run(
        request.message,
        deps=EmailDeps(
            sender_email=request.email,
            original_message=request.message
        )
    )

    return {
        "status": "sent",
        "OUTPUT:": result.output,
        "MESSAGES:": result.all_messages()
    }