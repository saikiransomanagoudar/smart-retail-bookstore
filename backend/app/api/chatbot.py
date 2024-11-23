import logging
from fastapi import APIRouter, Request
import asyncio
from fastapi.responses import JSONResponse
from backend.app.services.chatbot_service import ChatbotService
from backend.app.services.utils import serialize_message
from langchain_core.messages import AIMessage

router = APIRouter()

# Initialize ChatbotService
chatbot_service = ChatbotService()

@router.post("/chat")
async def chat(request: Request):
    data = await request.json()
    logging.info(f"Received request data: {data}")
    user_input = data.get("message")

    if not user_input:
        return JSONResponse(content={
            "type": "error",
            "response": "No message provided in the request."
        }, status_code=400)

    try:
        if asyncio.iscoroutinefunction(chatbot_service.operator_agent.on_message):
            response = await chatbot_service.operator_agent.on_message(user_input)
        else:
            response = chatbot_service.operator_agent.on_message(user_input)

        # Serialize response messages
        response["messages"] = [
            serialize_message(msg) for msg in response["messages"]
        ]
        logging.info(f"Chatbot response: {response}")
        return JSONResponse(content=response)
    except Exception as e:
        logging.error(f"Error in /chat endpoint: {str(e)}")
        return JSONResponse(content={
            "type": "error",
            "response": f"An error occurred: {str(e)}"
        }, status_code=500)


@router.post("/place-order")
async def place_order(request: Request):
    """
    Endpoint to handle order placement.
    """
    data = await request.json()
    logging.info(f"Received order placement data: {data}")
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
        # Use ChatbotService's place_order method
        response = chatbot_service.place_order(combined_data)
        logging.info(f"Order placement response: {response}")
        return JSONResponse(content=response)
    except Exception as e:
        logging.error(f"Error in /place-order endpoint: {str(e)}")
        return JSONResponse(content={
            "type": "error",
            "response": f"An error occurred while placing the order: {str(e)}"
        }, status_code=500)

@router.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return JSONResponse(content={"status": "healthy"})
