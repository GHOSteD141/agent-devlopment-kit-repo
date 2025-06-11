# CMS Agent Documentation

This document describes the purpose and functionality of each file in the CMS Agent project, and how each part works together.

---

## Project Structure Overview


---

## File-by-File Purpose and How It Works

### 1. `src/agents/cms_agent.py`
**Purpose:**  
Defines the `CMSAgent` class, which contains the core logic for content management (create, update, delete, retrieve).

**How it works:**  
- Implements methods for content operations.
- Used by tool functions in `main.py` to perform CMS actions.
- May interact with session state for context-aware operations.

---

### 2. `src/tools/memory.py`
**Purpose:**  
Provides utility functions for agent memory, such as storing and clearing information.

**How it works:**  
- Functions here can be used by agents or tools to remember or forget data during a session.

---

### 3. `src/tools/cms_tools.py`
**Purpose:**  
Contains tool functions for CMS operations.

**How it works:**  
- Functions like `create_content`, `update_content`, etc., are defined here.
- These are wrapped as ADK `FunctionTool` objects in `main.py` and exposed to the agent.

---

### 4. `src/shared_libraries/constants.py`
**Purpose:**  
Stores constants used throughout the project.

**How it works:**  
- Centralizes configuration values, keys, or other constants for easy reuse and maintainability.

---

### 5. `src/sessions/state.py`
**Purpose:**  
Defines the session state management logic.

**How it works:**  
- Implements the `State` class or related utilities.
- Used to track user/session data, such as admin status or preferences.

---

### 6. `src/main.py`
**Purpose:**  
Main entry point for running the CMS agent as a CLI or backend service.

**How it works:**  
- Imports and initializes all agents, tools, and session management.
- Defines sub-agents (greeting, farewell, verification, content link, mode switch, general chat).
- Sets up the root orchestrator agent with all sub-agents and tools.
- Handles user input and agent responses in a loop (CLI) or as a backend for the web API.

---

### 7. `src/web_api.py`
**Purpose:**  
Exposes the CMS agent as a FastAPI web API for integration with web frontends.

**How it works:**  
- Defines endpoints (e.g., `/chat`) for frontend-backend communication.
- Handles session setup and agent invocation for web clients.
- Allows the HTML/JS frontend to send user messages and receive agent responses.

---

### 8. `eval/cms_scenario_default.json`
**Purpose:**  
Provides default test scenarios for evaluating the CMS agent.

**How it works:**  
- Used for automated or manual testing of agent behavior and flows.

---

### 9. `requirements.txt`
**Purpose:**  
Lists all Python dependencies required for the project.

**How it works:**  
- Used with `pip install -r requirements.txt` to set up the Python environment.

---

### 10. `chat.html`
**Purpose:**  
Frontend HTML file for the conversational CMS agent web UI.

**How it works:**  
- Provides the chat interface for users to interact with the agent.
- Uses JavaScript to send user messages to the backend API and display responses.

---

### 11. `chat.css`
**Purpose:**  
CSS file for styling the chat UI in `chat.html`.

**How it works:**  
- Controls layout, colors, fonts, and responsive design for the chat interface.

---

### 12. `README.md`
**Purpose:**  
Main project readme with setup instructions, usage, and high-level overview.

**How it works:**  
- Guides users on how to install, run, and use the CMS agent project.

---

## How Everything Works Together

- The **backend** (`main.py`, `web_api.py`, agent/tool/session files) manages all agent logic, content operations, and user session state.
- The **frontend** (`chat.html`, `chat.css`) provides a user-friendly chat interface.
- The **web API** (`web_api.py`) connects the frontend and backend, allowing real-time chat with the agent.
- **Sub-agents** handle specialized tasks (greetings, farewells, verification, content links, mode switching, general chat), while the **root agent** orchestrates which agent should handle each user request.
- **Session state** ensures user/admin status and preferences are remembered across interactions.

---cms-agent ├── src │ ├── agents │ │ └── cms_agent.py │ ├── tools │ │ ├── memory.py │ │ └── cms_tools.py │ ├── shared_libraries │ │ └── constants.py │ ├── sessions │ │ └── state.py │ ├── main.py │ └── web_api.py ├── eval │ └── cms_scenario_default.json ├── requirements.txt ├── chat.html ├── chat.css └── README.md