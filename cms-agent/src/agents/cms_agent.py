# File: cms-agent/cms-agent/src/agents/cms_agent.py

class CMSAgent:
    def __init__(self, tool_context):
        self.tool_context = tool_context
        if 'content' not in self.tool_context.state:
            self.tool_context.state['content'] = []
        self._next_id = 1

    def create_content(self, title: str, body: str, tags=None):
        if not title or not body:
            return {"status": "Error", "message": "Title and body cannot be empty."}
        if tags is None:
            tags = []
        content_item = {
            "id": str(self._next_id),
            "title": title,
            "body": body,
            "tags": tags
        }
        self.tool_context.state['content'].append(content_item)
        self._next_id += 1
        return {"status": "Content created", "content": content_item}

    def update_content(self, content_id: str, updates: dict):
        content_list = self.tool_context.state.get('content', [])
        for item in content_list:
            if item["id"] == content_id:
                item.update(updates)
                return {"status": "Content updated", "content": item}
        return {"status": "Error", "message": "No content found to update"}

    def delete_content(self, content_id: str):
        content_list = self.tool_context.state.get('content', [])
        for i, item in enumerate(content_list):
            if item["id"] == content_id:
                deleted = content_list.pop(i)
                return {"status": "Content deleted", "content": deleted}
        return {"status": "Error", "message": "No content found to delete"}

    def get_content(self, content_id: str):
        content_list = self.tool_context.state.get('content', [])
        for item in content_list:
            if item["id"] == content_id:
                return {"status": "Content retrieved", "content": item}
        return {"status": "Error", "message": "No content found"}

    def process_request(self, request):
        action = request.get('action')
        if action == 'create_content':
            params = request.get('parameters', {})
            return self.create_content(params.get('title'), params.get('body'), params.get('tags'))
        elif action == 'update_content':
            params = request.get('parameters', {})
            return self.update_content(params.get('content_id'), params.get('updates', {}))
        elif action == 'delete_content':
            params = request.get('parameters', {})
            return self.delete_content(params.get('content_id'))
        elif action == 'retrieve_content':
            params = request.get('parameters', {})
            return self.get_content(params.get('content_id'))
        else:
            return {"status": "Error", "message": "Invalid action"}


class MultiAgentManager:
    def __init__(self):
        self.agents = {}

    def add_agent(self, agent_id, tool_context):
        self.agents[agent_id] = CMSAgent(tool_context)

    def process_request(self, agent_id, request):
        agent = self.agents.get(agent_id)
        if not agent:
            return {"status": "Error", "message": f"No agent found with id {agent_id}"}
        return agent.process_request(request)


# Example usage
# tool_context = ToolContext()  # This would be provided in the actual implementation
# cms_agent = CMSAgent(tool_context)
# response = cms_agent.process_request({'action': 'create', 'title': 'My Title', 'body': 'Content body'})
# print(response)

# manager = MultiAgentManager()
# manager.add_agent('agent1', ToolContext())
# response = manager.process_request('agent1', {'action': 'create', 'title': 'Title', 'body': 'Body'})
# print(response)