from sqlalchemy.orm import Session
from backend.app.database.database import Base
from sqlalchemy import Column, String, Text, Integer

class UserPreferences(Base):
    __tablename__ = "user_preferences"
    user_id = Column(Integer, primary_key=True, index=True)
    favorite_books = Column(Text)  
    favorite_authors = Column(Text)
    preferred_genres = Column(Text)
    themes_of_interest = Column(Text)
    reading_level = Column(String(50))

async def save_user_preferences(user_id: str, preferences: dict, db: Session):
    user_preferences = db.query(UserPreferences).filter(UserPreferences.user_id == user_id).first()

    if user_preferences:
        user_preferences.favorite_books = ', '.join(preferences.get("favorite_books", []))
        user_preferences.favorite_authors = ', '.join(preferences.get("favorite_authors", []))
        user_preferences.preferred_genres = ', '.join(preferences.get("preferred_genres", []))
        user_preferences.themes_of_interest = ', '.join(preferences.get("themes_of_interest", []))
        user_preferences.reading_level = preferences.get("reading_level", "")
    else:
        new_preferences = UserPreferences(
            user_id=user_id,
            favorite_books=', '.join(preferences.get("favorite_books", [])),
            favorite_authors=', '.join(preferences.get("favorite_authors", [])),
            preferred_genres=', '.join(preferences.get("preferred_genres", [])),
            themes_of_interest=', '.join(preferences.get("themes_of_interest", [])),
            reading_level=preferences.get("reading_level", "")
        )
        db.add(new_preferences)
    db.commit()

async def get_user_preferences(user_id: str, db: Session):
    try:
        user_preferences = db.query(UserPreferences).filter(UserPreferences.user_id == user_id).first()
        if user_preferences:
            return {
                "user_id": user_preferences.user_id,
                "favorite_books": user_preferences.favorite_books.split(', ') if user_preferences.favorite_books else [],
                "favorite_authors": user_preferences.favorite_authors.split(', ') if user_preferences.favorite_authors else [],
                "preferred_genres": user_preferences.preferred_genres.split(', ') if user_preferences.preferred_genres else [],
                "themes_of_interest": user_preferences.themes_of_interest.split(', ') if user_preferences.themes_of_interest else [],
                "reading_level": user_preferences.reading_level
            }
        else:
            return None
    except Exception as e:
        print(f"Error retrieving user preferences: {str(e)}")
        return None