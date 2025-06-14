from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os
from fastapi import UploadFile, File
from fastapi.responses import JSONResponse, FileResponse
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

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
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/chat")
async def chat_page():
    # Adjust the path if chat.html is not in the parent directory of src
    html_path = os.path.join(static_dir, "chat.html")
    return FileResponse(html_path)

@app.get("/shop")
async def shop_page():
    html_path = os.path.join(static_dir, "shop.html")
    return FileResponse(html_path)

@app.get("/products")
async def get_products():
    # Try to get products from CMS agent's memory
    try:
        from main import cms_agent_logic
        content_list = cms_agent_logic.tool_context.state.get('content', [])
    except Exception:
        content_list = []
    # If empty, return a default product list for demo
    if not content_list:
        content_list = [
            {
                "title": "Premium Wireless Headphones",
                "price": 199.99,
                "image": "https://images.unsplash.com/photo-1618160702438-9b02ab6515c9?w=400&h=300&fit=crop",
                "category": "Electronics",
                "body": "High-fidelity sound, noise cancellation, and all-day comfort."
            },
            {
                "title": "Modern Living Room Set",
                "price": 1299.99,
                "image": "https://images.unsplash.com/photo-1721322800607-8c38375eef04?w=400&h=300&fit=crop",
                "category": "Furniture",
                "body": "Elegant design and comfort for your home."
            },
            {
                "title": "Cozy Pet Blanket",
                "price": 29.99,
                "image": "https://images.unsplash.com/photo-1582562124811-c09040d0a901?w=400&h=300&fit=crop",
                "category": "Pet Supplies",
                "body": "Soft, warm, and perfect for your furry friends."
            },
            {
                "title": "Mountain Adventure Gear",
                "price": 399.99,
                "image": "https://images.unsplash.com/photo-1493962853295-0fd70327578a?w=400&h=300&fit=crop",
                "category": "Outdoor",
                "body": "Everything you need for your next adventure."
            },
            {
                "title": "Premium Cat Toy Collection",
                "price": 49.99,
                "image": "https://images.unsplash.com/photo-1535268647677-300dbf3d78d1?w=400&h=300&fit=crop",
                "category": "Pet Supplies",
                "body": "Keep your cat entertained for hours."
            },
            {
                "title": "Natural Honey & Bee Products",
                "price": 24.99,
                "image": "https://images.unsplash.com/photo-1498936178812-4b2e558d2937?w=400&h=300&fit=crop",
                "category": "Food & Beverages",
                "body": "Pure, natural, and delicious honey products."
            }
        ]
    return {"products": content_list}

# The FastAPI server is running locally at:
#   http://127.0.0.1:8000
# or
#   http://localhost:8000

# Your HTML/JS frontend should POST to http://localhost:8000/chat
# Your HTML/JS frontend should POST to http://localhost:8000/chat
