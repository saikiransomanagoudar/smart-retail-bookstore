import logging
import os
import random
import json
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user import get_user_preferences
from app.services.graphql_service import graphql_service
from typing import List, Dict
import re
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI

dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '.env'))
load_dotenv(dotenv_path)
openai_api_key = os.getenv("OPENAI_API_KEY")
llm = OpenAI(api_key=openai_api_key, temperature=0.7)

def normalize_title(title: str) -> str:
    return re.split(r':|–|-', title)[-1].strip()

def generate_random_price():
    return round(random.uniform(9.99, 29.99), 2)


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

        Return ONLY a valid JSON object containing 20 book recommendations in exactly this format:
        {{
            "recommendations": [
                {{
                    "title": "Example Title",
                    "author": "Author Name"
                }},
            ]
        }}

        Important rules:
        1. Return EXACTLY 20 recommendations
        2. Ensure complete, properly formatted JSON
        3. No additional text or explanations
        4. All brackets and braces must be properly closed"""
    )

    max_retries = 3
    for attempt in range(max_retries):
        try:
            generated_response = llm.invoke(
                prompt_template.format(
                    favorite_books=", ".join(favorite_books) if favorite_books else "various books",
                    favorite_authors=", ".join(favorite_authors) if favorite_authors else "various authors",
                    preferred_genres=", ".join(preferred_genres) if preferred_genres else "various genres"
                )
            )

            # Clean up the response
            cleaned_response = generated_response.strip()

            # Parse the JSON
            recommendations_data = json.loads(cleaned_response)
            recommendations = recommendations_data.get("recommendations", [])

            validated_recommendations = []
            for rec in recommendations:
                if all(key in rec for key in ["title", "author"]):
                    cleaned_rec = {
                        "title": rec["title"].strip(),
                        "author": rec["author"].strip()
                    }
                    validated_recommendations.append(cleaned_rec)

            if len(validated_recommendations) == 8:
                return validated_recommendations

            continue

        except json.JSONDecodeError as e:
            logging.error(f"Attempt {attempt + 1}: JSON parsing error: {e}")
            continue
        except Exception as e:
            logging.error(f"Attempt {attempt + 1}: Unexpected error: {e}")
            continue

    raise HTTPException(
        status_code=500,
        detail="Unable to generate valid recommendations after multiple attempts. Please try again."
    )

async def get_recommendations(user_id: str, db: Session) -> List[Dict]:
    user_preferences = get_user_preferences(user_id, db)

    if not user_preferences:
        import random
        random_ids = random.sample(range(1, 2000), 20)
        
        try:
            random_books = await graphql_service.get_book_details_by_ids(random_ids)
            processed_books = []
            for book in random_books:
                processed_book = {
                    "id": book.get("id"),
                    "title": book["title"],
                    "release_year": book.get("release_year"),
                    "release_date": book.get("release_date"),
                    "image_url": book.get("image_url", "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjQwMCIgdmlld0JveD0iMCAwIDMwMCA0MDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CiAgPGRlZnM+CiAgICA8bGluZWFyR3JhZGllbnQgaWQ9ImJnR3JhZGllbnQiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMTAwJSIgeTI9IjEwMCUiPgogICAgICA8c3RvcCBvZmZzZXQ9IjAlIiBzdHlsZT0ic3RvcC1jb2xvcjojNjY2Njk5O3N0b3Atb3BhY2l0eToxIiAvPgogICAgICA8c3RvcCBvZmZzZXQ9IjEwMCUiIHN0eWxlPSJzdG9wLWNvbG9yOiM5OTk5Y2M7c3RvcC1vcGFjaXR5OjEiIC8+CiAgICA8L2xpbmVhckdyYWRpZW50PgogICAgPGxpbmVhckdyYWRpZW50IGlkPSJib29rR3JhZGllbnQiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMTAwJSIgeTI9IjEwMCUiPgogICAgICA8c3RvcCBvZmZzZXQ9IjAlIiBzdHlsZT0ic3RvcC1jb2xvcjojNDA0NjhiO3N0b3Atb3BhY2l0eToxIiAvPgogICAgICA8c3RvcCBvZmZzZXQ9IjEwMCUiIHN0eWxlPSJzdG9wLWNvbG9yOiM2MjY2OWY7c3RvcC1vcGFjaXR5OjEiIC8+CiAgICA8L2xpbmVhckdyYWRpZW50PgogICAgPGZpbHRlciBpZD0iZHJvcFNoYWRvdyI+CiAgICAgIDxmZU9mZnNldCBkeD0iMyIgZHk9IjMiLz4KICAgICAgPGZlR2F1c3NpYW5CbHVyIHN0ZERldmlhdGlvbj0iMyIvPgogICAgICA8ZmVGbG9vZCBmbG9vZC1jb2xvcj0iIzAwMDAwMCIgZmxvb2Qtb3BhY2l0eT0iMC4zIi8+CiAgICAgIDxmZUNvbXBvc2l0ZSBvcGVyYXRvcj0ib3ZlciIvPgogICAgPC9maWx0ZXI+CiAgPC9kZWZzPgogIDxyZWN0IHdpZHRoPSIzMDAiIGhlaWdodD0iNDAwIiBmaWxsPSJ1cmwoI2JnR3JhZGllbnQpIi8+CiAgPGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoNzUsIDgwKSI+CiAgICA8IS0tIEJvb2sgQ292ZXIgLS0+CiAgICA8cmVjdCB4PSIwIiB5PSIwIiB3aWR0aD0iMTUwIiBoZWlnaHQ9IjI0MCIgZmlsbD0idXJsKCNib29rR3JhZGllbnQpIiByeD0iMTAiIGZpbHRlcj0idXJsKCNkcm9wU2hhZG93KSIvPgogICAgPCEtLSBCb29rIFNwaW5lIC0tPgogICAgPHJlY3QgeD0iNSIgeT0iMCIgd2lkdGg9IjEwIiBoZWlnaHQ9IjI0MCIgZmlsbD0iIzJkMzc0OCIgcng9IjIiLz4KICAgIDwhLS0gQm9vayBQYWdlcyAtLT4KICAgIDxyZWN0IHg9IjE1IiB5PSI4IiB3aWR0aD0iMTI1IiBoZWlnaHQ9IjIyNCIgZmlsbD0iI2Y4ZjlmYSIgcng9IjUiLz4KICAgIDwhLS0gVGV4dCBMaW5lcyAtLT4KICAgIDxyZWN0IHg9IjI1IiB5PSIzMCIgd2lkdGg9IjEwNSIgaGVpZ2h0PSI0IiBmaWxsPSIjZTBlNmVkIiByeD0iMiIvPgogICAgPHJlY3QgeD0iMjUiIHk9IjQ1IiB3aWR0aD0iODAiIGhlaWdodD0iNCIgZmlsbD0iI2UwZTZlZCIgcng9IjIiLz4KICAgIDxyZWN0IHg9IjI1IiB5PSI2MCIgd2lkdGg9Ijk1IiBoZWlnaHQ9IjQiIGZpbGw9IiNlMGU2ZWQiIHJ4PSIyIi8+CiAgICA8cmVjdCB4PSIyNSIgeT0iNzUiIHdpZHRoPSI3MCIgaGVpZ2h0PSI0IiBmaWxsPSIjZTBlNmVkIiByeD0iMiIvPgogICAgPHJlY3QgeD0iMjUiIHk9IjkwIiB3aWR0aD0iMTAwIiBoZWlnaHQ9IjQiIGZpbGw9IiNlMGU2ZWQiIHJ4PSIyIi8+CiAgICA8IS0tIEJvb2sgSWNvbiAtLT4KICAgIDxjaXJjbGUgY3g9Ijc1IiBjeT0iMTYwIiByPSIyNSIgZmlsbD0iIzQwNDY4YiIgb3BhY2l0eT0iMC4xIi8+CiAgICA8dGV4dCB4PSI3NSIgeT0iMTcwIiBmb250LWZhbWlseT0iU2Vnb2UgVUksIEFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjMwIiBmaWxsPSIjNDA0NjhiIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj7wn5OWPC90ZXh0PgogIDwvZz4KPC9zdmc+"),
                    "rating": book.get("rating"),
                    "pages": book.get("pages"),
                    "description": book.get("description", "No description available."),
                    "price": generate_random_price()
                }
                processed_books.append(processed_book)
            
            return processed_books
        except Exception as e:
            logging.error(f"Error getting random books: {e}")
            return []
    
    try:
        recommended_books = generate_llm_recommendations(user_preferences)
        if not recommended_books:
            import random
            random_ids = random.sample(range(1, 2000), 20)
            random_books = await graphql_service.get_book_details_by_ids(random_ids)
            
            processed_books = []
            for book in random_books:
                processed_book = {
                    "id": book.get("id"),
                    "title": book["title"],
                    "release_year": book.get("release_year"),
                    "release_date": book.get("release_date"),
                    "image_url": book.get("image_url", "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjQwMCIgdmlld0JveD0iMCAwIDMwMCA0MDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CiAgPGRlZnM+CiAgICA8bGluZWFyR3JhZGllbnQgaWQ9ImJnR3JhZGllbnQiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMTAwJSIgeTI9IjEwMCUiPgogICAgICA8c3RvcCBvZmZzZXQ9IjAlIiBzdHlsZT0ic3RvcC1jb2xvcjojNjY2Njk5O3N0b3Atb3BhY2l0eToxIiAvPgogICAgICA8c3RvcCBvZmZzZXQ9IjEwMCUiIHN0eWxlPSJzdG9wLWNvbG9yOiM5OTk5Y2M7c3RvcC1vcGFjaXR5OjEiIC8+CiAgICA8L2xpbmVhckdyYWRpZW50PgogICAgPGxpbmVhckdyYWRpZW50IGlkPSJib29rR3JhZGllbnQiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMTAwJSIgeTI9IjEwMCUiPgogICAgICA8c3RvcCBvZmZzZXQ9IjAlIiBzdHlsZT0ic3RvcC1jb2xvcjojNDA0NjhiO3N0b3Atb3BhY2l0eToxIiAvPgogICAgICA8c3RvcCBvZmZzZXQ9IjEwMCUiIHN0eWxlPSJzdG9wLWNvbG9yOiM2MjY2OWY7c3RvcC1vcGFjaXR5OjEiIC8+CiAgICA8L2xpbmVhckdyYWRpZW50PgogICAgPGZpbHRlciBpZD0iZHJvcFNoYWRvdyI+CiAgICAgIDxmZU9mZnNldCBkeD0iMyIgZHk9IjMiLz4KICAgICAgPGZlR2F1c3NpYW5CbHVyIHN0ZERldmlhdGlvbj0iMyIvPgogICAgICA8ZmVGbG9vZCBmbG9vZC1jb2xvcj0iIzAwMDAwMCIgZmxvb2Qtb3BhY2l0eT0iMC4zIi8+CiAgICAgIDxmZUNvbXBvc2l0ZSBvcGVyYXRvcj0ib3ZlciIvPgogICAgPC9maWx0ZXI+CiAgPC9kZWZzPgogIDxyZWN0IHdpZHRoPSIzMDAiIGhlaWdodD0iNDAwIiBmaWxsPSJ1cmwoI2JnR3JhZGllbnQpIi8+CiAgPGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoNzUsIDgwKSI+CiAgICA8IS0tIEJvb2sgQ292ZXIgLS0+CiAgICA8cmVjdCB4PSIwIiB5PSIwIiB3aWR0aD0iMTUwIiBoZWlnaHQ9IjI0MCIgZmlsbD0idXJsKCNib29rR3JhZGllbnQpIiByeD0iMTAiIGZpbHRlcj0idXJsKCNkcm9wU2hhZG93KSIvPgogICAgPCEtLSBCb29rIFNwaW5lIC0tPgogICAgPHJlY3QgeD0iNSIgeT0iMCIgd2lkdGg9IjEwIiBoZWlnaHQ9IjI0MCIgZmlsbD0iIzJkMzc0OCIgcng9IjIiLz4KICAgIDwhLS0gQm9vayBQYWdlcyAtLT4KICAgIDxyZWN0IHg9IjE1IiB5PSI4IiB3aWR0aD0iMTI1IiBoZWlnaHQ9IjIyNCIgZmlsbD0iI2Y4ZjlmYSIgcng9IjUiLz4KICAgIDwhLS0gVGV4dCBMaW5lcyAtLT4KICAgIDxyZWN0IHg9IjI1IiB5PSIzMCIgd2lkdGg9IjEwNSIgaGVpZ2h0PSI0IiBmaWxsPSIjZTBlNmVkIiByeD0iMiIvPgogICAgPHJlY3QgeD0iMjUiIHk9IjQ1IiB3aWR0aD0iODAiIGhlaWdodD0iNCIgZmlsbD0iI2UwZTZlZCIgcng9IjIiLz4KICAgIDxyZWN0IHg9IjI1IiB5PSI2MCIgd2lkdGg9Ijk1IiBoZWlnaHQ9IjQiIGZpbGw9IiNlMGU2ZWQiIHJ4PSIyIi8+CiAgICA8cmVjdCB4PSIyNSIgeT0iNzUiIHdpZHRoPSI3MCIgaGVpZ2h0PSI0IiBmaWxsPSIjZTBlNmVkIiByeD0iMiIvPgogICAgPHJlY3QgeD0iMjUiIHk9IjkwIiB3aWR0aD0iMTAwIiBoZWlnaHQ9IjQiIGZpbGw9IiNlMGU2ZWQiIHJ4PSIyIi8+CiAgICA8IS0tIEJvb2sgSWNvbiAtLT4KICAgIDxjaXJjbGUgY3g9Ijc1IiBjeT0iMTYwIiByPSIyNSIgZmlsbD0iIzQwNDY4YiIgb3BhY2l0eT0iMC4xIi8+CiAgICA8dGV4dCB4PSI3NSIgeT0iMTcwIiBmb250LWZhbWlseT0iU2Vnb2UgVUksIEFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjMwIiBmaWxsPSIjNDA0NjhiIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj7wn5OWPC90ZXh0PgogIDwvZz4KPC9zdmc+"),
                    "rating": book.get("rating"),
                    "pages": book.get("pages"),
                    "description": book.get("description", "No description available."),
                    "price": generate_random_price()
                }
                processed_books.append(processed_book)
            
            return processed_books

        processed_books = []
        
        for book in recommended_books:
            try:
                normalized_title = normalize_title(book['title'])
                book_details = await graphql_service.get_book_details_by_titles(normalized_title)
                if book_details:
                    b = book_details[0]
                    processed_book = {
                        "title": b["title"],
                        "release_year": b.get("release_year"),
                        "image_url": b.get("image_url", "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjQwMCIgdmlld0JveD0iMCAwIDMwMCA0MDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CiAgPGRlZnM+CiAgICA8bGluZWFyR3JhZGllbnQgaWQ9ImJnR3JhZGllbnQiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMTAwJSIgeTI9IjEwMCUiPgogICAgICA8c3RvcCBvZmZzZXQ9IjAlIiBzdHlsZT0ic3RvcC1jb2xvcjojNjY2Njk5O3N0b3Atb3BhY2l0eToxIiAvPgogICAgICA8c3RvcCBvZmZzZXQ9IjEwMCUiIHN0eWxlPSJzdG9wLWNvbG9yOiM5OTk5Y2M7c3RvcC1vcGFjaXR5OjEiIC8+CiAgICA8L2xpbmVhckdyYWRpZW50PgogICAgPGxpbmVhckdyYWRpZW50IGlkPSJib29rR3JhZGllbnQiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMTAwJSIgeTI9IjEwMCUiPgogICAgICA8c3RvcCBvZmZzZXQ9IjAlIiBzdHlsZT0ic3RvcC1jb2xvcjojNDA0NjhiO3N0b3Atb3BhY2l0eToxIiAvPgogICAgICA8c3RvcCBvZmZzZXQ9IjEwMCUiIHN0eWxlPSJzdG9wLWNvbG9yOiM2MjY2OWY7c3RvcC1vcGFjaXR5OjEiIC9+CiAgICA8L2xpbmVhckdyYWRpZW50PgogICAgPGZpbHRlciBpZD0iZHJvcFNoYWRvdyI+CiAgICAgIDxmZU9mZnNldCBkeD0iMyIgZHk9IjMiLz4KICAgICAgPGZlR2F1c3NpYW5CbHVyIHN0ZERldmlhdGlvbj0iMyIvPgogICAgICA8ZmVGbG9vZCBmbG9vZC1jb2xvcj0iIzAwMDAwMCIgZmxvb2Qtb3BhY2l0eT0iMC4zIi8+CiAgICAgIDxmZUNvbXBvc2l0ZSBvcGVyYXRvcj0ib3ZlciIvPgogICAgPC9maWx0ZXI+CiAgPC9kZWZzPgogIDxyZWN0IHdpZHRoPSIzMDAiIGhlaWdodD0iNDAwIiBmaWxsPSJ1cmwoI2JnR3JhZGllbnQpIi8+CiAgPGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoNzUsIDgwKSI+CiAgICA8IS0tIEJvb2sgQ292ZXIgLS0+CiAgICA8cmVjdCB4PSIwIiB5PSIwIiB3aWR0aD0iMTUwIiBoZWlnaHQ9IjI0MCIgZmlsbD0idXJsKCNib29rR3JhZGllbnQpIiByeD0iMTAiIGZpbHRlcj0idXJsKCNkcm9wU2hhZG93KSIvPgogICAgPCEtLSBCb29rIFNwaW5lIC0tPgogICAgPHJlY3QgeD0iNSIgeT0iMCIgd2lkdGg9IjEwIiBoZWlnaHQ9IjI0MCIgZmlsbD0iIzJkMzc0OCIgcng9IjIiLz4KICAgIDwhLS0gQm9vayBQYWdlcyAtLT4KICAgIDxyZWN0IHg9IjE1IiB5PSI4IiB3aWR0aD0iMTI1IiBoZWlnaHQ9IjIyNCIgZmlsbD0iI2Y4ZjlmYSIgcng9IjUiLz4KICAgIDwhLS0gVGV4dCBMaW5lcyAtLT4KICAgIDxyZWN0IHg9IjI1IiB5PSIzMCIgd2lkdGg9IjEwNSIgaGVpZ2h0PSI0IiBmaWxsPSIjZTBlNmVkIiByeD0iMiIvPgogICAgPHJlY3QgeD0iMjUiIHk9IjQ1IiB3aWR0aD0iODAiIGhlaWdodD0iNCIgZmlsbD0iI2UwZTZlZCIgcng9IjIiLz4KICAgIDxyZWN0IHg9IjI1IiB5PSI2MCIgd2lkdGg9Ijk1IiBoZWlnaHQ9IjQiIGZpbGw9IiNlMGU2ZWQiIHJ4PSIyIi8+CiAgICA8cmVjdCB4PSIyNSIgeT0iNzUiIHdpZHRoPSI3MCIgaGVpZ2h0PSI0IiBmaWxsPSIjZTBlNmVkIiByeD0iMiIvPgogICAgPHJlY3QgeD0iMjUiIHk9IjkwIiB3aWR0aD0iMTAwIiBoZWlnaHQ9IjQiIGZpbGw9IiNlMGU2ZWQiIHJ4PSIyIi8+CiAgICA8IS0tIEJvb2sgSWNvbiAtLT4KICAgIDxjaXJjbGUgY3g9Ijc1IiBjeT0iMTYwIiByPSIyNSIgZmlsbD0iIzQwNDY4YiIgb3BhY2l0eT0iMC4xIi8+CiAgICA8dGV4dCB4PSI3NSIgeT0iMTcwIiBmb250LWZhbWlseT0iU2Vnb2UgVUksIEFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjMwIiBmaWxsPSIjNDA0NjhiIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj7wn5OWPC90ZXh0PgogIDwvZz4KPC9zdmc+"),
                        "rating": b.get("rating"),
                        "pages": b.get("pages"),
                        "author": book["author"],
                        "price": generate_random_price(),
                        "description": b.get("description"),
                        "headline": b.get("headline")
                    }
                    processed_books.append(processed_book)
            except Exception as e:
                logging.error(f"Error processing book {book.get('title', 'Unknown')}: {e}")
                continue
        
        if processed_books:
            return processed_books
            
    except Exception as e:
        logging.error(f"Error in LLM recommendations: {e}")
    
    import random
    random_ids = random.sample(range(1, 2000), 20)
    try:
        random_books = await graphql_service.get_book_details_by_ids(random_ids)
        processed_books = []
        for book in random_books:
            processed_book = {
                "id": book.get("id"),
                "title": book["title"],
                "release_year": book.get("release_year"),
                "release_date": book.get("release_date"),
                "image_url": book.get("image_url", "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjQwMCIgdmlld0JveD0iMCAwIDMwMCA0MDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CiAgPGRlZnM+CiAgICA8bGluZWFyR3JhZGllbnQgaWQ9ImJnR3JhZGllbnQiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMTAwJSIgeTI9IjEwMCUiPgogICAgICA8c3RvcCBvZmZzZXQ9IjAlIiBzdHlsZT0ic3RvcC1jb2xvcjojNjY2Njk5O3N0b3Atb3BhY2l0eToxIiAvPgogICAgICA8c3RvcCBvZmZzZXQ9IjEwMCUiIHN0eWxlPSJzdG9wLWNvbG9yOiM5OTk5Y2M7c3RvcC1vcGFjaXR5OjEiIC8+CiAgICA8L2xpbmVhckdyYWRpZW50PgogICAgPGxpbmVhckdyYWRpZW50IGlkPSJib29rR3JhZGllbnQiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMTAwJSIgeTI9IjEwMCUiPgogICAgICA8c3RvcCBvZmZzZXQ9IjAlIiBzdHlsZT0ic3RvcC1jb2xvcjojNDA0NjhiO3N0b3Atb3BhY2l0eToxIiAvPgogICAgICA8c3RvcCBvZmZzZXQ9IjEwMCUiIHN0eWxlPSJzdG9wLWNvbG9yOiM2MjY2OWY7c3RvcC1vcGFjaXR5OjEiIC8+CiAgICA8L2xpbmVhckdyYWRpZW50PgogICAgPGZpbHRlciBpZD0iZHJvcFNoYWRvdyI+CiAgICAgIDxmZU9mZnNldCBkeD0iMyIgZHk9IjMiLz4KICAgICAgPGZlR2F1c3NpYW5CbHVyIHN0ZERldmlhdGlvbj0iMyIvPgogICAgICA8ZmVGbG9vZCBmbG9vZC1jb2xvcj0iIzAwMDAwMCIgZmxvb2Qtb3BhY2l0eT0iMC4zIi8+CiAgICAgIDxmZUNvbXBvc2l0ZSBvcGVyYXRvcj0ib3ZlciIvPgogICAgPC9maWx0ZXI+CiAgPC9kZWZzPgogIDxyZWN0IHdpZHRoPSIzMDAiIGhlaWdodD0iNDAwIiBmaWxsPSJ1cmwoI2JnR3JhZGllbnQpIi8+CiAgPGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoNzUsIDgwKSI+CiAgICA8IS0tIEJvb2sgQ292ZXIgLS0+CiAgICA8cmVjdCB4PSIwIiB5PSIwIiB3aWR0aD0iMTUwIiBoZWlnaHQ9IjI0MCIgZmlsbD0idXJsKCNib29rR3JhZGllbnQpIiByeD0iMTAiIGZpbHRlcj0idXJsKCNkcm9wU2hhZG93KSIvPgogICAgPCEtLSBCb29rIFNwaW5lIC0tPgogICAgPHJlY3QgeD0iNSIgeT0iMCIgd2lkdGg9IjEwIiBoZWlnaHQ9IjI0MCIgZmlsbD0iIzJkMzc0OCIgcng9IjIiLz4KICAgIDwhLS0gQm9vayBQYWdlcyAtLT4KICAgIDxyZWN0IHg9IjE1IiB5PSI4IiB3aWR0aD0iMTI1IiBoZWlnaHQ9IjIyNCIgZmlsbD0iI2Y4ZjlmYSIgcng9IjUiLz4KICAgIDwhLS0gVGV4dCBMaW5lcyAtLT4KICAgIDxyZWN0IHg9IjI1IiB5PSIzMCIgd2lkdGg9IjEwNSIgaGVpZ2h0PSI0IiBmaWxsPSIjZTBlNmVkIiByeD0iMiIvPgogICAgPHJlY3QgeD0iMjUiIHk9IjQ1IiB3aWR0aD0iODAiIGhlaWdodD0iNCIgZmlsbD0iI2UwZTZlZCIgcng9IjIiLz4KICAgIDxyZWN0IHg9IjI1IiB5PSI2MCIgd2lkdGg9Ijk1IiBoZWlnaHQ9IjQiIGZpbGw9IiNlMGU2ZWQiIHJ4PSIyIi8+CiAgICA8cmVjdCB4PSIyNSIgeT0iNzUiIHdpZHRoPSI3MCIgaGVpZ2h0PSI0IiBmaWxsPSIjZTBlNmVkIiByeD0iMiIvPgogICAgPHJlY3QgeD0iMjUiIHk9IjkwIiB3aWR0aD0iMTAwIiBoZWlnaHQ9IjQiIGZpbGw9IiNlMGU2ZWQiIHJ4PSIyIi8+CiAgICA8IS0tIEJvb2sgSWNvbiAtLT4KICAgIDxjaXJjbGUgY3g9Ijc1IiBjeT0iMTYwIiByPSIyNSIgZmlsbD0iIzQwNDY4YiIgb3BhY2l0eT0iMC4xIi8+CiAgICA8dGV4dCB4PSI3NSIgeT0iMTcwIiBmb250LWZhbWlseT0iU2Vnb2UgVUksIEFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjMwIiBmaWxsPSIjNDA0NjhiIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj7wn5OWPC90ZXh0PgogIDwvZz4KPC9zdmc+"),
                "rating": book.get("rating"),
                "pages": book.get("pages"),
                "description": book.get("description", "No description available."),
                "price": generate_random_price()
            }
            processed_books.append(processed_book)

    return processed_books
    except Exception as e:
        logging.error(f"Final fallback failed: {e}")
        return []


async def get_trending_books() -> List[Dict]:
    trending_ids = await graphql_service.get_trending_books_ids()

    if not trending_ids:
        raise HTTPException(
            status_code=404,
            detail="No trending books found"
        )

    trending_books = await graphql_service.get_book_details_by_ids(trending_ids)

    if not trending_books:
        raise HTTPException(
            status_code=404,
            detail="Could not fetch trending books details"
        )

    processed_books = []
    for book in trending_books:
        processed_book = {
            "id": book["id"],
            "title": book["title"],
            "release_year": book.get("release_year"),
            "release_date": book.get("release_date"),
            "image_url": book.get("image_url", "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjQwMCIgdmlld0JveD0iMCAwIDMwMCA0MDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CiAgPGRlZnM+CiAgICA8bGluZWFyR3JhZGllbnQgaWQ9ImJnR3JhZGllbnQiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMTAwJSIgeTI9IjEwMCUiPgogICAgICA8c3RvcCBvZmZzZXQ9IjAlIiBzdHlsZT0ic3RvcC1jb2xvcjojNjY2Njk5O3N0b3Atb3BhY2l0eToxIiAvPgogICAgICA8c3RvcCBvZmZzZXQ9IjEwMCUiIHN0eWxlPSJzdG9wLWNvbG9yOiM5OTk5Y2M7c3RvcC1vcGFjaXR5OjEiIC8+CiAgICA8L2xpbmVhckdyYWRpZW50PgogICAgPGxpbmVhckdyYWRpZW50IGlkPSJib29rR3JhZGllbnQiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMTAwJSIgeTI9IjEwMCUiPgogICAgICA8c3RvcCBvZmZzZXQ9IjAlIiBzdHlsZT0ic3RvcC1jb2xvcjojNDA0NjhiO3N0b3Atb3BhY2l0eToxIiAvPgogICAgICA8c3RvcCBvZmZzZXQ9IjEwMCUiIHN0eWxlPSJzdG9wLWNvbG9yOiM2MjY2OWY7c3RvcC1vcGFjaXR5OjEiIC8+CiAgICA8L2xpbmVhckdyYWRpZW50PgogICAgPGZpbHRlciBpZD0iZHJvcFNoYWRvdyI+CiAgICAgIDxmZU9mZnNldCBkeD0iMyIgZHk9IjMiLz4KICAgICAgPGZlR2F1c3NpYW5CbHVyIHN0ZERldmlhdGlvbj0iMyIvPgogICAgICA8ZmVGbG9vZCBmbG9vZC1jb2xvcj0iIzAwMDAwMCIgZmxvb2Qtb3BhY2l0eT0iMC4zIi8+CiAgICAgIDxmZUNvbXBvc2l0ZSBvcGVyYXRvcj0ib3ZlciIvPgogICAgPC9maWx0ZXI+CiAgPC9kZWZzPgogIDxyZWN0IHdpZHRoPSIzMDAiIGhlaWdodD0iNDAwIiBmaWxsPSJ1cmwoI2JnR3JhZGllbnQpIi8+CiAgPGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoNzUsIDgwKSI+CiAgICA8IS0tIEJvb2sgQ292ZXIgLS0+CiAgICA8cmVjdCB4PSIwIiB5PSIwIiB3aWR0aD0iMTUwIiBoZWlnaHQ9IjI0MCIgZmlsbD0idXJsKCNib29rR3JhZGllbnQpIiByeD0iMTAiIGZpbHRlcj0idXJsKCNkcm9wU2hhZG93KSIvPgogICAgPCEtLSBCb29rIFNwaW5lIC0tPgogICAgPHJlY3QgeD0iNSIgeT0iMCIgd2lkdGg9IjEwIiBoZWlnaHQ9IjI0MCIgZmlsbD0iIzJkMzc0OCIgcng9IjIiLz4KICAgIDwhLS0gQm9vayBQYWdlcyAtLT4KICAgIDxyZWN0IHg9IjE1IiB5PSI4IiB3aWR0aD0iMTI1IiBoZWlnaHQ9IjIyNCIgZmlsbD0iI2Y4ZjlmYSIgcng9IjUiLz4KICAgIDwhLS0gVGV4dCBMaW5lcyAtLT4KICAgIDxyZWN0IHg9IjI1IiB5PSIzMCIgd2lkdGg9IjEwNSIgaGVpZ2h0PSI0IiBmaWxsPSIjZTBlNmVkIiByeD0iMiIvPgogICAgPHJlY3QgeD0iMjUiIHk9IjQ1IiB3aWR0aD0iODAiIGhlaWdodD0iNCIgZmlsbD0iI2UwZTZlZCIgcng9IjIiLz4KICAgIDxyZWN0IHg9IjI1IiB5PSI2MCIgd2lkdGg9Ijk1IiBoZWlnaHQ9IjQiIGZpbGw9IiNlMGU2ZWQiIHJ4PSIyIi8+CiAgICA8cmVjdCB4PSIyNSIgeT0iNzUiIHdpZHRoPSI3MCIgaGVpZ2h0PSI0IiBmaWxsPSIjZTBlNmVkIiByeD0iMiIvPgogICAgPHJlY3QgeD0iMjUiIHk9IjkwIiB3aWR0aD0iMTAwIiBoZWlnaHQ9IjQiIGZpbGw9IiNlMGU2ZWQiIHJ4PSIyIi8+CiAgICA8IS0tIEJvb2sgSWNvbiAtLT4KICAgIDxjaXJjbGUgY3g9Ijc1IiBjeT0iMTYwIiByPSIyNSIgZmlsbD0iIzQwNDY4YiIgb3BhY2l0eT0iMC4xIi8+CiAgICA8dGV4dCB4PSI3NSIgeT0iMTcwIiBmb250LWZhbWlseT0iU2Vnb2UgVUksIEFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjMwIiBmaWxsPSIjNDA0NjhiIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj7wn5OWPC90ZXh0PgogIDwvZz4KPC9zdmc+"),
            "rating": book.get("rating"),
            "pages": book.get("pages"),
            "description": book.get("description", "No description available."),
            "price": generate_random_price()
        }
        processed_books.append(processed_book)

    return processed_books


async def get_genre_specific_books(genre: str, limit: int = 15, offset: int = 0) -> List[Dict]:
    """Get books specific to a genre using multiple search strategies"""
    try:
        recent_ids = await graphql_service.get_popular_books_by_year_range(2020, 2024, 30)
        
        classic_ids = await graphql_service.get_popular_books_by_year_range(2010, 2020, 30)
        
        all_ids = list(set(recent_ids + classic_ids))
        
        if all_ids:
            import random
            random.shuffle(all_ids)
            
            total_available = len(all_ids)
            start_idx = offset % total_available
            books_to_fetch = min(limit * 2, total_available)
            end_idx = min(start_idx + books_to_fetch, total_available)
            
            if end_idx - start_idx < books_to_fetch and start_idx > 0:
                selected_ids = all_ids[start_idx:] + all_ids[:books_to_fetch - (end_idx - start_idx)]
            else:
                selected_ids = all_ids[start_idx:end_idx]
            books = await graphql_service.get_book_details_by_ids(selected_ids)
            
            if books:
                processed_books = []
                for book in books[:limit]:
                    processed_book = {
                        "id": book.get("id"),
                        "title": book["title"],
                        "release_year": book.get("release_year"),
                        "release_date": book.get("release_date"),
                        "image_url": book.get("image_url", "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjQwMCIgdmlld0JveD0iMCAwIDMwMCA0MDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CiAgPGRlZnM+CiAgICA8bGluZWFyR3JhZGllbnQgaWQ9ImJnR3JhZGllbnQiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMTAwJSIgeTI9IjEwMCUiPgogICAgICA8c3RvcCBvZmZzZXQ9IjAlIiBzdHlsZT0ic3RvcC1jb2xvcjojNjY2Njk5O3N0b3Atb3BhY2l0eToxIiAvPgogICAgICA8c3RvcCBvZmZzZXQ9IjEwMCUiIHN0eWxlPSJzdG9wLWNvbG9yOiM5OTk5Y2M7c3RvcC1vcGFjaXR5OjEiIC8+CiAgICA8L2xpbmVhckdyYWRpZW50PgogICAgPGxpbmVhckdyYWRpZW50IGlkPSJib29rR3JhZGllbnQiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMTAwJSIgeTI9IjEwMCUiPgogICAgICA8c3RvcCBvZmZzZXQ9IjAlIiBzdHlsZT0ic3RvcC1jb2xvcjojNDA0NjhiO3N0b3Atb3BhY2l0eToxIiAvPgogICAgICA8c3RvcCBvZmZzZXQ9IjEwMCUiIHN0eWxlPSJzdG9wLWNvbG9yOiM2MjY2OWY7c3RvcC1vcGFjaXR5OjEiIC8+CiAgICA8L2xpbmVhckdyYWRpZW50PgogICAgPGZpbHRlciBpZD0iZHJvcFNoYWRvdyI+CiAgICAgIDxmZU9mZnNldCBkeD0iMyIgZHk9IjMiLz4KICAgICAgPGZlR2F1c3NpYW5CbHVyIHN0ZERldmlhdGlvbj0iMyIvPgogICAgICA8ZmVGbG9vZCBmbG9vZC1jb2xvcj0iIzAwMDAwMCIgZmxvb2Qtb3BhY2l0eT0iMC4zIi8+CiAgICAgIDxmZUNvbXBvc2l0ZSBvcGVyYXRvcj0ib3ZlciIvPgogICAgPC9maWx0ZXI+CiAgPC9kZWZzPgogIDxyZWN0IHdpZHRoPSIzMDAiIGhlaWdodD0iNDAwIiBmaWxsPSJ1cmwoI2JnR3JhZGllbnQpIi8+CiAgPGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoNzUsIDgwKSI+CiAgICA8IS0tIEJvb2sgQ292ZXIgLS0+CiAgICA8cmVjdCB4PSIwIiB5PSIwIiB3aWR0aD0iMTUwIiBoZWlnaHQ9IjI0MCIgZmlsbD0idXJsKCNib29rR3JhZGllbnQpIiByeD0iMTAiIGZpbHRlcj0idXJsKCNkcm9wU2hhZG93KSIvPgogICAgPCEtLSBCb29rIFNwaW5lIC0tPgogICAgPHJlY3QgeD0iNSIgeT0iMCIgd2lkdGg9IjEwIiBoZWlnaHQ9IjI0MCIgZmlsbD0iIzJkMzc0OCIgcng9IjIiLz4KICAgIDwhLS0gQm9vayBQYWdlcyAtLT4KICAgIDxyZWN0IHg9IjE1IiB5PSI4IiB3aWR0aD0iMTI1IiBoZWlnaHQ9IjIyNCIgZmlsbD0iI2Y4ZjlmYSIgcng9IjUiLz4KICAgIDwhLS0gVGV4dCBMaW5lcyAtLT4KICAgIDxyZWN0IHg9IjI1IiB5PSIzMCIgd2lkdGg9IjEwNSIgaGVpZ2h0PSI0IiBmaWxsPSIjZTBlNmVkIiByeD0iMiIvPgogICAgPHJlY3QgeD0iMjUiIHk9IjQ1IiB3aWR0aD0iODAiIGhlaWdodD0iNCIgZmlsbD0iI2UwZTZlZCIgcng9IjIiLz4KICAgIDxyZWN0IHg9IjI1IiB5PSI2MCIgd2lkdGg9Ijk1IiBoZWlnaHQ9IjQiIGZpbGw9IiNlMGU2ZWQiIHJ4PSIyIi8+CiAgICA8cmVjdCB4PSIyNSIgeT0iNzUiIHdpZHRoPSI3MCIgaGVpZ2h0PSI0IiBmaWxsPSIjZTBlNmVkIiByeD0iMiIvPgogICAgPHJlY3QgeD0iMjUiIHk9IjkwIiB3aWR0aD0iMTAwIiBoZWlnaHQ9IjQiIGZpbGw9IiNlMGU2ZWQiIHJ4PSIyIi8+CiAgICA8IS0tIEJvb2sgSWNvbiAtLT4KICAgIDxjaXJjbGUgY3g9Ijc1IiBjeT0iMTYwIiByPSIyNSIgZmlsbD0iIzQwNDY4YiIgb3BhY2l0eT0iMC4xIi8+CiAgICA8dGV4dCB4PSI3NSIgeT0iMTcwIiBmb250LWZhbWlseT0iU2Vnb2UgVUksIEFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjMwIiBmaWxsPSIjNDA0NjhiIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj7wn5OWPC90ZXh0PgogIDwvZz4KPC9zdmc+"),
                        "rating": book.get("rating"),
                        "pages": book.get("pages"),
                        "description": book.get("description", "No description available."),
                        "price": generate_random_price(),
                        "author": book.get("author", "Unknown Author")
                    }
                    processed_books.append(processed_book)
                
                return processed_books
                
    except Exception as e:
        pass
    
    return await get_trending_books()