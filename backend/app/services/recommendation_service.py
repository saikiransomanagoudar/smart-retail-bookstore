from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from backend.app.database.models import Book, Author, Rating
from backend.app.services.llm_service import generate_book_recommendations
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_book_details(db: Session, titles: List[str]) -> List[Dict]:
    logger.info(f"Searching for books with titles: {titles}")

    books = db.query(Book, Author, func.avg(Rating.rating).label('avg_rating'),
                     func.count(Rating.rating).label('rating_count')) \
        .join(Book.authors) \
        .outerjoin(Book.ratings) \
        .filter(or_(*[func.lower(Book.title).like(f"%{title.lower()}%") for title in titles])) \
        .group_by(Book.id, Author.id) \
        .all()

    logger.info(f"Found {len(books)} books in the database")

    results = []
    for book, author, avg_rating, rating_count in books:
        results.append({
            "title": book.title,
            "author": author.name,
            "publisher": book.publisher,
            "image_url": book.image_url,
            "rating": round(avg_rating, 1) if avg_rating else None,
            "rating_count": rating_count
        })

    return results


def get_initial_recommendations(db: Session, user_preferences: Dict) -> List[Dict]:
    recommended_titles = generate_book_recommendations(user_preferences)
    logger.info(f"LLM recommended {len(recommended_titles)} titles")

    book_details = get_book_details(db, recommended_titles)
    logger.info(f"Found details for {len(book_details)} books in the database")

    # Sort by rating and limit to 20 books
    sorted_books = sorted(book_details, key=lambda x: (x['rating'] or 0, x['rating_count'] or 0), reverse=True)
    final_recommendations = sorted_books[:20]

    # If we don't have 20 books, add some of the LLM recommendations that weren't found in the DB
    if len(final_recommendations) < 20:
        missing_titles = set(recommended_titles) - set(book['title'] for book in final_recommendations)
        for title in list(missing_titles)[:20 - len(final_recommendations)]:
            final_recommendations.append({
                "title": title,
                "author": "Unknown",
                "publisher": "Not found in database",
                "image_url": None,
                "rating": None,
                "rating_count": None
            })

    logger.info(f"Returning {len(final_recommendations)} final recommendations")
    return final_recommendations