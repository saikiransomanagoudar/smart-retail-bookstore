import random
from backend.app.services.graphql_service import graphql_service
from typing import List, Dict

def generate_random_price():
    """Helper function to generate a random price for books."""
    return round(random.uniform(9.00, 100.00), 2)

async def get_recommendations(user_preferences: dict) -> List[Dict]:
    """
    Fetch book recommendations based on user preferences such as favorite books, authors, and genres.
    
    Args:
        user_preferences (dict): User preferences such as favorite books, authors, and genres.

    Returns:
        List[Dict]: List of detailed book recommendations.
    """
    # Extract preferences
    favorite_books = user_preferences.get("favorite_books", [])
    favorite_authors = user_preferences.get("favorite_authors", [])
    preferred_genres = user_preferences.get("preferred_genres", [])

    # If no books are provided, use a default set of titles
    if not favorite_books:
        favorite_books = ["The Great Gatsby", "To Kill a Mockingbird"]  # Default titles

    # Fetch detailed book information from GraphQL API for each title
    book_details = await graphql_service.get_book_details_by_titles(favorite_books)

    # Return the list of book details (with some random pricing added)
    recommendations = []
    for book in book_details:
        recommendation = {
            "id": book["id"],
            "title": book["title"],
            "release_year": book.get("release_year"),
            "release_date": book.get("release_date"),
            "image_url": book["images"][0]["url"] if book.get("images") else None,
            "rating": book.get("rating"),
            "pages": book.get("pages"),
            "genres": book.get("dto_combined", []),
            "price": generate_random_price(),  # Add random price for demonstration
        }
        recommendations.append(recommendation)
    
    return recommendations


async def get_trending_books() -> List[Dict]:
    """
    Fetch the list of trending books from the GraphQL service.

    Returns:
        List[Dict]: List of trending books with detailed information.
    """
    # Fetch trending book IDs
    trending_ids = await graphql_service.get_trending_books_ids()
    
    # Fetch book details using the fetched trending IDs
    trending_books = await graphql_service.get_book_details_by_ids(trending_ids)

    # Process the trending books and return the detailed info
    processed_books = []
    for book in trending_books:
        processed_book = {
            "id": book["id"],
            "title": book["title"],
            "release_year": book.get("release_year"),
            "release_date": book.get("release_date"),
            "image_url": book["images"][0]["url"] if book.get("images") else None,
            "rating": book.get("rating"),
            "pages": book.get("pages"),
            "genres": book.get("dto_combined", []),
            "price": generate_random_price()  # Add random price for demonstration
        }
        processed_books.append(processed_book)
    
    return processed_books
