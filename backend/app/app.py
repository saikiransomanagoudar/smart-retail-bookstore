from fastapi import FastAPI
from backend.app.api import recommendations, users
from backend.app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

# app.include_router(recommendations.router, prefix="/api/recommendations", tags=["recommendations"])
# app.include_router(users.router, prefix="/api/users", tags=["users"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Book Recommendation System API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)