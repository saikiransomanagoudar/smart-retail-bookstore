from typing import Tuple
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

from backend.app.models.orders import Order
from backend.app.services.graphql_service import graphql_service

from typing import List, Dict, Any
from datetime import datetime, timedelta
import logging
import re
import json

logging.basicConfig(level=logging.INFO)

def normalize_title(title: str) -> str:
    return re.split(r":|–|-", title)[-1].strip()

class RecommendationAgent:
    def __init__(self, llm, memory):
        self.llm = llm
        self.memory = memory
        self.recommendation_provided = False
        self.ready_for_recommendations = False
        self.recommended_books = set()
        self.question_count = 0
        self.MIN_QUESTIONS = 4  # Increased to 4 questions before recommendations
        self.out_of_context_count = 0

        # Separate prompts for conversation and recommendations
        self.conversation_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are an AI assistant specializing in book recommendations. Your goal is to understand the user's preferences and provide personalized book recommendations. Follow these guidelines:

                    1. You MUST ask at least 4 questions before making recommendations. Track the following key areas:
                    - Preferred genres and themes
                    - Specific interests within genres
                    - Reading experience level
                    - Previous books they enjoyed or disliked
                    2. Avoid repetitive questions, and try to gather comprehensive information quickly.
                    3. Once you have enough context, you can proceed with providing recommendations.
                    4. Keep the conversation natural and avoid excessive follow-up questions.
                    5. If a user provides multiple pieces of information in one response, proceed to recommendations if sufficient details are covered.""",
                ),
                ("human", "{input}"),
                ("ai", "{agent_scratchpad}"),
            ]
        )

        self.recommendation_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are a book recommendation specialist. Generate recommendations based on the provided conversation history. Follow these rules strictly:
                    1. NEVER include author names in book titles
                    2. NEVER use "by" or "written by" in titles
                    3. Return ONLY the exact book title as it appears on the cover
                    4. Ensure recommendations are diverse within the user's interests
                    5. Format output as a valid JSON array
                    6. DO NOT recommend any books from the provided exclusion list
                    7. Focus especially on the most recent preferences and feedback provided by the user""",
                ),
                ("human", "{input}"),
            ]
        )

        self.conversation = (
            RunnablePassthrough.assign(
                agent_scratchpad=lambda x: self.memory.chat_memory.messages
            )
            | self.conversation_prompt
            | self.llm
            | StrOutputParser()
        )

        self.recommendation_chain = (
            self.recommendation_prompt | self.llm | StrOutputParser()
        )

    async def chat(self, user_input: str):
        if user_input.lower() == "quit":
            self.reset_state()
            return {"type": "system", "response": "Conversation reset."}

        if self.is_out_of_context(user_input):
            self.out_of_context_count += 1
            if self.out_of_context_count == 1:
                response = "I'm here to help you with book recommendations and information about books. Please ask something related to books."
            elif self.out_of_context_count == 2:
                response = "Remember, I’m your book assistant. How can I assist you with book recommendations or book-related information?"
            else:
                response = "It seems we're off track. Let's get back to discussing books! Please ask me anything about book recommendations or book-related topics."
            return {"type": "system", "response": response}

        self.out_of_context_count = 0

        feedback_keywords = [
            "don't recommend", "don't like", "didn't like", "not good",
            "bad recommendations", "poor suggestions", "stop recommendations"
        ]
        if self.recommendation_provided and any(phrase in user_input.lower() for phrase in feedback_keywords):
            self.recommendation_provided = False
            self.ready_for_recommendations = False
            self.question_count = max(2, self.question_count)  # Reset to ask at least 2 more questions for clarity

            response = await self.conversation.ainvoke({
                "input": f"It seems you weren't satisfied with the previous recommendations. Could you tell me more about your preferences or specific genres, authors, or themes you're interested in? This will help me improve my suggestions."
            })
            self.memory.chat_memory.add_user_message(user_input)
            self.memory.chat_memory.add_ai_message(response)
            return {"type": "question", "response": response}

        # Continue with regular conversation flow if no feedback or out-of-context issue is detected
        response = await self.conversation.ainvoke({"input": user_input})
        self.memory.chat_memory.add_user_message(user_input)
        self.memory.chat_memory.add_ai_message(response)

        if self.check_readiness(response):
            self.ready_for_recommendations = True
            recommendations = await self.recommend_books()
            self.recommendation_provided = True
            return {"type": "recommendation", "response": recommendations}

        # Increment question count for building context
        if "?" in response and not self.ready_for_recommendations:
            self.question_count += 1

        return {"type": "question", "response": response}

    def is_out_of_context(self, user_input: str) -> bool:
        """Determine if the user's question is out of context."""
        out_of_context_keywords = [
            "weather", "news", "joke", "recipe", "food", "sports", "politics", 
            "movies", "games", "unrelated topic", "non-book related"
        ]
        return any(keyword in user_input.lower() for keyword in out_of_context_keywords)

    def check_readiness(self, response: str) -> bool:
        """
        Determines if enough context is gathered to provide recommendations.
        Either based on the number of questions asked or the quality of responses.
        """
        sufficient_context = self.question_count >= self.MIN_QUESTIONS
        detailed_response = len(self.memory.chat_memory.messages) > 3

        # Additional condition to ask about sub-genres or reading level if genre is given
        if "genre" in response.lower() and self.question_count < self.MIN_QUESTIONS:
            self.ask_follow_up_questions(response)

        return sufficient_context or detailed_response

    def ask_follow_up_questions(self, response: str):
        """
        Adds follow-up questions based on user-provided information.
        """
        if "genre" in response.lower() and self.question_count < self.MIN_QUESTIONS:
            # Follow-up question about specific types within the chosen genre
            follow_up_question = (
                "What specific type within this genre do you enjoy reading?"
            )
            self.memory.chat_memory.add_ai_message(follow_up_question)
            self.question_count += 1

        if self.question_count == 3:
            # Follow-up question about reading level
            follow_up_question = "What is your preferred reading level? Beginner, Intermediate, or Advanced?"
            self.memory.chat_memory.add_ai_message(follow_up_question)
            self.question_count += 1
    
    def is_out_of_context(self, user_input: str) -> bool:
        """Determine if the user's question is out of context."""
        out_of_context_keywords = [
            "weather", "news", "joke", "recipe", "food", "sports", "politics", 
            "movies", "games", "unrelated topic", "non-book related"
        ]
        return any(keyword in user_input.lower() for keyword in out_of_context_keywords)


    async def recommend_books(self) -> List[Dict[str, Any]]:
        if not self.ready_for_recommendations:
            return []

        chat_history = self.memory.chat_memory.messages
        conversation_summary = "\n".join(
            [f"{msg.type}: {msg.content}" for msg in chat_history]
        )

        try:
            previously_recommended = "\n".join(self.recommended_books)
            response = await self.recommendation_chain.ainvoke(
                {
                    "input": f"""Based on this conversation: 

                    {conversation_summary}

                    DO NOT recommend any of these previously recommended books:
                    {previously_recommended}

                    Recommend 5 personalized books. Respond ONLY with a JSON array of objects. 
                    Each object must have these keys: 
                    - "Title": The book's full title (string) [X DO NOT ADD AUTHORS NAME]
                    - "ReasonForRecommendation": A brief explanation for the recommendation (string) 
                    - "Price": Price in dollars (without currency symbols) 

                    Return ONLY the JSON object, with no additional text, formatting, or characters."""
                }
            )

            cleaned_response = response.strip().strip("```json").strip("```").strip()
            recommendations = json.loads(cleaned_response)

            if not isinstance(recommendations, list):
                raise ValueError("Response is not a JSON array")

            processed_books = []
            for rec in recommendations:
                normalized_title = normalize_title(rec["Title"])

                if normalized_title in self.recommended_books:
                    continue

                book_details = await graphql_service.get_book_details_by_title_chatbot(
                    normalized_title
                )

                if book_details:
                    book = book_details[0]
                    processed_book = {
                        "title": book["title"],
                        "release_year": book.get("release_year"),
                        "image_url": (
                            book["images"][0]["url"]
                            if book.get("images")
                            else (book["image"]["url"] if book.get("image") else None)
                        ),
                        "rating": book.get("rating"),
                        "pages": book.get("pages"),
                        "ReasonForRecommendation": rec["ReasonForRecommendation"],
                        "Price": rec["Price"],
                    }
                    self.recommended_books.add(normalized_title)
                    processed_books.append(processed_book)
                else:
                    logging.warning(f"No match found for book: {rec['Title']}")

            return processed_books

        except Exception as e:
            logging.error(f"Error generating recommendations: {str(e)}")
            return []

    def reset_state(self):
        self.memory.clear()
        self.recommendation_provided = False
        self.ready_for_recommendations = False
        self.recommended_books.clear()
        self.question_count = 0  # Reset question counter

