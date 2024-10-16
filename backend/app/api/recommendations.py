from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from backend.app.database.database import get_db
from backend.app.services.recommendation_service import get_recommendations, get_trending_book

router = APIRouter()

class UserPreferencesInput(BaseModel):
    favorite_book: List[str]
    favorite_authors: List[str]
    preferred_genres: List[str]
    themes_of_interest: List[str]
    reading_level: str

class BookRecommendation(BaseModel):
    id: int
    title: str
    release_year: Optional[int] = None
    release_date: Optional[str] = None
    image_url: Optional[str] = None
    rating: Optional[float] = None
    pages: Optional[int] = None
    genres: Optional[List[str]] = None
    price: float


@router.post("/initial-recommendations", response_model=List[BookRecommendation])
async def initial_recommendations(preferences: UserPreferencesInput, db: Session = Depends(get_db)):
    return ""

@router.post("/save-preferences")
async def save_preferences(preferences: UserPreferencesInput, user_id: str, db: Session = Depends(get_db)):
    return {"message": "Preferences saved successfully"}

@router.get("/trending-books", response_model=List[BookRecommendation])
async def get_trending_books():
    trending_books = await get_trending_book()
    return trending_books