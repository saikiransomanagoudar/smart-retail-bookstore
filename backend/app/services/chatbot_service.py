import logging
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables import RunnablePassthrough
from backend.app.services.graphql_service import graphql_service
import json
import re

def normalize_title(title: str) -> str:
    return re.split(r':|–|-', title)[-1].strip()

class ChatbotService:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo")
        self.memory = ConversationBufferMemory(return_messages=True)

        self.conversation_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an AI assistant specializing in book recommendations. Your initial goal is to gather detailed preferences from the user by asking targeted questions. Please adhere to these guidelines:

1. Ask 3-4 well-structured questions, one at a time, regarding the user's reading habits. Focus on genres, themes, authors, or recent favorites.
2. During this phase, **do not** offer any book recommendations.
3. After 3-4 questions, conclude with: 'Based on our conversation, I'm ready to provide some book recommendations for you.'
4. Wait for explicit user instructions before recommending any books.

Your priority is to gather information, not recommend books at this stage.
Remember, accuracy in book titles is crucial for our system to find the correct book from API."""),

            ("human", "{input}"),
            ("ai", "{agent_scratchpad}")
        ])

        self.conversation = (
            RunnablePassthrough.assign(
                agent_scratchpad=lambda x: self.memory.chat_memory.messages
            )
            | self.conversation_prompt
            | self.llm
            | StrOutputParser()
        )

        self.recommendation_state = {
            "questions_asked": 0,
            "preferences": {},
            "recommendation_provided": False
        }

    async def recommend_books(self) -> List[Dict[str, Any]]:
        chat_history = self.memory.chat_memory.messages
        conversation_summary = "\n".join([f"{msg.type}: {msg.content}" for msg in chat_history])
        logging.info(f"Conversation summary: {conversation_summary}")

        response = await self.conversation.ainvoke({
            "input": f"""Here is the user's reading preference summary based on our previous conversation:

    {conversation_summary}

    Provide 5 personalized book recommendations based on the user’s preferences. Ensure the response is in JSON format as a **single JSON array** with the following keys for each book:
    - 'Title': The full and accurate title of the book
    - 'ReasonForRecommendation': A concise explanation of why this book matches the user's preferences

    Ensure all books are included inside a single JSON array."""
        })

        # Strip out any code blocks, then clean and parse the JSON
        clean_response = re.sub(r'```json\s*|\s*```', '', response).strip()

        try:
            # Parse the response as a JSON array
            recommendations = json.loads(clean_response)
            if not isinstance(recommendations, list):
                raise ValueError("Response is not a JSON array")
        except (json.JSONDecodeError, ValueError) as e:
            logging.error(f"Failed to parse JSON or invalid format: {clean_response}")
            logging.error(f"Error: {str(e)}")
            return []

        processed_books = []
        for rec in recommendations:
            normalized_title = normalize_title(rec['Title'])
            logging.info(f"Searching for book: {normalized_title}")
            book_details = await graphql_service.get_book_details_by_title_chatbot(normalized_title)
            if book_details:
                book = book_details[0]
                processed_book = {
                    "id": book["id"],
                    "title": book["title"],
                    "release_year": book.get("release_year"),
                    "release_date": book.get("release_date"),
                    "image_url": book["images"][0]["url"] if book["images"] else None,
                    "rating": book.get("rating"),
                    "pages": book.get("pages"),
                    "genres": book.get("dto_combined", []),
                    "ReasonForRecommendation": rec["ReasonForRecommendation"]
                }
                processed_books.append(processed_book)
            else:
                logging.warning(f"No match found for book: {rec['Title']}")

        return processed_books

    async def chat(self, user_input: str):
        if self.recommendation_state["recommendation_provided"]:
            # Reset the state for a new conversation
            self.recommendation_state = {
                "questions_asked": 0,
                "preferences": {},
                "recommendation_provided": False
            }
            self.memory.clear()
            return "Hello! I'd be happy to help you find some new books to read. What kind of books do you usually enjoy?"

        response = await self.conversation.ainvoke({"input": user_input})
        self.memory.chat_memory.add_user_message(user_input)
        self.memory.chat_memory.add_ai_message(response)

        if "Based on our conversation, I'm ready to provide some book recommendations for you." in response:
            self.recommendation_state["questions_asked"] += 1
            if self.recommendation_state["questions_asked"] >= 3:
                recommendations = await self.recommend_books()
                self.recommendation_state["recommendation_provided"] = True
                return recommendations
            else:
                return response
        else:
            self.recommendation_state["questions_asked"] += 1
            self.recommendation_state["preferences"][f"preference_{self.recommendation_state['questions_asked']}"] = user_input
            return response

chatbot_service = ChatbotService()
