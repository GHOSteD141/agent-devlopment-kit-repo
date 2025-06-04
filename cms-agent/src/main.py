def main():
    from google.adk.tools import ToolContext
    from google.adk.agents.callback_context import CallbackContext
    from src.agents.cms_agent import CMSAgent
    from src.sessions.state import State

    # Initialize the tool context and session state
    tool_context = ToolContext(state=State())
    
    # Load any necessary configurations or initial states
    # This could include loading from a JSON file or setting defaults
    # For example, you might load a scenario from eval/cms_scenario_default.json

    # Create an instance of the CMS agent
    cms_agent = CMSAgent(tool_context)

    # Start the agent's processing loop
    while True:
        # Here you would typically wait for input or events to process
        # For example, you might listen for user commands or API requests
        command = input("Enter command for CMS agent: ")
        response = cms_agent.process_command(command)
        print(response)

if __name__ == "__main__":
    main()