from typing import List, Dict
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from backend.app.core.config import settings

class GraphQLService:
    def __init__(self, token: str):
        headers = {
            "Authorization": f"{token}"
        }
        transport = AIOHTTPTransport(url=settings.HARDCOVER_API_URL, headers=headers)
        self.client = Client(transport=transport, fetch_schema_from_transport=True)

    async def execute_query(self, query: str, variables: Dict = None) -> Dict:
        try:
            result = await self.client.execute_async(gql(query), variable_values=variables)
            return result
        except Exception as e:
            print(f"An error occurred while executing GraphQL query: {str(e)}")
            return {}

    async def get_trending_books_ids(self) -> List[int]:
        query = """
        query GetTrendingBooks {
            books_trending(from: "2010-01-01", limit: 20, offset: 10) {
                ids
            }
        }
        """
        result = await self.execute_query(query)
        return result.get("books_trending", {}).get("ids", [])

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
                dto
                dto_combined(path: "genres")
            }
        }
        """
        variables = {"ids": book_ids}
        result = await self.execute_query(query, variables)
        return result.get("books", [])

    async def get_book_details_by_titles(self, titles: List[str]) -> List[Dict]:
        query = """
        query MyQuery($titles: [String!]!) {
            books(where: {
                title: {_in: $titles},
                release_year: {_is_null: false}, 
                dto_combined: {_is_null: false}
            }, distinct_on: title) {
                id
                title
                release_year
                release_date
                images(limit: 1, where: {url: {_is_null: false}}) {
                    url
                }
                rating
                pages
                dto
                dto_combined(path: "genres")
            }
        }
        """
        variables = {"titles": titles}
        result = await self.execute_query(query, variables)
        return result.get("books", [])

    async def get_book_details_by_title_chatbot(self, title: str) -> List[Dict]:
        query = """
        query MyQuery($title: String!) {
            books(where: {title: {_ilike: $title, _is_null: false}}, limit: 1) {
                id
                title
                release_year
                release_date
                images(limit: 1, where: {url: {_is_null: false}}) {
                  url
                }
                rating
                description
                headline
                image{
                  url
                }
            }
        }
        """
        variables = {"title": title}
        result = await self.execute_query(query, variables)
        return result.get("books", [])

graphql_service = GraphQLService(settings.HARDCOVER_API_TOKEN)