class OrderPlacementAgent:
    def __init__(self, llm):
        self.llm = llm
        self.state = "INIT"
        self.order_data = {}
        self.cart_items = []

    async def process_order(self, user_input: Any = None):
        try:
            logging.info(f"Full input data received: {user_input}")

            if not isinstance(user_input, dict):
                logging.error("User input is not a dictionary")
                return {
                    "type": "error",
                    "response": "Invalid input format. Please provide order data and user details.",
                }

            # Extract order_data and user_details from input
            order_data = user_input.get("order_data")
            user_details = user_input.get("user_details")

            if not order_data or not user_details:
                logging.error("Missing required data")
                return {
                    "type": "error",
                    "response": "Missing required order information. Please provide both order data and user details.",
                }

            # Only process order if the state is "INIT"
            if self.state != "INIT":
                logging.error("Order placement called in invalid state.")
                return {
                    "type": "error",
                    "response": "Invalid order state. Please try again.",
                }

            # Set up the order information
            self.cart_items = order_data
            self.order_data = user_details

            # Validate order_data and user_details presence
            if not order_data or not user_details:
                logging.error(
                    f"Missing required data. order_data: {bool(order_data)}, user_details: {bool(user_details)}"
                )
                return {
                    "type": "error",
                    "response": "Missing required order information. Please provide both order data and user details.",
                }

            # Process the order if the agent is in the INIT state
            if self.state == "INIT":
                # Validate cart items format
                if not isinstance(order_data, list):
                    logging.error("Cart items are not in a list format")
                    return {
                        "type": "error",
                        "response": "Invalid cart data format. Please try again.",
                    }

                # Validate user details fields
                required_fields = ["name", "address", "cardNumber", "expiryDate", "cvv"]
                missing_fields = [
                    field for field in required_fields if field not in user_details
                ]
                if missing_fields:
                    logging.error(f"Missing fields in user details: {missing_fields}")
                    return {
                        "type": "error",
                        "response": f"Missing fields in user details: {', '.join(missing_fields)}.",
                    }

                # Validate card details
                if (
                    len(user_details["cardNumber"]) != 16
                    or not user_details["cardNumber"].isdigit()
                ):
                    return {
                        "type": "error",
                        "response": "Card number must be 16 digits.",
                    }
                if not re.match(r"^\d{2}/\d{2}$", user_details["expiryDate"]):
                    return {
                        "type": "error",
                        "response": "Expiry date must be in MM/YY format.",
                    }
                if (
                    len(user_details["cvv"]) != 3
                    or not user_details["cvv"].isdigit()
                ):
                    return {"type": "error", "response": "CVV must be 3 digits."}

                # Calculate total cost
                total_cost = sum(
                    float(item.get("Price", 0)) * item.get("quantity", 1)
                    for item in order_data
                )

                # Create order confirmation response
                order_confirmation = {
                "order_id": f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "total_cost": f"{total_cost:.2f}",
                "order_placed_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "expected_delivery": (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"),
                "status": "success",
                "message": "Your order has been successfully placed. Thank you for shopping with us!",
            }

            # Log success and reset state
            logging.info("Order placed successfully, transitioning to COMPLETE state.")
            self.state = "COMPLETE"

            # Reset state for the next order
            self.reset()

            return {"type": "order_confirmation", "response": order_confirmation}

        except Exception as e:
            logging.error(f"Error processing order: {str(e)}")
            self.reset()
            return {
                "type": "error",
                "response": "Sorry, there was an error processing your order. Please try again.",
            }

    def reset(self):
        """Reset the agent state"""
        self.state = "INIT"
        self.order_data = {}
        self.cart_items = []


