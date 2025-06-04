# File: cms-agent/cms-agent/src/agents/cms_agent.py

class CMSAgent:
    def __init__(self, tool_context):
        self.tool_context = tool_context

    def create_content(self, title: str, body: str):
        # Logic to create content
        self.tool_context.state['content'] = {'title': title, 'body': body}
        return {"status": "Content created", "content": self.tool_context.state['content']}

    def update_content(self, title: str, body: str):
        # Logic to update existing content
        if 'content' in self.tool_context.state:
            self.tool_context.state['content']['title'] = title
            self.tool_context.state['content']['body'] = body
            return {"status": "Content updated", "content": self.tool_context.state['content']}
        return {"status": "No content found to update"}

    def delete_content(self):
        # Logic to delete content
        if 'content' in self.tool_context.state:
            del self.tool_context.state['content']
            return {"status": "Content deleted"}
        return {"status": "No content found to delete"}

    def process_request(self, request):
        # Main logic to process incoming requests
        action = request.get('action')
        if action == 'create':
            return self.create_content(request.get('title'), request.get('body'))
        elif action == 'update':
            return self.update_content(request.get('title'), request.get('body'))
        elif action == 'delete':
            return self.delete_content()
        else:
            return {"status": "Invalid action"}

# Example usage
# tool_context = ToolContext()  # This would be provided in the actual implementation
# cms_agent = CMSAgent(tool_context)
# response = cms_agent.process_request({'action': 'create', 'title': 'My Title', 'body': 'Content body'})
# print(response)