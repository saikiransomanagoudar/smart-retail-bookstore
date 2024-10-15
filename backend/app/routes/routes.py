from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional

from sqlalchemy.sql.sqltypes import NULLTYPE

from backend.app.database.database import get_db
from backend.app.models import UserPreference
from backend.app.services.recommendation_service import get_initial_recommendations

router = APIRouter()

class UserPreferencesInput(BaseModel):
    favorite_book: List[str]
    favorite_authors: List[str]
    preferred_genres: List[str]
    themes_of_interest: List[str]
    reading_level: str

class BookRecommendation(BaseModel):
    title: str
    author: str
    publisher: Optional[str]
    image_url: Optional[str]
    rating: Optional[float]
    rating_count: Optional[int]

#returns 20 initial recommendations based on user preference
@router.post("/initial-recommendations", response_model=List[BookRecommendation])
def initial_recommendations(preferences: UserPreferencesInput, db: Session = Depends(get_db)):

    return ""


@router.post("/save-preferences")
def save_preferences(preferences: UserPreferencesInput, user_id: str, db: Session = Depends(get_db)):

    return {"message": "Preferences saved successfully"}