class ChatbotService:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0.7, model_name="gpt-4o-mini")
        self.memory = ConversationBufferMemory(return_messages=True)
        self.recommendation_agent = RecommendationAgent(self.llm, self.memory)
        self.order_placement_agent = OrderPlacementAgent(self.llm)
        self.current_agent = "recommendation"
        self.greeting_message = "Welcome! I'm BookWorm, your virtual assistant. I’m here to help you browse and find the perfect book for your collection. Ready to start exploring?"
        self.first_interaction = True
    async def chat(self, user_input: str):
        if user_input.lower() == "clear":
            self.reset_first_interaction()
            self.memory.clear()  # Clear all chat memory
            return {"type": "system", "response": "Chat reset. How can I assist you with books today?"}
    
    async def chat(self, user_input: str):
        if self.first_interaction:
            self.first_interaction = False
            return {"type": "greeting", "response": self.greeting_message}

        if user_input.lower() == "hi" and not self.first_interaction:
            return {
                "type": "question",
                "response": "What genres or themes do you typically enjoy reading?",
            }

        if self.current_agent == "recommendation":
            if not self.memory.chat_memory.messages:
                self.memory.chat_memory.add_ai_message(self.greeting_message)

            response = await self.recommendation_agent.chat(user_input)
            return response
        elif self.current_agent == "order_placement":
            response = await self.order_placement_agent.process_order(user_input)
            if response["type"] == "order_confirmation" or response["type"] == "error":
                self.current_agent = "recommendation"
            return response

    def reset_first_interaction(self):
        self.first_interaction = True

    async def place_order(self, payload: Dict[str, Any]):
        self.current_agent = "order_placement"
        
        # Extract order_data and user_details from payload
        order_data = payload.get("order_data", [])
        user_details = payload.get("user_details", {})
        
        # Ensure both order_data and user_details are present
        if not order_data or not user_details:
            return {
                "type": "error",
                "response": "Missing required order information. Please provide both order data and user details."
            }

        # Pass extracted data to process_order
        formatted_data = {
            "order_data": order_data,
            "user_details": user_details
        }
        return await self.order_placement_agent.process_order(formatted_data)


chatbot_service = ChatbotService()
