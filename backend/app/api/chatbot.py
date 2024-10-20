import json

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse, JSONResponse
from backend.app.services.chatbot_service import chatbot_service
import asyncio

router = APIRouter()


@router.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data.get("message")

    async def event_generator():
        try:
            # Use chatbot_service to handle the chat logic
            response = await chatbot_service.chat(user_input)

            # If chatbot_service returns recommendations (as list), send a JSON response and stop SSE
            if isinstance(response, list):
                yield json.dumps(response)
            else:
                # Stream conversation response via SSE
                yield f"data: {response}\n\n"
                await asyncio.sleep(0.1)
                yield "data: [DONE]\n\n"

        except Exception as e:
            yield f"data: Error: {str(e)}\n\n"
            yield "data: [DONE]\n\n"

    # Check if recommendations are ready (handled by chatbot_service)
    response = await chatbot_service.chat(user_input)
    if isinstance(response, list):
        # Return JSON response for recommendations instead of SSE
        return JSONResponse(content=response)
    else:
        # If not recommendations, return SSE stream for chat conversation
        return StreamingResponse(event_generator(), media_type="text/event-stream")


@router.get("/health")
async def health_check():
    return JSONResponse(content={"status": "healthy"})
