from typing import Dict, List, Any, Tuple
from langchain_core.agents import AgentAction, AgentFinish
from langchain.agents import AgentExecutor
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langgraph.graph import StateGraph, END
from sqlalchemy import select
from backend.app.database.database import SessionLocal
from backend.app.models.orders import Order
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from fastapi import Depends


# Example: Using a session to retrieve the user's ID
def get_user_id_from_session(session: dict) -> str:
    user_id = session.get("user_id")
    if not user_id:
        raise ValueError("User not logged in.")
    return user_id

from datetime import datetime, timedelta
import logging
import re
import json
import traceback

from backend.app.services.graphql_service import graphql_service
from sqlalchemy.exc import SQLAlchemyError

logging.basicConfig(level=logging.INFO)

def normalize_title(title: str) -> str:
    return re.split(r":|–|-", title)[-1].strip()

def classify_intent(user_input: str) -> str:
    fraud_keywords = ["fraudulent", "unauthorized", "unknown charge", "damaged", "broken", "shipping box"]
    order_keywords = ["order", "purchase", "bought", "delivery", "shipping", "track"]
    recommendation_keywords = ["recommend", "suggest", "book", "read", "genre", "theme"]

    if any(keyword in user_input.lower() for keyword in fraud_keywords):
        return "fraud"
    elif any(keyword in user_input.lower() for keyword in order_keywords):
        return "order"
    elif any(keyword in user_input.lower() for keyword in recommendation_keywords):
        return "recommendation"
    else:
        return "unknown"


