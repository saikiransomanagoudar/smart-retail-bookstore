import random
from backend.app.services.graphql_service import graphql_service
from typing import List, Dict

def generate_random_price():
    return round(random.uniform(9.00, 100.00), 2)

async def get_recommendations(user_preferences: dict) -> list[dict]:
    # Your LLM logic to get recommended titles
    recommended_titles = ["The Great Gatsby", "To Kill a Mockingbird"]  # Example

    # Fetch detailed information about the recommended books
    book_details = await graphql_service.fetch_book_details(recommended_titles)
    print(book_details)
    return book_details


async def get_trending_book() -> List[Dict]:
    trending_ids = await graphql_service.get_trending_books_ids()
    trending_books = await graphql_service.get_book_details_by_ids(trending_ids)

    processed_books = []
    for book in trending_books:
        processed_book = {
            "id": book["id"],
            "title": book["title"],
            "release_year": book.get("release_year"),
            "release_date": book.get("release_date"),
            "image_url": book["images"][0]["url"] if book["images"] else None,
            "rating": book.get("rating"),
            "pages": book.get("pages"),
            "genres": book.get("dto_combined", []),
            "price": generate_random_price()
        }
        processed_books.append(processed_book)

    return processed_books