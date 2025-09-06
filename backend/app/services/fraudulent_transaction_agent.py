# fraudulent_transaction_agent.py

from typing import Dict, Any
import logging

class FraudulentTransactionAgent:

    def __init__(self, llm):
        self.llm = llm
        self.logger = logging.getLogger(__name__)

    async def handle_issue(self, user_input: Dict[str, Any], user_id: int):
        issue_type = user_input.get('issue_type')
        if issue_type == "damaged_product":
            return await self.handle_damaged_product(user_input, user_id)
        elif issue_type == "fraudulent_transaction":
            return await self.handle_fraudulent_transaction(user_input, user_id)
        else:
            return {
                "type": "error",
                "response": "Invalid issue type provided."
            }

    async def handle_damaged_product(self, user_input: Dict[str, Any], user_id: int) -> Dict[str, Any]:
        message = user_input.get('message', '')
        image_url = user_input.get('image_url', '')

        decision = await self.make_decision(message, "damaged_product")
        response = self.generate_response(decision, "damaged_product")
        return response

    async def handle_fraudulent_transaction(self, user_input: Dict[str, Any], user_id: int) -> Dict[str, Any]:
        message = user_input.get('message', '')
        ocr_image_url = user_input.get('ocr_image_url', '')

        # Make a decision using the LLM
        decision = await self.make_decision(message, "fraudulent_transaction")
        response = self.generate_response(decision, "fraudulent_transaction")
        return response

    async def make_decision(self, message: str, issue_type: str) -> str:
        prompt = f"""
You are an AI assistant handling customer issues.

Issue Type: {issue_type}
Customer Message: "{message}"

Based on the issue type and message, decide on one of the following actions:

- For damaged_product:
  - "Refund"
  - "Replace"
  - "Escalate to Human-Agent"

- For fraudulent_transaction:
  - "Refund"
  - "Decline"
  - "Escalate to Human-Agent"

Respond with only the action.
"""
        try:
            decision = await self.llm.apredict(prompt)
            decision = decision.strip()
            self.logger.info(f"Decision made: {decision}")
            return decision
        except Exception as e:
            self.logger.error(f"Error making decision: {str(e)}")
            return "Escalate to Human-Agent"

    def generate_response(self, decision: str, issue_type: str) -> Dict[str, Any]:
        if issue_type == "damaged_product":
            if decision == "Refund":
                response = "We apologize for the inconvenience. A refund has been initiated for your damaged product."
            elif decision == "Replace":
                response = "We're sorry about the damaged product. A replacement will be shipped to you shortly."
            else:
                response = "Your case requires further assistance. A human agent will contact you soon."
        elif issue_type == "fraudulent_transaction":
            if decision == "Refund":
                response = "We have processed a refund for the fraudulent transaction on your account."
            elif decision == "Decline":
                response = "After reviewing, we cannot process a refund for this transaction."
            else:
                response = "Your case requires further assistance. A human agent will contact you soon."
        else:
            response = "An error occurred while processing your request."

        return {"type": "resolution", "response": response}

    def reset(self):
        
        pass

    async def on_message(self, message: str) -> Dict[str, Any]:
       
        from langchain_core.messages import AIMessage
        
        try:
            response = "I can help you with fraudulent transaction issues. Please provide details about the suspicious transaction."
            return {"messages": [AIMessage(content=response)]}
        except Exception as e:
            logging.error(f"Error in FraudulentTransactionAgent.on_message: {str(e)}")
            return {"messages": [AIMessage(content="I'm sorry, I encountered an error while processing your request. Please try again.")]}

    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Callable interface for langgraph compatibility.
        Handles fraudulent transactions and updates the state.
        """
        issue_details = state.get('issue_details', {})
        resolution = self.handle_issue(issue_details)
        state['resolution'] = resolution
        return state
