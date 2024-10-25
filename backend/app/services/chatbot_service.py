from typing import Tuple
from langchain_openai import ChatOpenAI

from langchain.memory import ConversationBufferMemory
from datetime import datetime, timedelta

from backend.app.models.orders import Order
from backend.app.services.graphql_service import graphql_service
import re

def normalize_title(title: str) -> str:
    return re.split(r':|–|-', title)[-1].strip()


from typing import List, Dict, Any
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
import json
import logging


class RecommendationAgent:
    def __init__(self, llm, memory):
        self.llm = llm
        self.memory = memory
        self.recommendation_provided = False
        self.ready_for_recommendations = False
        self.recommended_books = set()  # Track previously recommended books
        self.question_count = 0
        self.MIN_QUESTIONS = 3  # Minimum number of questions before recommendations

        # Separate prompts for conversation and recommendations
        self.conversation_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an AI assistant specializing in book recommendations. Your goal is to understand the user's preferences and provide personalized book recommendations. Follow these guidelines:

1. You MUST ask at least 3 questions before making recommendations. Track the following key areas:
   - Preferred genres and themes
   - Reading experience level
   - Specific interests or topics
   - Previous books they enjoyed or disliked
2. Only say 'READY_FOR_RECOMMENDATIONS' after asking AT LEAST 3 meaningful questions.
3. If the user expresses dissatisfaction with recommendations:
   - First acknowledge their feedback
   - Then ask AT LEAST 2 specific questions about what they didn't like
   - Focus on understanding their preferences more deeply
