
import logging
from fastapi import APIRouter, Request
import asyncio
from fastapi.responses import JSONResponse
from app.services.chatbot_service import ChatbotService
from app.services.utils import serialize_message
from langchain_core.messages import AIMessage

router = APIRouter()

# Initialize ChatbotService
chatbot_service = ChatbotService()

@router.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data.get("message")

    if not user_input:
        return JSONResponse(content={
            "type": "error",
            "response": "No message provided in the request."
        }, status_code=400)

    try:
        response = await chatbot_service.chat(user_input)

        
        if "recommendations" in response:
            recommendations = response["recommendations"]
            formatted_response = {
                "type": "recommendation",
                "response": recommendations,
                "next_node": response.get("next_node", "END"),
                "messages": [serialize_message(msg) for msg in response["messages"]]
            }
            return JSONResponse(content=formatted_response)
        
        if "messages" in response and response["messages"]:
            first_message = response["messages"][0]
            if isinstance(first_message, dict):
                message_content = first_message.get("content", "")
            else:
                serialized = serialize_message(first_message)
                message_content = serialized.get("content", "")
            
            formatted_response = {
                "type": "response",  # Default type
                "response": message_content,
                "next_node": response.get("next_node", "END"),
                "messages": [serialize_message(msg) for msg in response["messages"]]
            }
        else:
            formatted_response = {
                "type": "error",
                "response": "No response generated",
                "messages": []
            }
        
        return JSONResponse(content=formatted_response)
    except Exception as e:
        logging.error(f"Error in chat endpoint: {str(e)}")
        return JSONResponse(content={
            "type": "error",
            "response": f"An error occurred: {str(e)}"
        }, status_code=500)


@router.post("/place-order")
async def place_order(request: Request):
    data = await request.json()
    order_data = data.get("order_data")
    user_details = data.get("user_details")

    if not order_data or not user_details:
        return JSONResponse(content={
            "type": "error",
            "response": "Invalid input format. Please provide both cart (`order_data`) and user details (`user_details`)."
        }, status_code=400)

    try:
        combined_data = {
            "order_data": order_data,
            "user_details": user_details
        }
        response = chatbot_service.place_order(combined_data)
        return JSONResponse(content=response)
    except Exception as e:
        pass
        return JSONResponse(content={
            "type": "error",
            "response": f"An error occurred while placing the order: {str(e)}"
        }, status_code=500)

@router.get("/health")
async def health_check():
    return JSONResponse(content={"status": "healthy"})
