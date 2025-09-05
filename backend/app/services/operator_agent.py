from typing import Dict, List, Any
from .recommendation_agent import RecommendationAgent
from langchain.chat_models import ChatOpenAI
from .order_query_agent import OrderQueryAgent
from .order_placement_agent import OrderPlacementAgent
from .fraudulent_transaction_agent import FraudulentTransactionAgent
from .user_proxy_agent import UserProxyAgent
from langchain.llms import OpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langchain.memory import ConversationBufferMemory
from app.services.utils import serialize_message
import logging
import os
import asyncio
from dotenv import load_dotenv

# Load environment variables (ensure .env contains OPENAI_API_KEY)
load_dotenv()

class OperatorAgent:
    def __init__(self, name: str, llm, memory):
        self.name = name

        # Initialize LLM and memory
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,
            openai_api_key=os.getenv("OPENAI_API_KEY"),
        )
        self.memory = ConversationBufferMemory(return_messages=True)

        # Register agents
        self.agent_registry = {
            "recommendation_agent": RecommendationAgent(self.llm, self.memory),
            "order_query_agent": OrderQueryAgent(llm=self.llm),
            "order_placement_agent": OrderPlacementAgent(llm=self.llm),
            "fraudulent_transaction_agent": FraudulentTransactionAgent(llm=self.llm),
            "user_proxy_agent": UserProxyAgent(),
        }

    def initialize_llm(self) -> ChatOpenAI:
        """
        Initialize the language model (LLM) with the API key from environment variables.
        """
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logging.error("OPENAI_API_KEY is not found in environment variables.")
            raise ValueError("OPENAI_API_KEY not found. Please set it in your .env file.")

        return ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,
            openai_api_key=api_key
        )

    def set_agent_registry(self, registry: Dict[str, Any]):
        """
        Register agents with the OperatorAgent for intent-based routing.
        """
        self.agent_registry = registry


    def determine_intent(self, message: str) -> List[str]:
        """
        Use the LLM to determine the intent of the user query.
        """
        prompt = (
            f"Classify the user's message into one or more of the following intents: "
            f"book_recommendation, order_query, order_placement, "
            f"fraudulent_transactions, or out_of_context.\n\n"
            f"User message: {message}\n\n"
            f"Return a comma-separated list of intents."
        )

        try:
            # Use the updated `invoke` method
            response = self.llm.invoke(prompt)
            # Extract content from AIMessage object
            response_content = response.content if hasattr(response, 'content') else str(response)
            predicted_intents = [intent.strip().lower() for intent in response_content.split(",")]
            return predicted_intents
        except Exception as e:
            logging.error(f"Error during intent determination: {e}")
            return ["out_of_context"]



    async def on_message(self, message: str) -> Dict:
        """
        Process the user message, determine the intent, and route to appropriate agents.
        """
        # Determine intents
        intents = self.determine_intent(message)

        # Intent to agent mapping
        intent_to_agent_map = {
            "book_recommendation": "recommendation_agent",
            "order_query": "order_query_agent",
            "order_placement": "order_placement_agent",
            "fraudulent_transactions": "fraudulent_transaction_agent",
            "out_of_context": None,
        }

        # Determine which agents to trigger
        triggered_agents = list({intent_to_agent_map[intent] for intent in intents
                                 if intent in intent_to_agent_map and intent_to_agent_map[intent]})

        # Fallback response if no agents are triggered
        if not triggered_agents:
            fallback_response = (
                "I'm here to assist with books, orders, or related queries. Please ask a relevant question!"
            )
            return {"next_node": "END", "messages": [AIMessage(content=fallback_response)]}

        combined_responses = []
        response_set = set()

        for intent in intents:
            agent_key = intent_to_agent_map.get(intent)
            if not agent_key or agent_key not in self.agent_registry:
                continue

            agent = self.agent_registry[agent_key]

            if asyncio.iscoroutinefunction(agent.on_message):
                agent_response = await agent.on_message(message)
            else:
                agent_response = agent.on_message(message)

            if "messages" in agent_response:
                for msg in agent_response["messages"]:
                    if isinstance(msg, AIMessage) and msg.content not in response_set:
                        combined_responses.append(serialize_message(msg))
                        response_set.add(msg.content)
                    elif isinstance(msg, dict) and msg.get("content") and msg.get("content") not in response_set:
                        # Handle already-serialized messages
                        combined_responses.append(msg)
                        response_set.add(msg.get("content"))
            
            if "recommendations" in agent_response:
                result = {"next_node": "END", "messages": combined_responses, "recommendations": agent_response["recommendations"]}
                return result

        curated_response = " ".join(msg["content"] for msg in combined_responses)
        self.memory.chat_memory.add_message(HumanMessage(content=curated_response))
        return {"next_node": "END", "messages": combined_responses}

    def __call__(self, input: str) -> Dict:
        """
        Allow the OperatorAgent to be callable by routing the input message to on_message.
        """
        return self.on_message(input)
