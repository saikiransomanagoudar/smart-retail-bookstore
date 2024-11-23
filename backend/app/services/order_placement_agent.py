# order_placement_agent.py

import logging
import re
from datetime import datetime, timedelta
from typing import Any, Dict
from sqlalchemy.exc import SQLAlchemyError

from backend.app.database.database import SessionLocal
from backend.app.models.orders import Order

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

            # Extract user_id (it should match an existing user_id in user_preferences)
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

    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Callable interface for langgraph compatibility.
        Processes the order details and updates the state.
        """
        order_details = state.get('order_details', {})
        order_confirmation = self.process_order(order_details)
        state['order_confirmation'] = order_confirmation
        return state