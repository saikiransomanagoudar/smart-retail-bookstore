from langchain_core.messages import AIMessage, HumanMessage

def serialize_message(message):
    """
    Serialize a message object (AIMessage or HumanMessage) into a JSON-compatible format.
    """
    if isinstance(message, AIMessage):
        return {"type": "ai", "content": message.content}
    elif isinstance(message, HumanMessage):
        return {"type": "human", "content": message.content}
    return {"type": "unknown", "content": str(message)}