class FraudTransactionAgent:
    def __init__(self, llm):
        self.llm = llm  # Use the GPT-4o-mini model here
        self.state = "INIT"
        self.issue_type = None
        self.description = None
        self.image_url = None

    async def process_fraud_report(self, user_input: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handles the fraud report process step-by-step.
        """
        try:
            if self.state == "INIT":
                # Ask for clarification
                self.state = "CLARIFY_ISSUE"
                return {
                    "type": "question",
                    "response": "Could you please describe the issue you're facing? For example, is it a damaged product or a fraudulent transaction?"
                }

            elif self.state == "CLARIFY_ISSUE":
                # Determine the type of issue
                if "damaged" in user_input.lower() or "box" in user_input.lower():
                    self.issue_type = "damaged_product"
                    self.state = "REQUEST_IMAGE"
                    return {
                        "type": "question",
                        "response": "Thank you for clarifying. Please upload an image of the damaged product or shipping box for further review."
                    }
                elif "fraudulent" in user_input.lower() or "unauthorized" in user_input.lower():
                    self.issue_type = "fraudulent_transaction"
                    self.state = "REQUEST_IMAGE"
                    return {
                        "type": "question",
                        "response": "Thank you for clarifying. Please upload an image of the transaction (e.g., a screenshot or receipt) for further review."
                    }
                else:
                    return {
                        "type": "clarification",
                        "response": "I'm sorry, I couldn't identify the issue. Could you please specify if it's a damaged product or a fraudulent transaction?"
                    }

            elif self.state == "REQUEST_IMAGE":
                # Handle image upload
                if "image_url" in metadata:
                    self.image_url = metadata["image_url"]
                    self.state = "REQUEST_DESCRIPTION"
                    return {
                        "type": "question",
                        "response": "Thank you for the image. Could you also provide a brief description of the issue to help us analyze it better?"
                    }
                else:
                    return {
                        "type": "request_image",
                        "response": "Please upload an image to proceed with your report."
                    }

            elif self.state == "REQUEST_DESCRIPTION":
                # Store description and move to analysis
                self.description = user_input
                self.state = "PROCESSING"
                return await self.analyze_report()

        except Exception as e:
            logging.error(f"Error processing fraud report: {str(e)}")
            return {
                "type": "error",
                "response": "Sorry, there was an error processing your request. Please try again."
            }

    async def analyze_report(self) -> Dict[str, Any]:
        """
        Uses GPT-4o-mini to analyze the image and description and decide the appropriate action.
        """
        try:
            # Generate the input for GPT-4o-mini
            gpt_input = f"""
You are a fraud detection assistant. Analyze the following report:

1. Issue Type: {self.issue_type}
2. Description: {self.description}
3. Image URL: {self.image_url}

Based on the description and image:
- Determine if this issue is valid or invalid.
- Suggest one of the following actions:
  - "Refund" if the issue is valid and warrants a refund.
  - "Decline" if the issue is invalid or unverifiable.
  - "Escalate to Human-Agent" if more detailed human review is required.

Respond with a JSON object in the following format:
{{
  "decision": "<Refund|Decline|Escalate to Human-Agent>",
  "reason": "<Brief reason for the decision>"
}}
            """

            # Call GPT-4o-mini for decision-making
            gpt_response = await self.llm.agenerate([gpt_input])
            decision_data = json.loads(gpt_response.generations[0].text.strip())

            # Extract the decision and reason
            decision = decision_data.get("decision")
            reason = decision_data.get("reason", "No specific reason provided.")

            if decision == "Refund":
                return {
                    "type": "resolution",
                    "action": "Refund",
                    "response": f"Decision: Refund. {reason}"
                }
            elif decision == "Decline":
                return {
                    "type": "resolution",
                    "action": "Decline",
                    "response": f"Decision: Decline. {reason}"
                }
            elif decision == "Escalate to Human-Agent":
                return {
                    "type": "resolution",
                    "action": "Escalate to Human-Agent",
                    "response": f"Decision: Escalate to Human-Agent. {reason}"
                }
            else:
                return {
                    "type": "error",
                    "response": "An unexpected decision was returned. Please try again."
                }

        except Exception as e:
            logging.error(f"Error analyzing report with GPT-4o-mini: {str(e)}")
            return {
                "type": "error",
                "response": "An error occurred during analysis. Please try again later."
            }

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

    async def chat(self, user_input: str) -> Dict[str, Any]:

        try:
            # Handle "quit" command
            if user_input.lower() == "quit":
                self.reset_state()
                return {"type": "system", "response": "Conversation reset. Feel free to start over."}

            # Handle out-of-context user inputs
            if self.is_out_of_context(user_input):
                self.out_of_context_count += 1
                if self.out_of_context_count == 1:
                    response = "I'm here to assist with book recommendations and related information. Please ask about books."
                elif self.out_of_context_count == 2:
                    response = "I specialize in helping with books. Let me know how I can assist you with recommendations or book-related queries."
                else:
                    response = "It seems we are off track. Let's refocus on books! How can I assist you today?"
                return {"type": "system", "response": response}

            # Reset out-of-context counter
            self.out_of_context_count = 0

            # Handle user feedback on recommendations
            feedback_keywords = [
                "don't recommend", "don't like", "didn't like", "not good",
                "bad recommendations", "poor suggestions", "stop recommendations"
            ]
            if self.recommendation_provided and any(phrase in user_input.lower() for phrase in feedback_keywords):
                self.recommendation_provided = False
                self.ready_for_recommendations = False
                self.question_count = max(2, self.question_count)  # Reset question count

                response = await self.conversation.ainvoke({
                    "input": "It seems you weren't satisfied with the previous recommendations. Could you share more about your preferences (genres, authors, or themes) to improve my suggestions?"
                })
                self.memory.chat_memory.add_user_message(user_input)
                self.memory.chat_memory.add_ai_message(response)
                return {"type": "question", "response": response}

            # Regular conversation flow
            response = await self.conversation.ainvoke({"input": user_input})
            self.memory.chat_memory.add_user_message(user_input)
            self.memory.chat_memory.add_ai_message(response)

            # Check if ready for recommendations
            if self.check_readiness(response):
                self.ready_for_recommendations = True
                recommendations = await self.recommend_books()
                self.recommendation_provided = True
                return {"type": "recommendation", "response": recommendations}

            # Increment question count for building context
            if "?" in response and not self.ready_for_recommendations:
                self.question_count += 1

            return {"type": "question", "response": response}

        except Exception as e:
            # Log the exception and return a user-friendly error message
            logging.error(f"An error occurred during chat processing: {str(e)}")
            logging.error(traceback.format_exc())
            return {
                "type": "error",
                "response": "I'm sorry, something went wrong while process"
            }


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
        from backend.app.database.database import SessionLocal
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

            # Validate user_details fields
            required_fields = ["user_id", "address", "cardNumber", "expiryDate", "cvv"]
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

            user_id = user_details.get("user_id")
            if not user_id:
                return {
                    "type": "error",
                    "response": "User ID is required and must match an existing user in the system.",
                }

            # Generate order_id and other metadata
            order_id = f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            total_cost = sum(float(item.get("Price", 0)) * item.get("quantity", 1) for item in order_data)
            purchase_time = datetime.now()
            expected_delivery = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")

            # Save order to the database
            db = SessionLocal()
            try:
                for item in order_data:
                    new_order = Order(
                        order_id=order_id,
                        user_id=user_id,
                        title=item.get("title"),
                        price=float(item.get("Price", 0)),
                        total_quantity=item.get("quantity", 1),
                        street=user_details.get("address").get("street"),
                        city=user_details.get("address").get("city"),
                        state=user_details.get("address").get("state"),
                        zip_code=user_details.get("address").get("zip_code"),
                        card_number=f"****{user_details['cardNumber'][-4:]}",
                        expiry_date=user_details.get("expiryDate"),
                        purchase_date=purchase_time,
                        expected_shipping_date=expected_delivery,
                    )
                    db.add(new_order)
                db.commit()
            except SQLAlchemyError as e:
                logging.error(f"Database error: {str(e)}")
                db.rollback()
                return {
                    "type": "error",
                    "response": "Sorry, there was an issue saving your order. Please try again.",
                }
            finally:
                db.close()

            # Create order confirmation response
            order_confirmation = {
                "order_id": order_id,
                "total_cost": f"{total_cost:.2f}",
                "order_placed_on": purchase_time.strftime("%Y-%m-%d %H:%M:%S"),
                "expected_delivery": expected_delivery,
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


class OrderQueryAgent:
    def __init__(self, llm):
        self.llm = llm
        self.state = "INIT"
        self.user_id = None

    async def process_query(self, user_input: str, user_id: Any) -> Dict[str, Any]:
        # Log the received user_id for debugging
        logging.info(f"Received user_id: {user_id}, type: {type(user_id)}")

        # Ensure user_id is always treated as a string
        if not isinstance(user_id, str):
            logging.warning(f"Expected user_id as string but got {type(user_id)}. Converting to string.")
            user_id = str(user_id)

        self.user_id = user_id  # Store the user_id for potential future use
        logging.info(f"Processing query for user_id: {user_id}, input: {user_input}")

        # Check if the user is asking about order history
        if any(keyword in user_input.lower() for keyword in ["orders", "history", "purchases"]):
            try:
                logging.info(f"User {user_id} requested order history")

                # Fetch orders for the user
                orders = Order.get_user_orders(user_id=user_id)
                logging.info(f"Orders retrieved for user_id {user_id}: {orders}")

                # Return the orders if they exist
                if orders:
                    return {"type": "order_list", "response": orders}

                # Return an error if no orders are found
                return {"type": "error", "response": "No orders found."}
            except Exception as e:
                # Log any errors that occur during order retrieval
                logging.error(f"Error fetching order history for user_id {user_id}: {e}")
                return {"type": "error", "response": "An error occurred while fetching your order history."}

        # Handle cases where the user's input is unclear
        return {
            "type": "clarification",
            "response": "Would you like to see your order history or check a specific order? Please provide more details."
        }


    def extract_order_id(self, text: str) -> str:
        """Extract order ID from user input"""
        import re
        uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
        uuid_match = re.search(uuid_pattern, text, re.IGNORECASE)
        if uuid_match:
            return uuid_match.group(0)
        return None

    def format_order_details(self, order_details: Dict[str, Any]) -> Dict[str, Any]:
        """Format order details for response"""
        return {
            "order_id": order_details["order_id"],
            "total_cost": str(sum(item["subtotal"] for item in order_details["items"])),
            "order_placed_on": order_details["purchase_date"],
            "expected_delivery": order_details["expected_shipping_date"],
            "status": "Delivered" if datetime.now() > datetime.strptime(order_details["expected_delivery"], "%Y-%m-%d") else "In Transit",
            "message": "Order details retrieved successfully.",
            "shipping_address": order_details["shipping_address"],
            "items": order_details["items"]
        }


class ChatbotService:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0.7, model_name="gpt-4o-mini")
        self.memory = ConversationBufferMemory(return_messages=True)
        self.recommendation_agent = RecommendationAgent(self.llm, self.memory)
        self.order_placement_agent = OrderPlacementAgent(self.llm)
        self.order_query_agent = OrderQueryAgent(self.llm)
        self.fraud_transaction_agent = FraudTransactionAgent(self.llm)
        self.current_agent = "recommendation"
        self.greeting_message = "Welcome! I'm BookWorm, your virtual assistant. I'm here to help you browse and find the perfect book for your collection. Ready to start exploring?"
        self.first_interaction = True

    async def chat(self, user_input: dict):
        """
        Main chat method that dynamically routes user queries to the appropriate agent
        based on the intent classification.
        """
        input_message = user_input.get('message') if isinstance(user_input, dict) else user_input
        metadata = user_input.get('metadata') if isinstance(user_input, dict) else {}

        if self.first_interaction and not metadata:
            self.first_interaction = False
            return {"type": "greeting", "response": self.greeting_message}

        if isinstance(input_message, str):
            if input_message.lower() == "clear":
                self.reset_first_interaction()
                self.memory.clear()
                return {"type": "system", "response": "How can I assist you today?"}

            # Classify the user's intent
            intent = self.classify_intent(input_message)

            try:
                if intent == "fraud":
                    # Route to FraudTransactionAgent
                    return await self.fraud_transaction_agent.process_fraud_report(input_message, metadata)

                elif intent == "order":
                    # Route to OrderQueryAgent
                    # Get the user's ID dynamically from metadata or session
                    user_id = await self.get_user_id_from_metadata(metadata)
                    if not user_id:
                        return {"type": "error", "response": "Please log in to view or manage your orders."}
                    return await self.order_query_agent.process_query(input_message, user_id)

                elif intent == "recommendation":
                    # Route to RecommendationAgent
                    return await self.recommendation_agent.chat(input_message)

                else:
                    # Handle unknown or unclear intents
                    return {
                        "type": "clarification",
                        "response": "I'm sorry, I didn't understand your request. Could you please clarify?"
                    }

            except Exception as e:
                # Handle any errors during routing or processing
                logging.error(f"Error processing chat request: {str(e)}")
                return {"type": "error", "response": "Sorry, something went wrong while processing your request."}

        else:
            # Handle invalid input
            return {"type": "error", "response": "Invalid input. Please provide a valid message."}

    # Add the helper method for intent classification
    def classify_intent(self, user_input: str) -> str:
        
        # Keywords for fraud-related queries
        fraud_keywords = ["fraud", "report fraud", "fraudulent", "unauthorized", "unknown charge", "damaged", "broken", "shipping box"]
        order_keywords = ["order", "purchase", "bought", "delivery", "shipping", "track"]
        recommendation_keywords = ["recommend", "suggest", "book", "read", "genre", "theme"]

        user_input_lower = user_input.lower()

        if any(keyword in user_input_lower for keyword in fraud_keywords):
            return "fraud"
        elif any(keyword in user_input_lower for keyword in order_keywords):
            return "order"
        elif any(keyword in user_input_lower for keyword in recommendation_keywords):
            return "recommendation"
        else:
            return "unknown"


    # Add the helper method to get the user ID from metadata or session
    async def get_user_id_from_metadata(self, metadata: dict) -> str:
        """
        Retrieve the user ID from metadata or session.
        """
        try:
            from fastapi import Request
            request: Request = metadata.get('request')
            session = request.session if request else None
            if session:
                return get_user_id_from_session(session)
        except ValueError as e:
            logging.error(f"Error retrieving user ID: {str(e)}")
            return None



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
