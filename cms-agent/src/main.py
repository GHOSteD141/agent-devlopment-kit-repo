from google.adk.agents import Agent
from google.adk.tools import FunctionTool, google_search
import sys
import os

# Ensure the src directory is in sys.path for module resolution
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.cms_agent import CMSAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
from typing import List
from demo_products import demo_products

# Utility: Generate an image URL for new content (replace with Gemini image API if available)
def generate_image_url(title: str, body: str) -> str:
    # Placeholder: Use a service like Unsplash or via.placeholder.com
    # For demo, use Unsplash with the title as a search query
    import urllib.parse
    query = urllib.parse.quote(title or "product")
    return f"https://source.unsplash.com/400x300/?{query}"

# Wrap CMS logic as tools
def create_content_tool(title: str, body: str, tags: List[str]) -> dict:
    # Ensure tags is always a list (ADK requires this for schema)
    if tags is None:
        tags = []
    result = cms_agent_logic.create_content(title, body, tags)
    # If content was created, generate and attach an image
    if result.get("status") == "Content created" and "content" in result:
        image_url = generate_image_url(title, body)
        result["content"]["image"] = image_url
        # Also update in backend state for consistency
        for item in cms_agent_logic.tool_context.state.get("content", []):
            if item.get("id") == result["content"].get("id"):
                item["image"] = image_url
    return result

def update_content_tool(content_id: str, updates: dict):
    return cms_agent_logic.update_content(content_id, updates)

def delete_content_tool(content_id: str):
    return cms_agent_logic.delete_content(content_id)

def retrieve_content_tool(content_id: str):
    return cms_agent_logic.get_content(content_id)

# Fix: Provide a minimal tool_context with a .state attribute (use a simple class)
class SimpleToolContext:
    def __init__(self):
        self.state = {}

cms_agent_logic = CMSAgent(SimpleToolContext())

# Prepopulate CMS agent memory with demo products
cms_agent_logic.tool_context.state['content'] = demo_products.copy()

# CMS tools
cms_tools = [
    FunctionTool(create_content_tool),
    FunctionTool(update_content_tool),
    FunctionTool(delete_content_tool),
    FunctionTool(retrieve_content_tool),
]

# Set your Gemini API key (replace with your actual key)
os.environ["GOOGLE_API_KEY"] = "AIzaSyDEyY-uS7_KV1eaDBjPudqRjHfyowgahMk"


# --- Sub-agent: Greeting Agent ---
greeting_agent = Agent(
    model="gemini-2.0-flash",
    name="greeting_agent",
    instruction="You are a greeting agent. Greet the user in a friendly way. Do not perform any other tasks.",
    description="Handles greetings.",
    tools=[]
)

# --- Sub-agent: Farewell Agent ---
farewell_agent = Agent(
    model="gemini-2.0-flash",
    name="farewell_agent",
    instruction="You are a farewell agent. Say goodbye to the user in a polite way. Do not perform any other tasks.",
    description="Handles farewells.",
    tools=[]
)

# --- Sub-agent: General Chat Agent (for unrelated topics) ---
general_chat_agent = Agent(
    model="gemini-2.0-flash",
    name="general_chat_agent",
    instruction="You are a helpful general-purpose assistant. Answer user questions or chat about topics not related to CMS management, greetings, or farewells.",
    description="Handles general conversation and unrelated topics.",
    tools=[]
)

# --- Sub-agent: Content Link Agent ---
def get_content_link_tool(content_id: str) -> dict:
    """Returns the website link for the given content ID."""
    # Replace with your actual URL pattern if needed
    base_url = "https://yourwebsite.com/content/"
    return {"link": f"{base_url}{content_id}"}

content_link_agent = Agent(
    model="gemini-2.0-flash",
    name="content_link_agent",
    instruction="You are a content link agent. When asked for a link to content, use the get_content_link_tool to provide the direct website link for the given content ID.",
    description="Provides website links for content items.",
    tools=[FunctionTool(get_content_link_tool)]
)

# Admin credentials (for demo, use env vars or a secure store in production)
ADMIN_ID = "admin"
ADMIN_PASSWORD = "admin123"

# --- Sub-agent: Verification Agent ---
def verify_admin_tool(user_id: str, password: str) -> dict:
    """Verifies if the provided user_id and password are correct for admin access.
    Username check is strict and must match 'admin' exactly (case-insensitive, trimmed)."""
    if user_id.strip().lower() == ADMIN_ID and password == ADMIN_PASSWORD:
        return {"is_admin": True, "message": "Admin verified. You have full access."}
    else:
        return {"is_admin": False, "message": "You are not an admin. Only content search/retrieval is allowed."}

verification_agent = Agent(
    model="gemini-2.0-flash",
    name="verification_agent",
    instruction=(
        "You are a verification agent. When the user requests to create or update content, "
        "ask for their admin ID and password. Use the verify_admin_tool to check credentials. "
        "If verified, allow the operation. If not, deny creation/update and only allow content search or retrieval."
    ),
    description="Verifies if the user is admin before allowing content creation or update.",
    tools=[FunctionTool(verify_admin_tool)]
)

# --- Root CMS Agent (Orchestrator) ---
cms_conversational_agent = Agent(
    model="gemini-2.0-flash",
    name="cms_conversational_agent",
    instruction=(
        "You are a conversational CMS agent. "
        "If the user wants to create or update content, delegate to the verification_agent to check if they are admin. "
        "If the user asks for a content link, delegate to the content_link_agent. "
        "If the user greets you, delegate to the greeting_agent. "
        "If the user says goodbye, delegate to the farewell_agent. "
        "If the user asks about something unrelated to CMS, greetings, or farewells, delegate to the general_chat_agent. "
        "Otherwise, handle the request yourself using your CMS tools. "
        "Be friendly and helpful, and ask for clarification if the user's request is ambiguous."
    ),
    description="A conversational agent for managing CMS content, greetings, farewells, verification, content links, and general chat.",
    tools=[
        FunctionTool(create_content_tool),
        FunctionTool(update_content_tool),
        FunctionTool(delete_content_tool),
        FunctionTool(retrieve_content_tool),
    ],
    sub_agents=[
        greeting_agent,
        farewell_agent,
        verification_agent,
        content_link_agent,
        general_chat_agent
    ]
)

def main():
    print("Welcome to the Conversational CMS Agent! Type 'exit' to quit.")

    # Setup session service and runner
    session_service = InMemorySessionService()
    APP_NAME = "cms_agent_app"
    USER_ID = "user_1"
    SESSION_ID = "session_001"

    # Create a session (if not already exists)
    import asyncio
    async def setup_session():
        await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=SESSION_ID
        )
    asyncio.run(setup_session())

    runner = Runner(
        agent=cms_conversational_agent,
        app_name=APP_NAME,
        session_service=session_service
    )

    while True:
        user_input = input("You: ")
        if user_input.strip().lower() == "x":
            break

        # Prepare ADK Content object for the user message
        content = types.Content(role='user', parts=[types.Part(text=user_input)])

        async def print_response():
            async for event in runner.run_async(
                user_id=USER_ID,
                session_id=SESSION_ID,
                new_message=content
            ):
                if event.is_final_response():
                    if event.content and event.content.parts:
                        text_parts = [p.text for p in event.content.parts if hasattr(p, "text") and p.text]
                        if text_parts:
                            print("Agent:", " ".join(text_parts))
                        else:
                            print("Agent: [No text response]")
        asyncio.run(print_response())

if __name__ == "__main__":
    main()
