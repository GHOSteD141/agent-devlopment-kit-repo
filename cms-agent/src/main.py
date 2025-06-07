from google.adk.agents import Agent
from google.adk.tools import FunctionTool, google_search
from agents.cms_agent import CMSAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
import os
from typing import List

# Wrap CMS logic as tools
def create_content_tool(title: str, body: str, tags: List[str]) -> dict:
    # Ensure tags is always a list (ADK requires this for schema)
    if tags is None:
        tags = []
    return cms_agent_logic.create_content(title, body, tags)

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

# CMS tools
cms_tools = [
    FunctionTool(create_content_tool),
    FunctionTool(update_content_tool),
    FunctionTool(delete_content_tool),
    FunctionTool(retrieve_content_tool),
]

# Set your Gemini API key (replace with your actual key)
os.environ["GOOGLE_API_KEY"] = "AIzaSyAx7LRR8jDqUDb8nplrRujv8SL0zhNdh6c"

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

# --- Sub-agent: Google Search Agent ---
# Use a supported model for function calling (Gemini 1.5 Pro or Gemini 1.0 Pro)
search_agent = Agent(
    model="gemini-1.5-pro",  # Use a model that supports function calling/tools
    name="search_agent",
    instruction="You are a search agent. Use the google_search tool to answer user questions that require up-to-date information from the web.",
    description="Handles web search queries using Google Search.",
    tools=[google_search]
)

# --- Root CMS Agent (Orchestrator) ---
cms_conversational_agent = Agent(
    model="gemini-2.0-flash",
    name="cms_conversational_agent",
    instruction=(
        "You are a conversational CMS agent. "
        "You help users create, update, delete, and retrieve content items using your CMS tools. "
        "If the user greets you, delegate to the greeting_agent. "
        "If the user says goodbye, delegate to the farewell_agent. "
        "If the user asks a general question or for information not in the CMS, delegate to the search_agent. "
        "Otherwise, handle the request yourself using your CMS tools. "
        "Be friendly and helpful, and ask for clarification if the user's request is ambiguous."
    ),
    description="A conversational agent for managing CMS content, greetings, farewells, and web search.",
    tools=cms_tools,
    sub_agents=[greeting_agent, farewell_agent, search_agent]
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
    #python "c:\Users\SHREYAJIT BEURA\OneDrive\Documents\GitHub\agent-devlopment-kit-repo\cms-agent\src\main.py"  (this is the command to run the script)