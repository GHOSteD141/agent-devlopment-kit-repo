# README.md

# CMS Agent

This project implements a Content Management System (CMS) agent using the Google ADK framework. The CMS agent is designed to manage content effectively, allowing for the creation, updating, and deletion of content items.

## Project Structure

The project is organized as follows:

```
cms-agent
├── src
│   ├── agents
│   │   └── cms_agent.py          # Defines the CMS agent and its logic
│   ├── tools
│   │   ├── memory.py             # Functions for memorizing and forgetting information
│   │   └── cms_tools.py          # Tools specific to CMS tasks
│   ├── shared_libraries
│   │   └── constants.py          # Constants used throughout the project
│   ├── sessions
│   │   └── state.py              # Manages the session state for the agent
│   └── main.py                   # Entry point for the application
├── eval
│   └── cms_scenario_default.json  # Default scenario for testing the CMS agent
├── requirements.txt               # Lists project dependencies
└── README.md                      # Project documentation
```

## Setup Instructions

1. **Clone the Repository**: 
   ```
   git clone <repository-url>
   cd cms-agent
   ```

2. **Install Dependencies**: 
   Ensure you have Python installed, then run:
   ```
   pip install -r requirements.txt
   ```

3. **Run the Agent**: 
   Execute the main script to start the CMS agent:
   ```
   python src/main.py
   ```

## Usage Examples

- **Creating Content**: Use the CMS agent to create new content items by sending a request to the agent with the necessary parameters.
- **Updating Content**: The agent can also handle requests to update existing content, ensuring that the latest information is stored.
- **Deleting Content**: To remove content, send a delete request to the agent with the identifier of the content to be removed.

## Additional Information

- The `cms_agent.py` file contains the core logic for the CMS agent, including how it interacts with memory and tools.
- The `cms_tools.py` file includes functions tailored for content management tasks.
- The `cms_scenario_default.json` file provides a template for testing various scenarios the CMS agent may encounter.

For further details on the implementation and available functions, please refer to the respective source files in the `src` directory.