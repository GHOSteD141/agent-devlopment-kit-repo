def main():
    from google.adk.tools import ToolContext
    from google.adk.agents.callback_context import CallbackContext
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
    # tool_context.state is now available via invocation_context.session.state

    # Create an instance of the CMS agent
    cms_agent = CMSAgent(tool_context)

    # Start the agent's processing loop
    while True:
        print("Enter action (create_content, update_content, delete_content, retrieve_content) or 'exit':")
        action = input("Action: ").strip()
        if action == "exit":
            break
        params = {}
        if action == "create_content":
            params["title"] = input("Title: ")
            params["body"] = input("Body: ")
            tags = input("Tags (comma separated, optional): ")
            params["tags"] = [t.strip() for t in tags.split(",")] if tags else []
        elif action in ("update_content", "delete_content", "retrieve_content"):
            params["content_id"] = input("Content ID: ")
            if action == "update_content":
                updates = {}
                title = input("New Title (leave blank to skip): ")
                body = input("New Body (leave blank to skip): ")
                if title:
                    updates["title"] = title
                if body:
                    updates["body"] = body
                params["updates"] = updates
        request = {"action": action, "parameters": params}
        response = cms_agent.process_request(request)
        print(response)

if __name__ == "__main__":
    main()