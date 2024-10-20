from fastapi import FastAPI
from backend.app.api.recommendations import router as recommendations_router
from backend.app.api.chatbot import router as chatbot_router
from backend.app.core.config import settings
from backend.app.database.database import create_tables

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

create_tables()

app.include_router(recommendations_router, prefix="/api/recommendations", tags=["recommendations"])
app.include_router(chatbot_router, prefix="/api/chatbot", tags=["chatbot"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Book Recommendation System API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)