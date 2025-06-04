def create_content(title: str, body: str, tool_context: ToolContext):
    """
    Create new content.

    Args:
        title: The title of the content.
        body: The body of the content.
        tool_context: The ADK tool context.

    Returns:
        A status message with the created content details.
    """
    content = {
        "title": title,
        "body": body,
        "created_at": str(datetime.now())
    }
    tool_context.state["content"].append(content)
    return {"status": "Content created", "content": content}


def update_content(content_id: int, title: str, body: str, tool_context: ToolContext):
    """
    Update existing content.

    Args:
        content_id: The ID of the content to update.
        title: The new title of the content.
        body: The new body of the content.
        tool_context: The ADK tool context.

    Returns:
        A status message indicating the result of the update.
    """
    content_list = tool_context.state.get("content", [])
    if 0 <= content_id < len(content_list):
        content_list[content_id]["title"] = title
        content_list[content_id]["body"] = body
        return {"status": "Content updated", "content": content_list[content_id]}
    return {"status": "Content not found"}


def delete_content(content_id: int, tool_context: ToolContext):
    """
    Delete existing content.

    Args:
        content_id: The ID of the content to delete.
        tool_context: The ADK tool context.

    Returns:
        A status message indicating the result of the deletion.
    """
    content_list = tool_context.state.get("content", [])
    if 0 <= content_id < len(content_list):
        deleted_content = content_list.pop(content_id)
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