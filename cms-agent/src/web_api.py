from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os
from fastapi import UploadFile, File
from fastapi.responses import JSONResponse, FileResponse
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles

# Ensure the src directory is in sys.path for module resolution
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import cms_conversational_agent, InMemorySessionService, Runner, types

# Session setup (reuse for all users for demo)
session_service = InMemorySessionService()
APP_NAME = "cms_agent_app"
USER_ID = "web_user"
SESSION_ID = "web_session"

async def ensure_session():
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )

@asynccontextmanager
async def lifespan(app: FastAPI):
    await ensure_session()
    yield

app = FastAPI(lifespan=lifespan)

# Allow CORS for all origins (for local HTML/JS testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

runner = Runner(
    agent=cms_conversational_agent,
    app_name=APP_NAME,
    session_service=session_service
)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    content = types.Content(role='user', parts=[types.Part(text=req.message)])
    response_text = ""
    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=content
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                text_parts = [p.text for p in event.content.parts if hasattr(p, "text") and p.text]
                response_text = " ".join(text_parts) if text_parts else "[No text response]"
    return {"response": response_text}

@app.get("/")
async def root():
    return {"status": "ok", "message": "CMS Agent API is running."}

# Serve the static directory (adjust path if needed)
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "..")), name="static")

@app.get("/chat")
async def chat_page():
    # Adjust the path if chat.html is not in the parent directory of src
    html_path = os.path.join(os.path.dirname(__file__), "..", "chat.html")
    return FileResponse(html_path)

# The FastAPI server is running locally at:
#   http://127.0.0.1:8000
# or
#   http://localhost:8000

# Your HTML/JS frontend should POST to http://localhost:8000/chat
