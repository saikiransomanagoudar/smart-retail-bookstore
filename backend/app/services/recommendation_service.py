import os
import random
from backend.app.services.graphql_service import graphql_service
from typing import List, Dict
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI

dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '.env'))
load_dotenv(dotenv_path)
opainai_api_key = os.getenv("OPENAI_API_KEY")
llm = OpenAI(api_key=opainai_api_key)

def generate_random_price():
    return round(random.uniform(9.00, 100.00), 2)

def extract_book_titles(generated_recommendations: str) -> List[str]:
    book_titles = []
    for line in generated_recommendations.splitlines():
        if line and line[0].isdigit() and ". " in line and " by " in line:
            title_with_author = line.split(" - ")[0].strip()
            title_with_author = title_with_author.split(". ", 1)[-1].strip()
            title = title_with_author.split(" by ")[0].strip()
            title = title.replace('"', '').strip()
            book_titles.append(title)
    return book_titles[:20]

def generate_llm_recommendations(preferences: dict) -> List[str]:
    prompt_template = PromptTemplate(
        input_variables=["favorite_books", "favorite_authors", "preferred_genres"],
        template="""
        Suggest 30 unique and popular book titles in various genres including {preferred_genres}.
        Consider the user's favorite books like {favorite_books} and authors like {favorite_authors}.
        Provide a brief description for each book.
        """
    )
    generated_recommendations = llm.invoke(prompt_template.format(
        favorite_books=", ".join(preferences.get("favorite_books", [])),
        favorite_authors=", ".join(preferences.get("favorite_authors", [])),
        preferred_genres=", ".join(preferences.get("preferred_genres", []))
    ))
    
    book_titles = extract_book_titles(generated_recommendations)
    return book_titles

async def get_recommendations(preferences: dict) -> List[Dict]:
    recommended_books = generate_llm_recommendations(preferences)
    book_details = await graphql_service.get_book_details_by_titles(recommended_books)
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
            "price": generate_random_price(),
        }
        recommendations.append(recommendation) 
    return recommendations

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
            "genres": book.get("dto_combined", []),
            "price": generate_random_price()
        }
        processed_books.append(processed_book)

    return processed_books
