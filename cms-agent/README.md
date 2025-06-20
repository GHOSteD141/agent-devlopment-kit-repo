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
│   ├── main.py                   # Entry point for the application (CLI)
│   ├── web_api.py                # FastAPI backend for web integration
│   ├── flask_api.py              # Flask backend (alternative modular API)
│   └── demo_products.py          # Demo product data for initial state
├── eval
│   └── cms_scenario_default.json # Default scenario for testing the CMS agent
├── chat.html                     # Frontend chat UI
├── chat.css                      # Styles for chat UI
├── shop.html                     # Frontend shop UI
├── shop.css                      # Styles for shop UI
├── requirements.txt              # Lists project dependencies
├── cms_documentation.md          # Project and code documentation
├── # Code Citations.md           # External code references and attributions
└── README.md                     # Project documentation
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

## Testing Instructions

Follow these steps to test the CMS Agent project:

### 1. Command-Line Interface (CLI) Testing

- Run the agent in CLI mode:
  ```
  python src/main.py
  ```
- Interact with the agent by typing messages in the terminal.
- To exit, type `x` and press Enter.

### 2. FastAPI Web API Testing

- Start the FastAPI backend:
  ```
  uvicorn src.web_api:app --reload
  ```
- Open your browser and go to:
  - [http://localhost:8000/shop](http://localhost:8000/shop) for the shop UI
  - [http://localhost:8000/chat](http://localhost:8000/chat) for the chat UI
- You can also test the API endpoints (e.g., `/chat`, `/products`) using tools like Postman or curl.

### 3. Flask Web API Testing (Alternative)

- Start the Flask backend:
  ```
  python src/flask_api.py
  ```
- The API will be available at [http://localhost:5000](http://localhost:5000).
- Endpoints:
  - `/chat` (POST): Send JSON `{"message": "your text"}` to chat with the agent.
  - `/products` (GET): Retrieve the current product list.

### 4. Frontend Testing

- Ensure the FastAPI backend is running.
- Open `shop.html` or `chat.html` in your browser (or access via `/shop` and `/chat` routes).
- Interact with the CMS agent and verify that content creation, updates, and retrieval work as expected.

### 5. Scenario Testing

- Use the provided scenario file for automated or manual testing:
  ```
  eval/cms_scenario_default.json
  ```
- Judges can review or run this scenario to verify agent behavior for create, update, delete, and retrieve actions.

## Google Technologies Used

- **Google Agent Development Kit (ADK)**:  
  Used for building, managing, and running conversational agents and tools.

- **Google Gemini Models**:  
  Used as the underlying language model for agent responses.

- **google.genai**:  
  Provides types and utilities for working with generative AI models.

## Additional Information

- The `cms_agent.py` file contains the core logic for the CMS agent, including how it interacts with memory and tools.
- The `cms_tools.py` file includes functions tailored for content management tasks.
- The `cms_scenario_default.json` file provides a template for testing various scenarios the CMS agent may encounter.

For further details on the implementation and available functions, please refer to the respective source files in the `src` directory.