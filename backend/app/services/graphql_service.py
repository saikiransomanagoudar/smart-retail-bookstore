from typing import List, Dict
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from backend.app.core.config import settings
import asyncio


class GraphQLService:
    def __init__(self, token: str):
        self.token = token
        self.url = settings.HARDCOVER_API_URL
        self._lock = asyncio.Lock()

    async def execute_query(self, query: str, variables: Dict = None) -> Dict:
        async with self._lock:
            try:
                transport = AIOHTTPTransport(
                    url=self.url,
                    headers={
                        "Authorization": self.token,
                        "Content-Type": "application/json"
                    },
                    timeout=60
                )
                async with Client(
                        transport=transport,
                        fetch_schema_from_transport=False
                ) as session:
                    result = await session.execute(gql(query), variable_values=variables)
                    return result
            except Exception as e:
                return {}

    def extract_author_from_dto(self, book: Dict) -> None:
        dto = book.get("dto")
        if dto and isinstance(dto, dict):
            author = dto.get("author")
            if author:
                book["author"] = author
            else:
                book["author"] = "Unknown Author"
        else:
            book["author"] = "Unknown Author"

    async def get_trending_books_ids(self) -> List[int]:
        query = """
        query GetTrendingBooks {
            books_trending(from: "2024-01-01", to: "2024-12-31", limit: 50, offset: 0) {
                ids
            }
        }
        """
        try:
            result = await self.execute_query(query)
            trending_ids = result.get("books_trending", {}).get("ids", [])
            if trending_ids:
                return trending_ids
        except Exception:
            pass
        
        import random
        return random.sample(range(1, 5000), 50)

    async def get_book_details_by_ids(self, book_ids: List[int]) -> List[Dict]:
        query = """
        query MyQuery($ids: [Int!]!) {
            books(where: {id: {_in: $ids}}, distinct_on: title) {
                id
                title
                release_year
                release_date
                images(limit: 1, where: {url: {_is_null: false}}) {
                    url
                }
                rating
                pages
                description
            }
        }
        """
        variables = {"ids": book_ids}
        result = await self.execute_query(query, variables)
        books = result.get("books", [])
 
        for book in books:
            if not book.get("images") or not book["images"]:
                book["image_url"] = "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjQwMCIgdmlld0JveD0iMCAwIDMwMCA0MDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CiAgPGRlZnM+CiAgICA8bGluZWFyR3JhZGllbnQgaWQ9ImJnR3JhZGllbnQiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMTAwJSIgeTI9IjEwMCUiPgogICAgICA8c3RvcCBvZmZzZXQ9IjAlIiBzdHlsZT0ic3RvcC1jb2xvcjojNjY2Njk5O3N0b3Atb3BhY2l0eToxIiAvPgogICAgICA8c3RvcCBvZmZzZXQ9IjEwMCUiIHN0eWxlPSJzdG9wLWNvbG9yOiM5OTk5Y2M7c3RvcC1vcGFjaXR5OjEiIC8+CiAgICA8L2xpbmVhckdyYWRpZW50PgogICAgPGxpbmVhckdyYWRpZW50IGlkPSJib29rR3JhZGllbnQiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMTAwJSIgeTI9IjEwMCUiPgogICAgICA8c3RvcCBvZmZzZXQ9IjAlIiBzdHlsZT0ic3RvcC1jb2xvcjojNDA0NjhiO3N0b3Atb3BhY2l0eToxIiAvPgogICAgICA8c3RvcCBvZmZzZXQ9IjEwMCUiIHN0eWxlPSJzdG9wLWNvbG9yOiM2MjY2OWY7c3RvcC1vcGFjaXR5OjEiIC8+CiAgICA8L2xpbmVhckdyYWRpZW50PgogICAgPGZpbHRlciBpZD0iZHJvcFNoYWRvdyI+CiAgICAgIDxmZU9mZnNldCBkeD0iMyIgZHk9IjMiLz4KICAgICAgPGZlR2F1c3NpYW5CbHVyIHN0ZERldmlhdGlvbj0iMyIvPgogICAgICA8ZmVGbG9vZCBmbG9vZC1jb2xvcj0iIzAwMDAwMCIgZmxvb2Qtb3BhY2l0eT0iMC4zIi8+CiAgICAgIDxmZUNvbXBvc2l0ZSBvcGVyYXRvcj0ib3ZlciIvPgogICAgPC9maWx0ZXI+CiAgPC9kZWZzPgogIDxyZWN0IHdpZHRoPSIzMDAiIGhlaWdodD0iNDAwIiBmaWxsPSJ1cmwoI2JnR3JhZGllbnQpIi8+CiAgPGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoNzUsIDgwKSI+CiAgICA8IS0tIEJvb2sgQ292ZXIgLS0+CiAgICA8cmVjdCB4PSIwIiB5PSIwIiB3aWR0aD0iMTUwIiBoZWlnaHQ9IjI0MCIgZmlsbD0idXJsKCNib29rR3JhZGllbnQpIiByeD0iMTAiIGZpbHRlcj0idXJsKCNkcm9wU2hhZG93KSIvPgogICAgPCEtLSBCb29rIFNwaW5lIC0tPgogICAgPHJlY3QgeD0iNSIgeT0iMCIgd2lkdGg9IjEwIiBoZWlnaHQ9IjI0MCIgZmlsbD0iIzJkMzc0OCIgcng9IjIiLz4KICAgIDwhLS0gQm9vayBQYWdlcyAtLT4KICAgIDxyZWN0IHg9IjE1IiB5PSI4IiB3aWR0aD0iMTI1IiBoZWlnaHQ9IjIyNCIgZmlsbD0iI2Y4ZjlmYSIgcng9IjUiLz4KICAgIDwhLS0gVGV4dCBMaW5lcyAtLT4KICAgIDxyZWN0IHg9IjI1IiB5PSIzMCIgd2lkdGg9IjEwNSIgaGVpZ2h0PSI0IiBmaWxsPSIjZTBlNmVkIiByeD0iMiIvPgogICAgPHJlY3QgeD0iMjUiIHk9IjQ1IiB3aWR0aD0iODAiIGhlaWdodD0iNCIgZmlsbD0iI2UwZTZlZCIgcng9IjIiLz4KICAgIDxyZWN0IHg9IjI1IiB5PSI2MCIgd2lkdGg9Ijk1IiBoZWlnaHQ9IjQiIGZpbGw9IiNlMGU2ZWQiIHJ4PSIyIi8+CiAgICA8cmVjdCB4PSIyNSIgeT0iNzUiIHdpZHRoPSI3MCIgaGVpZ2h0PSI0IiBmaWxsPSIjZTBlNmVkIiByeD0iMiIvPgogICAgPHJlY3QgeD0iMjUiIHk9IjkwIiB3aWR0aD0iMTAwIiBoZWlnaHQ9IjQiIGZpbGw9IiNlMGU2ZWQiIHJ4PSIyIi8+CiAgICA8IS0tIEJvb2sgSWNvbiAtLT4KICAgIDxjaXJjbGUgY3g9Ijc1IiBjeT0iMTYwIiByPSIyNSIgZmlsbD0iIzQwNDY4YiIgb3BhY2l0eT0iMC4xIi8+CiAgICA8dGV4dCB4PSI3NSIgeT0iMTcwIiBmb250LWZhbWlseT0iU2Vnb2UgVUksIEFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjMwIiBmaWxsPSIjNDA0NjhiIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj7wn5OWPC90ZXh0PgogIDwvZz4KPC9zdmc+"
            else:
                book["image_url"] = book["images"][0]["url"]
        
        return books

    async def get_book_details_by_titles(self, title: str) -> List[Dict]:

        query = """
        query MyQuery($title: String!) {
            books(where: {title: {_ilike: $title}, image_id: {_is_null: false}}) {
                id
                title
                release_year
                release_date
                rating
                pages
                images(limit: 1, where: {url: {_is_null: false}}) {
                  url
                }
                image {
                  url
                }
                description
                headline
            }
        }
        """
        variables = {"title": title}
        result = await self.execute_query(query, variables)
        books = result.get("books", [])

        for book in books:
            self.extract_author_from_dto(book)
            # Add fallback image
            if not book.get("images") or not book["images"]:
                if book.get("image") and book["image"].get("url"):
                    book["image_url"] = book["image"]["url"]
                else:
                    book["image_url"] = "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjQwMCIgdmlld0JveD0iMCAwIDMwMCA0MDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CiAgPGRlZnM+CiAgICA8bGluZWFyR3JhZGllbnQgaWQ9ImJnR3JhZGllbnQiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMTAwJSIgeTI9IjEwMCUiPgogICAgICA8c3RvcCBvZmZzZXQ9IjAlIiBzdHlsZT0ic3RvcC1jb2xvcjojNjY2Njk5O3N0b3Atb3BhY2l0eToxIiAvPgogICAgICA8c3RvcCBvZmZzZXQ9IjEwMCUiIHN0eWxlPSJzdG9wLWNvbG9yOiM5OTk5Y2M7c3RvcC1vcGFjaXR5OjEiIC8+CiAgICA8L2xpbmVhckdyYWRpZW50PgogICAgPGxpbmVhckdyYWRpZW50IGlkPSJib29rR3JhZGllbnQiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMTAwJSIgeTI9IjEwMCUiPgogICAgICA8c3RvcCBvZmZzZXQ9IjAlIiBzdHlsZT0ic3RvcC1jb2xvcjojNDA0NjhiO3N0b3Atb3BhY2l0eToxIiAvPgogICAgICA8c3RvcCBvZmZzZXQ9IjEwMCUiIHN0eWxlPSJzdG9wLWNvbG9yOiM2MjY2OWY7c3RvcC1vcGFjaXR5OjEiIC8+CiAgICA8L2xpbmVhckdyYWRpZW50PgogICAgPGZpbHRlciBpZD0iZHJvcFNoYWRvdyI+CiAgICAgIDxmZU9mZnNldCBkeD0iMyIgZHk9IjMiLz4KICAgICAgPGZlR2F1c3NpYW5CbHVyIHN0ZERldmlhdGlvbj0iMyIvPgogICAgICA8ZmVGbG9vZCBmbG9vZC1jb2xvcj0iIzAwMDAwMCIgZmxvb2Qtb3BhY2l0eT0iMC4zIi8+CiAgICAgIDxmZUNvbXBvc2l0ZSBvcGVyYXRvcj0ib3ZlciIvPgogICAgPC9maWx0ZXI+CiAgPC9kZWZzPgogIDxyZWN0IHdpZHRoPSIzMDAiIGhlaWdodD0iNDAwIiBmaWxsPSJ1cmwoI2JnR3JhZGllbnQpIi8+CiAgPGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoNzUsIDgwKSI+CiAgICA8IS0tIEJvb2sgQ292ZXIgLS0+CiAgICA8cmVjdCB4PSIwIiB5PSIwIiB3aWR0aD0iMTUwIiBoZWlnaHQ9IjI0MCIgZmlsbD0idXJsKCNib29rR3JhZGllbnQpIiByeD0iMTAiIGZpbHRlcj0idXJsKCNkcm9wU2hhZG93KSIvPgogICAgPCEtLSBCb29rIFNwaW5lIC0tPgogICAgPHJlY3QgeD0iNSIgeT0iMCIgd2lkdGg9IjEwIiBoZWlnaHQ9IjI0MCIgZmlsbD0iIzJkMzc0OCIgcng9IjIiLz4KICAgIDwhLS0gQm9vayBQYWdlcyAtLT4KICAgIDxyZWN0IHg9IjE1IiB5PSI4IiB3aWR0aD0iMTI1IiBoZWlnaHQ9IjIyNCIgZmlsbD0iI2Y4ZjlmYSIgcng9IjUiLz4KICAgIDwhLS0gVGV4dCBMaW5lcyAtLT4KICAgIDxyZWN0IHg9IjI1IiB5PSIzMCIgd2lkdGg9IjEwNSIgaGVpZ2h0PSI0IiBmaWxsPSIjZTBlNmVkIiByeD0iMiIvPgogICAgPHJlY3QgeD0iMjUiIHk9IjQ1IiB3aWR0aD0iODAiIGhlaWdodD0iNCIgZmlsbD0iI2UwZTZlZCIgcng9IjIiLz4KICAgIDxyZWN0IHg9IjI1IiB5PSI2MCIgd2lkdGg9Ijk1IiBoZWlnaHQ9IjQiIGZpbGw9IiNlMGU2ZWQiIHJ4PSIyIi8+CiAgICA8cmVjdCB4PSIyNSIgeT0iNzUiIHdpZHRoPSI3MCIgaGVpZ2h0PSI0IiBmaWxsPSIjZTBlNmVkIiByeD0iMiIvPgogICAgPHJlY3QgeD0iMjUiIHk9IjkwIiB3aWR0aD0iMTAwIiBoZWlnaHQ9IjQiIGZpbGw9IiNlMGU2ZWQiIHJ4PSIyIi8+CiAgICA8IS0tIEJvb2sgSWNvbiAtLT4KICAgIDxjaXJjbGUgY3g9Ijc1IiBjeT0iMTYwIiByPSIyNSIgZmlsbD0iIzQwNDY4YiIgb3BhY2l0eT0iMC4xIi8+CiAgICA8dGV4dCB4PSI3NSIgeT0iMTcwIiBmb250LWZhbWlseT0iU2Vnb2UgVUksIEFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjMwIiBmaWxsPSIjNDA0NjhiIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj7wn5OWPC90ZXh0PgogIDwvZz4KPC9zdmc+"
            else:
                book["image_url"] = book["images"][0]["url"]
        return books

    async def get_book_details_by_title_chatbot(self, title: str) -> List[Dict]:
        query = """
        query MyQuery($title: String!) {
            books(where: {title: {_ilike: $title, _is_null: false}}, limit: 1) {
                title
                release_year
                pages
                images(limit: 1, where: {url: {_is_null: false}}) {
                  url
                }
                image{
                  url
                }
            }
        }
        """
        variables = {"title": title}
        result = await self.execute_query(query, variables)
        books = result.get("books", [])

        for book in books:
            self.extract_author_from_dto(book)
        return books


    async def get_books_by_genre_search(self, genre_terms: List[str], limit: int = 20) -> List[int]:
        search_queries = []
        for term in genre_terms:
            query = f"""
            query SearchBooks {{
                books(where: {{
                    _or: [
                        {{description: {{_ilike: "%{term}%"}}}},
                        {{title: {{_ilike: "%{term}%"}}}}
                    ],
                    image_id: {{_is_null: false}}
                }}, limit: {limit//len(genre_terms)}) {{
                    id
                }}
            }}
            """
            try:
                result = await self.execute_query(query)
                books = result.get("books", [])
                search_queries.extend([book["id"] for book in books])
            except Exception:
                continue
        
        return search_queries[:limit] if search_queries else []

    async def get_popular_books_by_year_range(self, start_year: int, end_year: int, limit: int = 30) -> List[int]:
        query = f"""
        query GetPopularBooks {{
            books(where: {{
                release_year: {{_gte: {start_year}, _lte: {end_year}}},
                rating: {{_gte: 3.5}},
                image_id: {{_is_null: false}}
            }}, order_by: {{rating: desc}}, limit: {limit}) {{
                id
            }}
        }}
        """
        try:
            result = await self.execute_query(query)
            books = result.get("books", [])
            return [book["id"] for book in books]
        except Exception:
            return []

graphql_service = GraphQLService(settings.HARDCOVER_API_TOKEN)