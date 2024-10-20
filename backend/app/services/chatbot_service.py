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
import asyncpg

def normalize_title(title: str) -> str:
    return re.split(r':|–|-', title)[-1].strip()

class RecommendationAgent:
    def __init__(self, llm, memory):
        self.llm = llm
        self.memory = memory
        self.recommendation_provided = False
        self.conversation_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an AI assistant specializing in popular book recommendations. Your goal is to understand the user's preferences and provide personalized book recommendations. Follow these guidelines:

1. Ask one question at a time about the user's reading preferences. Focus on genres, themes, favorite authors, or recent books they enjoyed.
2. After the user has provided enough information (usually after 2-3 interactions), say 'Based on our conversation, I can now provide some book recommendations for you.'
3. Do not provide recommendations until explicitly instructed to do so.

Remember to keep the conversation natural and avoid repetitive questions."""),
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

    async def chat(self, user_input: str):
        if self.recommendation_provided:
            self.reset_state()

        response = await self.conversation.ainvoke({"input": user_input})
        self.memory.chat_memory.add_user_message(user_input)
        self.memory.chat_memory.add_ai_message(response)

        if "I can now provide some book recommendations for you" in response:
            recommendations = await self.recommend_books()
            self.recommendation_provided = True
            return {
                "type": "recommendation",
                "response": recommendations
            }
        else:
            return {
                "type": "question",
                "response": response
            }

    async def recommend_books(self) -> List[Dict[str, Any]]:
        chat_history = self.memory.chat_memory.messages
        conversation_summary = "\n".join([f"{msg.type}: {msg.content}" for msg in chat_history])
        logging.info(f"Conversation summary: {conversation_summary}")

        response = await self.conversation.ainvoke({
            "input": f"""Based on this conversation: 

    {conversation_summary} 

    Recommend 5 personalized popular books. Respond ONLY with a JSON array of objects. 
    Each object must have these keys: 
    - "Title": The book's full title (string) 
    - "ReasonForRecommendation": A brief explanation for the recommendation (string) 
    - "Price": Price in dollars (without currency symbols) 

    Return ONLY the JSON object, with no additional text, formatting, or characters."""
        })

        cleaned_response = response.strip().strip("```json").strip("```").strip()

        try:
            recommendations = json.loads(cleaned_response)
            if not isinstance(recommendations, list):
                raise ValueError("Response is not a JSON array")
        except (json.JSONDecodeError, ValueError) as e:
            logging.error(f"Failed to parse JSON or invalid format: {cleaned_response}")
            logging.error(f"Error: {str(e)}")
            return []

        processed_books = []
        for rec in recommendations:
            normalized_title = normalize_title(rec['Title'])
            book_details = await graphql_service.get_book_details_by_title_chatbot(normalized_title)
            if book_details:
                book = book_details[0]
                processed_book = {
                    "title": book["title"],
                    "release_year": book.get("release_year"),
                    "image_url": book["images"][0]["url"] if book.get("images") else (
                        book["image"]["url"] if book.get("image") else None),
                    "rating": book.get("rating"),
                    "pages": book.get("pages"),
                    "ReasonForRecommendation": rec["ReasonForRecommendation"],
                    "Price": rec["Price"]
                }
                processed_books.append(processed_book)
            else:
                logging.warning(f"No match found for book: {rec['Title']}")

        return processed_books

    def reset_state(self):
        self.memory.clear()
        self.recommendation_provided = False

class OrderPlacementAgent:
    def __init__(self, llm):
        self.llm = llm
        self.state = "INIT"
        self.order_data = {}

    async def process_order(self, user_input: str = None):
        if self.state == "INIT":
            self.state = "ASK_ADDRESS"
            return {
                "type": "order_question",
                "response": "Great! To place your order, I'll need some additional information. First, could you please provide your shipping address?"
            }
        elif self.state == "ASK_ADDRESS":
            self.order_data['address'] = user_input
            self.state = "ASK_PAYMENT"
            return {
                "type": "order_question",
                "response": "Thank you. Now, could you please provide your credit card information? Please enter the card number, expiration date, and CVV."
            }
        elif self.state == "ASK_PAYMENT":
            self.order_data['credit_card'] = user_input
            self.state = "CONFIRM"
            return await self.confirm_order()

    async def confirm_order(self):
        # Store order in PostgreSQL
        try:
            conn = await asyncpg.connect(user='your_username', password='your_password',
                                         database='your_database', host='your_host')

            order_id = await conn.fetchval(
                """
                INSERT INTO orders(title, price, address, credit_card)
                VALUES($1, $2, $3, $4)
                RETURNING id
                """,
                self.order_data['title'], self.order_data['Price'],
                self.order_data['address'], self.order_data['credit_card']
            )

            await conn.close()

            self.reset()
            return {
                "type": "order_confirmation",
                "response": f"Order placed successfully! Your order number is {order_id}."
            }
        except Exception as e:
            logging.error(f"Error storing order in database: {str(e)}")
            self.reset()
            return {
                "type": "error",
                "response": "There was an error processing your order. Please try again later."
            }

    def reset(self):
        self.state = "INIT"
        self.order_data = {}

class ChatbotService:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo")
        self.memory = ConversationBufferMemory(return_messages=True)
        self.recommendation_agent = RecommendationAgent(self.llm, self.memory)
        self.order_placement_agent = OrderPlacementAgent(self.llm)
        self.current_agent = "recommendation"

    async def chat(self, user_input: str):
        if self.current_agent == "recommendation":
            response = await self.recommendation_agent.chat(user_input)
            if response["type"] == "recommendation":
                self.current_agent = "order_placement"
            return response
        elif self.current_agent == "order_placement":
            response = await self.order_placement_agent.process_order(user_input)
            if response["type"] == "order_confirmation" or response["type"] == "error":
                self.current_agent = "recommendation"
            return response

    async def place_order(self, order_data: Dict[str, Any]):
        self.order_placement_agent.order_data = order_data
        self.current_agent = "order_placement"
        return await self.order_placement_agent.process_order()

chatbot_service = ChatbotService()