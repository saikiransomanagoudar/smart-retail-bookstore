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

def extract_book_titles_and_details(generated_recommendations: str) -> List[Dict[str, str]]:
    books = []
    for line in generated_recommendations.splitlines():
        if line and line[0].isdigit() and ". " in line and " by " in line:
            title_with_author = line.split(" - ")[0].strip()
            title_with_author = title_with_author.split(". ", 1)[-1].strip()
            title, author_description = title_with_author.split(" by ", 1)
            title = title.replace('"', '').strip()

            if ":" in author_description:
                author, description = author_description.split(":", 1)
                author = author.strip()
                description = description.strip()
            else:
                author = author_description.strip()
                description = "No description available."

            books.append({
                "title": title,
                "author": author,
                "description": description
            })
    return books[:20]

def generate_llm_recommendations(preferences: dict) -> List[Dict]:
    favorite_books = preferences.get("favorite_books", [])
    favorite_authors = preferences.get("favorite_authors", [])
    preferred_genres = preferences.get("preferred_genres", [])

    prompt_template = PromptTemplate(
        input_variables=["favorite_books", "favorite_authors", "preferred_genres"],
        template="""
        Suggest 30 unique and popular book titles in various genres including {preferred_genres}.
        Consider the user's favorite books like {favorite_books} and authors like {favorite_authors}.
        Provide a brief description for each book.
        Give the response in json format
        """
    )

    print(f"Favorite Books: {favorite_books}")
    print(f"Favorite Authors: {favorite_authors}")
    print(f"Preferred Genres: {preferred_genres}")

    generated_recommendations = llm.invoke(prompt_template.format(
        favorite_books=", ".join(favorite_books) if favorite_books else "various books",
        favorite_authors=", ".join(favorite_authors) if favorite_authors else "various authors",
        preferred_genres=", ".join(preferred_genres) if preferred_genres else "various genres"
    ))

    print(f"Generated Recommendations: {generated_recommendations}")

    book_details = extract_book_titles_and_details(generated_recommendations)
    return book_details


async def get_recommendations(preferences: dict) -> List[Dict]:
    recommended_books = generate_llm_recommendations(preferences)
    print(f"Recommended Books from LLM: {recommended_books}")

    book_titles = [book["title"] for book in recommended_books]
    book_details = await graphql_service.get_book_details_by_titles(book_titles)
    print(f"Book Details from GraphQL: {book_details}")
    
    recommendations = []
    for book_info in recommended_books:
        title = book_info["title"]
        author = book_info.get("author", "Unknown Author")
        description = book_info.get("description", "No description available.")

        matching_book = next((book for book in book_details if book['title'] == title), None)

        if matching_book:

            matching_book["author"] = author or matching_book.get("author", "Unknown Author")
            matching_book["description"] = description or matching_book.get("description", "No description available.")
        else:

            matching_book = {
                "id": 0,
                "title": title,
                "author": author,
                "description": description,
                "release_year": 0,
                "release_date": None,
                "image_url": None,
                "rating": 0.0,
                "pages": 0,
                "genres": ["Unknown Genre"],
                "price": generate_random_price()
            }
            print(f"Book not found in GraphQL, using fallback: {matching_book}")

        recommendations.append(matching_book)
    
    print(f"Final Recommendations: {recommendations}")
    return recommendations

async def get_trending_book() -> List[Dict]:
    trending_ids = await graphql_service.get_trending_books_ids()
    trending_books = await graphql_service.get_book_details_by_ids(trending_ids)

    processed_books = []
    for book in trending_books:
        processed_book = {
            "id": book["id"],
            "title": book["title"],
            "author": book.get("dto", {}).get("author", "Unknown Author"),
            "description": book.get("dto", {}).get("description", "No description available."),
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
