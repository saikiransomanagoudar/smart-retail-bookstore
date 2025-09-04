# order_query_agent.py

import logging
from datetime import datetime
import re
from typing import Dict, Any

from backend.app.models.orders import Order

class OrderQueryAgent:
    def __init__(self, llm):
        self.llm = llm
        self.state = "INIT"
        self.user_id = None

    async def on_message(self, user_input: str) -> Dict[str, Any]:
        """Handle messages from the operator agent"""
        # For now, use a default user_id since we don't have user context
        # In a real implementation, this should come from the session/auth
        default_user_id = 1  # You may want to extract this from context
        
        result = await self.process_query(user_input, default_user_id)
        
        # Convert to messages format expected by operator agent
        from langchain_core.messages import AIMessage
        return {
            "messages": [AIMessage(content=str(result.get("response", "No response available")))]
        }

    async def process_query(self, user_input: str, user_id: int) -> Dict[str, Any]:
        """Process user queries about orders"""
        self.user_id = user_id

        # Check if metadata is present in the input (for direct order detail requests)
        if isinstance(user_input, dict) and user_input.get('metadata', {}).get('type') == 'order_details':
            order_id = user_input['metadata'].get('order_id')
            if order_id:
                order_details = Order.get_order_details(order_id, user_id)
                if order_details:
                    # Format the order details to match the OrderInfoCard expectations
                    formatted_details = {
                        "order_id": order_details["order_id"],
                        "total_cost": str(sum(item["subtotal"] for item in order_details["items"])),
                        "order_placed_on": order_details["purchase_date"],
                        "expected_delivery": order_details["expected_delivery"],
                        "status": "Delivered" if datetime.now() > datetime.strptime(order_details["expected_delivery"],
                                                                                    "%Y-%m-%d") else "In Transit",
                        "message": f"Order details retrieved successfully.",
                        "shipping_address": order_details["shipping_address"],
                        "items": order_details["items"]
                    }
                    return {
                        "type": "order_info",  # Changed this from order_details to order_info
                        "response": formatted_details
                    }
                return {
                    "type": "error",
                    "response": "Order not found or unauthorized access."
                }

        # Handle text-based queries
        if isinstance(user_input, str):
            # Check if input contains an order ID
            if "order" in user_input.lower() and any(char.isdigit() for char in user_input):
                order_id = self.extract_order_id(user_input)
                if order_id:
                    order_details = Order.get_order_details(order_id, user_id)
                    if order_details:
                        formatted_details = {
                            "order_id": order_details["order_id"],
                            "total_cost": str(sum(item["subtotal"] for item in order_details["items"])),
                            "order_placed_on": order_details["purchase_date"],
                            "expected_delivery": order_details["expected_delivery"],
                            "status": "Delivered" if datetime.now() > datetime.strptime(
                                order_details["expected_delivery"], "%Y-%m-%d") else "In Transit",
                            "message": f"Order details retrieved successfully.",
                            "shipping_address": order_details["shipping_address"],
                            "items": order_details["items"]
                        }
                        return {
                            "type": "order_info",  # Changed this from order_details to order_info
                            "response": formatted_details
                        }
                    return {
                        "type": "error",
                        "response": "Order not found or unauthorized access."
                    }

            # If user asks about order history
            if any(keyword in user_input.lower() for keyword in ["orders", "history", "purchases"]):
                orders = Order.get_user_orders(user_id)
                if orders:
                    return {
                        "type": "order_list",
                        "response": orders
                    }
                return {
                    "type": "error",
                    "response": "No orders found."
                }

        return {
            "type": "clarification",
            "response": "Would you like to see your order history or check a specific order? Please provide more details."
        }

    def extract_order_id(self, text: str) -> str:
        """Extract order ID from user input"""
        import re
        # Look for UUID pattern
        uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
        uuid_match = re.search(uuid_pattern, text, re.IGNORECASE)
        if uuid_match:
            return uuid_match.group(0)
        return None
    
    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        
        user_id = state.get('user_id')
        order_id = state.get('order_id')
        order_details = self.query_order(user_id, order_id)
        state['order_details'] = order_details
        return state
