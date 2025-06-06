from google.adk.agents import Agent
from google.adk.tools import ToolContext, FunctionTool
from agents.cms_agent import CMSAgent
from sessions.state import State

# --- Mock invocation_context and session for local testing ---
class MockSession:
    def __init__(self):
        self.state = State()
class MockInvocationContext:
    def __init__(self):
        self.session = MockSession()
# ------------------------------------------------------------

# Initialize the tool context and session state
invocation_context = MockInvocationContext()
tool_context = ToolContext(invocation_context)
cms_agent_logic = CMSAgent(tool_context)

# Wrap CMS logic as tools
def create_content_tool(title: str, body: str, tags=None):
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

# Define the conversational agent
cms_conversational_agent = Agent(
    model="gemini-2.0-pro",
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

def main():
    print("Welcome to the Conversational CMS Agent! Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.strip().lower() == "exit":
            break
        # Try the most likely conversation method
        response = cms_conversational_agent.run_conversation(user_input, tool_context=tool_context)
        print("Agent:", response)

if __name__ == "__main__":
    main()