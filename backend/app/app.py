import os
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.api.recommendations import router as recommendations_router
from app.api.chatbot import router as chatbot_router
from app.core.config import settings
from app.database.database import create_tables

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

# Configure CORS for production
allowed_origins = [
    "http://localhost:3000",  # Local development
    "http://localhost:5173",  # Vite dev server
    "https://*.vercel.app",   # Vercel deployments
]

# Add production frontend URL if available
frontend_url = os.getenv("FRONTEND_URL")
if frontend_url:
    allowed_origins.append(frontend_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Initialize database tables on startup."""
    try:
        create_tables()
        print("✅ Database tables initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing database tables: {e}")

app.include_router(recommendations_router, prefix="/api/recommendations", tags=["recommendations"])
app.include_router(chatbot_router, prefix="/api/chatbot", tags=["chatbot"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Book Recommendation System API"}

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    try:
        # Test database connection
        from app.database.database import engine
        from sqlalchemy import text
        
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        
        return {
            "status": "healthy",
            "service": "Smart Retail Bookstore API",
            "version": settings.PROJECT_VERSION,
            "database": "connected"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "service": "Smart Retail Bookstore API",
            "version": settings.PROJECT_VERSION,
            "database": "disconnected",
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
