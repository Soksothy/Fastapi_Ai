from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import requests
import time
from starlette.middleware.base import BaseHTTPMiddleware

class PromptRequest(BaseModel):
    prompt: str

class ResponseTimeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

app = FastAPI()
app.add_middleware(ResponseTimeMiddleware)

OLLAMA_URL = "http://localhost:11434/api/generate"

@app.get("/")
def home():
    return {"message": "FastAPI is running with Ollama Llama 3.2!"}

@app.get("/status")
def status():
    return {"status": "Server is running"}

@app.post("/generate")
def generate_text(request: PromptRequest):
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": "llama3.2", 
            "prompt": request.prompt,
            "stream": False
        })
        data = response.json()
        return {"response": data.get("response", "No response")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