4. NEVER provide book recommendations in the conversation - wait for the explicit recommend_books call.
5. Keep the conversation natural and avoid repetitive questions.
6. If a user provides multiple pieces of information in one response, still ask follow-up questions about other aspects not covered."""),
            ("human", "{input}"),
            ("ai", "{agent_scratchpad}")
        ])

        self.recommendation_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a book recommendation specialist. Generate recommendations based on the provided conversation history. Follow these rules strictly:
1. NEVER include author names in book titles
2. NEVER use "by" or "written by" in titles
3. Return ONLY the exact book title as it appears on the cover
4. Ensure recommendations are diverse within the user's interests
5. Format output as a valid JSON array
6. DO NOT recommend any books from the provided exclusion list
7. Focus especially on the most recent preferences and feedback provided by the user"""),
            ("human", "{input}")
        ])

        self.conversation = (
                RunnablePassthrough.assign(
                    agent_scratchpad=lambda x: self.memory.chat_memory.messages
                )
                | self.conversation_prompt
                | self.llm
                | StrOutputParser()
        )

        self.recommendation_chain = (
                self.recommendation_prompt
                | self.llm
                | StrOutputParser()
        )

    async def chat(self, user_input: str):
        if user_input.lower() == 'quit':
            self.reset_state()
            return {"type": "system", "response": "Conversation reset."}

        # Handle user's dissatisfaction with recommendations
        if self.recommendation_provided and any(phrase in user_input.lower() for phrase in
                                                ["don't like", "didn't like", "not good", "bad recommendations",
                                                 "poor suggestions"]):
            self.recommendation_provided = False
            self.ready_for_recommendations = False
            self.question_count = 0  # Reset question count to ensure more questions are asked
            response = await self.conversation.ainvoke({
                "input": f"User didn't like previous recommendations: {user_input}. Ask specific questions about their preferences."
            })
            self.memory.chat_memory.add_user_message(user_input)
            self.memory.chat_memory.add_ai_message(response)
            return {"type": "question", "response": response}

        response = await self.conversation.ainvoke({"input": user_input})
        self.memory.chat_memory.add_user_message(user_input)
        self.memory.chat_memory.add_ai_message(response)

        # Increment question count when the AI asks a question
        if "?" in response:
            self.question_count += 1

        # Check if ready for recommendations
        if "READY_FOR_RECOMMENDATIONS" in response:
            if self.question_count >= self.MIN_QUESTIONS:
                self.ready_for_recommendations = True
                recommendations = await self.recommend_books()
                self.recommendation_provided = True
                return {
                    "type": "recommendation",
                    "response": recommendations
                }
            else:
                # Force more questions if minimum not reached
                follow_up_response = await self.conversation.ainvoke({
                    "input": "Please ask more questions to better understand user preferences"
                })
                self.memory.chat_memory.add_ai_message(follow_up_response)
                return {
                    "type": "question",
                    "response": follow_up_response
                }

        return {
            "type": "question",
            "response": response.replace("READY_FOR_RECOMMENDATIONS",
                                         "Based on our conversation, I can now provide some book recommendations for you.")
        }

    async def recommend_books(self) -> List[Dict[str, Any]]:
        # Rest of the recommend_books method remains the same
        if not self.ready_for_recommendations:
            return []

        chat_history = self.memory.chat_memory.messages
        conversation_summary = "\n".join([f"{msg.type}: {msg.content}" for msg in chat_history])

        try:
            previously_recommended = "\n".join(self.recommended_books)
            response = await self.recommendation_chain.ainvoke({
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
            })

            cleaned_response = response.strip().strip("```json").strip("```").strip()
            recommendations = json.loads(cleaned_response)

            if not isinstance(recommendations, list):
                raise ValueError("Response is not a JSON array")

            processed_books = []
            for rec in recommendations:
                normalized_title = normalize_title(rec['Title'])

                if normalized_title in self.recommended_books:
                    logging.info(f"Skipping previously recommended book: {normalized_title}")
                    continue

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
            logging.info(f"Processing order with input type: {type(user_input)}")
            logging.info(f"Current state: {self.state}")
            logging.info(f"Input data: {user_input}")

            # Initial state with cart data
            if self.state == "INIT" and isinstance(user_input, dict) and 'order_data' in user_input:
                self.cart_items = user_input['order_data']
                logging.info(f"Received cart items: {self.cart_items}")

                if not self.cart_items or not isinstance(self.cart_items, list):
                    return {
                        "type": "error",
                        "response": "No items in cart. Please add items before placing an order."
                    }

                self.state = "ASK_ADDRESS"
                return {
                    "type": "order_question",
                    "response": "Great! To place your order, I'll need some additional information. Please provide your shipping address in this format:\nStreet Address, City, State, ZIP"
                }

            # Handle address input
            elif self.state == "ASK_ADDRESS" and isinstance(user_input, str):
                success, result = self.parse_address(user_input)
                if success:
                    self.order_data.update(result)
                    self.state = "ASK_PAYMENT"
                    return {
                        "type": "order_question",
                        "response": "Thank you. Now, please provide your payment details in this format:\nCARD_NUMBER MM/YY CVV"
                    }
                else:
                    return {
                        "type": "order_question",
                        "response": result["error"]
                    }

            # Handle payment input
            elif self.state == "ASK_PAYMENT" and isinstance(user_input, str):
                success, result = self.parse_payment_details(user_input)
                if success:
                    self.order_data.update(result)
                    return await self.confirm_order()
                else:
                    return {
                        "type": "order_question",
                        "response": result["error"]
                    }

            else:
                logging.error(f"Invalid state or input type. State: {self.state}, Input type: {type(user_input)}")
                return {
                    "type": "error",
                    "response": "Something went wrong. Please try placing your order again."
                }

        except Exception as e:
            logging.error(f"Error processing order: {str(e)}")
            self.reset()
            return {
                "type": "error",
                "response": "Sorry, there was an error processing your request. Please try again."
            }

    async def confirm_order(self):
        """Create orders for all items in cart and return structured order confirmation"""
        try:
            # Prepare order data
            order_data = {
                'street': self.order_data.get('street'),
                'city': self.order_data.get('city'),
                'state': self.order_data.get('state'),
                'zip_code': self.order_data.get('zip_code'),
                'card_number': self.order_data.get('card_number'),
                'expiry_date': self.order_data.get('expiry_date'),
                'user_id': 1  # You might want to update this with actual user ID
            }

            total_cost = sum(item.get('Price', 0) * item.get('quantity', 0) for item in self.cart_items)

            order_date = datetime.now()
            expected_delivery = order_date + timedelta(days=4)

            success, order_id = Order.create_order(self.cart_items, order_data)

            if success:
                self.reset()
                return {
                    "type": "order_confirmation",
                    "response": {
                        "order_id": str(order_id),
                        "total_cost": f"{total_cost:.2f}",
                        "order_placed_on": order_date.strftime("%Y-%m-%d %H:%M:%S"),
                        "expected_delivery": expected_delivery.strftime("%Y-%m-%d"),
                        "status": "success",
                        "message": f"Successfully placed order!"
                    }
                }
            else:
                raise Exception("Failed to create order")

        except Exception as e:
            logging.error(f"Error confirming orders: {str(e)}")
            self.reset()
            return {
                "type": "error",
                "response": {
                    "status": "error",
                    "message": "Sorry, there was an error processing your order. Please try again later.",
                    "error_details": str(e)
                }
            }

    def parse_address(self, address: str) -> Tuple[bool, Dict[str, str]]:
        """Parse address string into components"""
        try:
            parts = [part.strip() for part in address.split(',') if part.strip()]

            if len(parts) < 4:
                return False, {"error": "Please provide your address in this format: Street Address, City, State, ZIP"}

            return True, {
                'street': parts[0],
                'city': parts[1],
                'state': parts[2].upper(),
                'zip_code': parts[3]
            }
        except Exception as e:
            logging.error(f"Error parsing address: {str(e)}")
            return False, {"error": "Please provide your address in this format: Street Address, City, State, ZIP"}

    def parse_payment_details(self, payment: str) -> Tuple[bool, Dict[str, str]]:
        """Parse payment string in format 'CARD_NUMBER MM/YY CVV'"""
        try:
            parts = payment.strip().split()
            if len(parts) != 3:
                return False, {"error": "Please provide payment details in this format: CARD_NUMBER MM/YY CVV"}

            card_number = parts[0]
            expiry_date = parts[1]

            if not card_number.isdigit() or len(card_number) != 16:
                return False, {"error": "Card number must be 16 digits"}

            if not re.match(r'^\d{2}/\d{2}$', expiry_date):
                return False, {"error": "Expiry date must be in MM/YY format"}

            return True, {
                'card_number': card_number,
                'expiry_date': expiry_date
            }
        except Exception as e:
            logging.error(f"Error parsing payment details: {str(e)}")
            return False, {"error": "Please provide payment details in this format: CARD_NUMBER MM/YY CVV"}

    def reset(self):
        """Reset the agent state"""
        self.state = "INIT"
        self.order_data = {}
        self.cart_items = []

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
            return response
        elif self.current_agent == "order_placement":
            response = await self.order_placement_agent.process_order(user_input)
            if response["type"] == "order_confirmation" or response["type"] == "error":
                self.current_agent = "recommendation"
            return response

    async def place_order(self, order_data: List[Dict[str, Any]]):
        self.current_agent = "order_placement"
        # Wrap the order data in the expected format
        formatted_data = {
            "order_data": order_data
        }
        return await self.order_placement_agent.process_order(formatted_data)

chatbot_service = ChatbotService()