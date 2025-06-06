from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from agents.cms_agent import CMSAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
import os
from typing import List

# Remove DummySession, DummyInvocationContext, and ToolContext usage for agent running

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

# Define tools for the agent
tools = [
    FunctionTool(create_content_tool),
    FunctionTool(update_content_tool),
    FunctionTool(delete_content_tool),
    FunctionTool(retrieve_content_tool),
]

# Set your Gemini API key (replace with your actual key)
os.environ["GOOGLE_API_KEY"] = "AIzaSyAx7LRR8jDqUDb8nplrRujv8SL0zhNdh6c"

# Use Gemini 2.0 Flash model as requested
cms_conversational_agent = Agent(
    model="gemini-2.0-flash",
    name="cms_conversational_agent",
    instruction=(
        "You are a conversational CMS agent. "
        "You help users create, update, delete, and retrieve content items. "
        "Use your tools to manage content as requested by the user. "
        "Be friendly and helpful, and ask for clarification if the user's request is ambiguous."
    ),
    description="A conversational agent for managing CMS content.",
    tools=tools,
)

# Instead of using DummyInvocationContext, pass only the user input string to run_live.
# This matches the ADK 1.2.1 pattern where the framework manages context.

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
                        print("Agent:", event.content.parts[0].text)
        asyncio.run(print_response())

if __name__ == "__main__":
    main()