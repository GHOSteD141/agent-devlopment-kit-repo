from datetime import datetime
from typing import List, Dict, Any, Optional
from google.adk.tools import ToolContext

def _get_next_id(tool_context: ToolContext) -> str:
    if "_next_content_id" not in tool_context.state:
        tool_context.state["_next_content_id"] = 1
    next_id = str(tool_context.state["_next_content_id"])
    tool_context.state["_next_content_id"] += 1
    return next_id


def create_content(title: str, body: str, tool_context: ToolContext, tags: Optional[List[str]] = None):
    """
    Create new content.

    Args:
        title: The title of the content.
        body: The body of the content.
        tool_context: The ADK tool context.
        tags: Optional; A list of tags associated with the content.

    Returns:
        A status message with the created content details.
    """
    if "content" not in tool_context.state:
        tool_context.state["content"] = []
    if tags is None:
        tags = []
    content = {
        "id": _get_next_id(tool_context),
        "title": title,
        "body": body,
        "tags": tags,
        "created_at": str(datetime.now())
    }
    tool_context.state["content"].append(content)
    return {"status": "Content created", "content": content}


def update_content(content_id: str, updates: Dict[str, Any], tool_context: ToolContext):
    """
    Update existing content.

    Args:
        content_id: The ID of the content to update.
        updates: A dictionary with the fields to update.
        tool_context: The ADK tool context.

    Returns:
        A status message indicating the result of the update.
    """
    content_list = tool_context.state.get("content", [])
    for item in content_list:
        if item["id"] == content_id:
            item.update(updates)
            return {"status": "Content updated", "content": item}
    return {"status": "Content not found"}


def delete_content(content_id: str, tool_context: ToolContext):
    """
    Delete existing content.

    Args:
        content_id: The ID of the content to delete.
        tool_context: The ADK tool context.

    Returns:
        A status message indicating the result of the deletion.
    """
    content_list = tool_context.state.get("content", [])
    for i, item in enumerate(content_list):
        if item["id"] == content_id:
            deleted_content = content_list.pop(i)
            return {"status": "Content deleted", "content": deleted_content}
    return {"status": "Content not found"}


def list_content(tool_context: ToolContext):
    """
    List all content.

    Args:
        tool_context: The ADK tool context.

    Returns:
        A list of all content stored in memory.
    """
    return {"content": tool_context.state.get("content", [])}