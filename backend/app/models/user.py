from sqlalchemy.orm import Session
from backend.app.database.database import Base
from sqlalchemy import Column, String, Text, Integer

# Define the UserPreferences model
class UserPreferences(Base):
    __tablename__ = "user_preferences"
    user_id = Column(Integer, primary_key=True, index=True)
    favorite_books = Column(Text)  
    favorite_authors = Column(Text)
    preferred_genres = Column(Text)
    themes_of_interest = Column(Text)
    reading_level = Column(String(50))

# Function to save or update user preferences
async def save_user_preferences(user_id: str, preferences: dict, db: Session):
    # Check if preferences for this user already exist
    user_preferences = db.query(UserPreferences).filter(UserPreferences.user_id == user_id).first()

    if user_preferences:
        # Update existing preferences
        user_preferences.favorite_books = ','.join(preferences.get("favorite_books", []))
        user_preferences.favorite_authors = ','.join(preferences.get("favorite_authors", []))
        user_preferences.preferred_genres = ','.join(preferences.get("preferred_genres", []))
        user_preferences.themes_of_interest = ','.join(preferences.get("themes_of_interest", []))
        user_preferences.reading_level = preferences.get("reading_level", "")
    else:
        # Create new preferences
        new_preferences = UserPreferences(
            user_id=user_id,
            favorite_books=','.join(preferences.get("favorite_books", [])),
            favorite_authors=','.join(preferences.get("favorite_authors", [])),
            preferred_genres=','.join(preferences.get("preferred_genres", [])),
            themes_of_interest=','.join(preferences.get("themes_of_interest", [])),
            reading_level=preferences.get("reading_level", "")
        )
        db.add(new_preferences)
    
    # Commit the transaction
    db.commit()
