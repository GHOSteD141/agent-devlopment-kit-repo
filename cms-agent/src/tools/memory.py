"""Memory management for the CMS agent."""

from typing import Dict, Any, List
from google.adk.tools import ToolContext

def memorize_list(key: str, value: str, tool_context: ToolContext):
    """
    Memorize pieces of information in a list format.

    Args:
        key: The label indexing the memory to store the value.
        value: The information to be stored.
        tool_context: The ADK tool context.

    Returns:
        A status message.
    """
    mem_dict = tool_context.state
    if key not in mem_dict:
        mem_dict[key] = []
    if value not in mem_dict[key]:
        mem_dict[key].append(value)
    return {"status": f'Stored "{key}": "{value}"'}


def memorize(key: str, value: str, tool_context: ToolContext):
    """
    Memorize a single piece of information.

    Args:
        key: The label indexing the memory to store the value.
        value: The information to be stored.
        tool_context: The ADK tool context.

    Returns:
        A status message.
    """
    mem_dict = tool_context.state
    mem_dict[key] = value
    return {"status": f'Stored "{key}": "{value}"'}


def forget(key: str, value: str, tool_context: ToolContext):
    """
    Forget a piece of information.

    Args:
        key: The label indexing the memory to store the value.
        value: The information to be removed.
        tool_context: The ADK tool context.

    Returns:
        A status message.
    """
    if key not in tool_context.state:
        return {"status": f'Key "{key}" not found.'}
    
    if tool_context.state[key] is None:
        tool_context.state[key] = []
    
    if value in tool_context.state[key]:
        tool_context.state[key].remove(value)
        return {"status": f'Removed "{key}": "{value}"'}
    
    return {"status": f'Value "{value}" not found in "{key}".'}


def clear_memory(key: str, tool_context: ToolContext):
    """
    Clear all memory associated with a specific key.

    Args:
        key: The label indexing the memory to clear.
        tool_context: The ADK tool context.

    Returns:
        A status message.
    """
    if key in tool_context.state:
        del tool_context.state[key]
        return {"status": f'Cleared memory for key "{key}".'}
    
    return {"status": f'Key "{key}" not found to clear.'}