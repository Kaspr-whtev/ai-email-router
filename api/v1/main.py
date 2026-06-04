from fastapi import FastAPI

from v1.schemas import MessageRequest

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
    return {
        "email": request.email,
        "message": request.message,
        "status": "received"
    }