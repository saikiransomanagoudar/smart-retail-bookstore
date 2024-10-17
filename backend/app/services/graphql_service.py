from typing import List, Dict
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from backend.app.core.config import settings

class GraphQLService:
    def __init__(self, token: str):
        """
        Initialize the GraphQL service with the provided token and set up the AIOHTTP transport.
        """
        headers = {
            "Authorization": f"{token}"
        }
        transport = AIOHTTPTransport(url=settings.HARDCOVER_API_URL, headers=headers)
        self.client = Client(transport=transport, fetch_schema_from_transport=True)

    async def execute_query(self, query: str, variables: Dict = None) -> Dict:
        """
        Execute a GraphQL query asynchronously and return the result. If an error occurs, log the query, 
        variables, and error message.
        
        Args:
            query (str): The GraphQL query to execute.
            variables (Dict): Optional variables to pass to the query.

        Returns:
            Dict: The result of the query.
        """
        try:
            result = await self.client.execute_async(gql(query), variable_values=variables)
            print(f"GraphQL Response: {result}")
            return result
        except Exception as e:
            print(f"An error occurred while executing GraphQL query: {str(e)}")
            print(f"Query: {query}")
            if variables:
                print(f"Variables: {variables}")
            return {}

    async def get_trending_books_ids(self) -> List[int]:
        """
        Fetch the list of trending book IDs from the GraphQL service.
        
        Returns:
            List[int]: List of trending book IDs.
        """
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
        """
        Fetch detailed information about books using their IDs.

        Args:
            book_ids (List[int]): List of book IDs to fetch details for.

        Returns:
            List[Dict]: List of detailed book information.
        """
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
        """
        Fetch details of multiple books by querying each title individually and aggregating the results.

        Args:
            titles (List[str]): List of book titles to fetch details for.

        Returns:
            List[Dict]: List of detailed book information.
        """
        books = []
        # Query each book title one by one
        for title in titles:
            details = await self.get_book_details_by_title_chatbot(title)
            books.extend(details)
        return books

    async def get_book_details_by_title_chatbot(self, title: str) -> List[Dict]:
        """
        Fetch detailed information about a single book title, using an ilike search.

        Args:
            title (str): The title of the book to fetch details for.

        Returns:
            List[Dict]: List of detailed book information.
        """
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
                image {
                  url
                }
            }
        }
        """
        variables = {"title": title}
        result = await self.execute_query(query, variables)
        return result.get("books", [])

# Instantiate the GraphQLService with the token from the settings
graphql_service = GraphQLService(settings.HARDCOVER_API_TOKEN)
