import os
import random
import json
from http.client import HTTPException
from requests import Session
from backend.app.models.user import get_user_preferences
from backend.app.services.graphql_service import graphql_service
from typing import List, Dict
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI

dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '.env'))
load_dotenv(dotenv_path)
openai_api_key = os.getenv("OPENAI_API_KEY")
llm = OpenAI(api_key=openai_api_key, temperature=0.7)


def generate_random_price():
    return round(random.uniform(9.00, 100.00), 2)


def generate_llm_recommendations(preferences: dict) -> List[Dict]:
    favorite_books = preferences.get("favorite_books", [])
    favorite_authors = preferences.get("favorite_authors", [])
    preferred_genres = preferences.get("preferred_genres", [])

    prompt_template = PromptTemplate(
        input_variables=["favorite_books", "favorite_authors", "preferred_genres"],
        template="""You are a book recommendation system. Based on these preferences:
        - Favorite Books: {favorite_books}
        - Favorite Authors: {favorite_authors}
        - Preferred Genres: {preferred_genres}

        Recommend exactly 20 books in this specific format, nothing more:
        {{
            "recommendations": [
                {{
                    "title": "Book Title",
                    "author": "Author Name",
                    "price": "15.99"
                }}
            ]
        }}

        Rules:
        1. Return ONLY valid JSON
        2. Include exactly 8 recommendations
        3. Keep descriptions very short
        4. Price should be between 9.99 and 29.99
        5. Must be complete, valid JSON
        """
    )

    try:
        generated_response = llm.invoke(
            prompt_template.format(
                favorite_books=", ".join(favorite_books) if favorite_books else "various books",
                favorite_authors=", ".join(favorite_authors) if favorite_authors else "various authors",
                preferred_genres=", ".join(preferred_genres) if preferred_genres else "various genres"
            ),
            max_tokens=2000,  # Limit response length
            temperature=0.7,
        )

        # Clean the response - remove any leading/trailing whitespace and newlines
        cleaned_response = generated_response.strip()

        try:
            # Parse JSON response
            recommendations_data = json.loads(cleaned_response)
            recommendations = recommendations_data.get("recommendations", [])

            # Validate each recommendation has required fields
            validated_recommendations = []
            for rec in recommendations:
                if all(key in rec for key in ["title", "author", "description"]):
                    validated_recommendations.append({
                        "title": rec["title"].strip(),
                        "author": rec["author"].strip(),
                        "description": rec["description"].strip()
                    })

            return validated_recommendations

        except json.JSONDecodeError as e:
            print(f"Error parsing LLM response as JSON: {e}")
            print(f"Raw response: {cleaned_response}")
            # Return an empty list instead of raising an exception
            return []

    except Exception as e:
        print(f"Error generating recommendations: {e}")
        return []


async def get_recommendations(user_id: str, db: Session) -> List[Dict]:
    user_preferences = await get_user_preferences(user_id, db)

    if not user_preferences:
        raise HTTPException(
            status_code=404,
            detail="User preferences not found. Please complete preferences setup."
        )

    recommended_books = generate_llm_recommendations(user_preferences)

    if not recommended_books:
        # Instead of raising an error, return trending books as fallback
        trending_books = await get_trending_book()
        return trending_books[:8]

    book_details = await graphql_service.get_book_details_by_titles(
        [book["title"] for book in recommended_books]
    )

    recommendations = []
    for book_info in recommended_books:
        title = book_info["title"]
        author = book_info["author"]
        description = book_info["description"]

        matching_book = next(
            (book for book in book_details if book['title'].lower() == title.lower()),
            None
        )

        if matching_book:
            matching_book.update({
                "author": author,
                "description": description,
                "price": generate_random_price()
            })
            recommendations.append(matching_book)
        else:
            recommendations.append({
                "id": len(recommendations),
                "title": title,
                "author": author,
                "description": description,
                "release_year": None,
                "release_date": None,
                "image_url": None,
                "rating": None,
                "pages": None,
                "genres": [],
                "price": generate_random_price()
            })

    return recommendations[:8]  # Ensure we return exactly 8 recommendations


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
            "image_url": book["images"][0]["url"] if book.get("images") else None,
            "rating": book.get("rating"),
            "pages": book.get("pages"),
            "description": book.get("description", "No description available."),
            "price": generate_random_price()
        }
        processed_books.append(processed_book)

    return processed_books