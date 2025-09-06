# chatbot_service.py

import os
import asyncio
from dotenv import load_dotenv
from typing import Dict, Any, List
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langgraph.graph import StateGraph
from langchain_core.messages import HumanMessage, AIMessage
from pydantic import BaseModel
import operator
import logging

from app.services.user_proxy_agent import UserProxyAgent
from app.services.operator_agent import OperatorAgent
from app.services.recommendation_agent import RecommendationAgent
from app.services.order_placement_agent import OrderPlacementAgent
from app.services.order_query_agent import OrderQueryAgent
from app.services.fraudulent_transaction_agent import FraudulentTransactionAgent

load_dotenv()


class MultiAgentState(BaseModel):
    messages: List[HumanMessage]

class ChatbotService:
    def __init__(self):
        # Load API Key
        openai_api_key = os.getenv('OPENAI_API_KEY')
        self.memory = ConversationBufferMemory(return_messages=True)
        if not openai_api_key:
            raise ValueError("OpenAI API key not found.")
        
        # Initialize LLM and memory
        self.llm = ChatOpenAI(
            temperature=0.7,
            model_name="gpt-4o-mini",  # Use the correct model name
            openai_api_key=openai_api_key
        )

        # Initialize agents
        self.user_proxy_agent = UserProxyAgent()
        self.recommendation_agent = RecommendationAgent(self.llm, self.memory)
        self.order_query_agent = OrderQueryAgent(llm=self.llm)
        self.order_placement_agent = OrderPlacementAgent(llm=self.llm)
        self.fraudulent_transaction_agent = FraudulentTransactionAgent(llm=self.llm)

        # Register agents with the OperatorAgent
        self.operator_agent = OperatorAgent("operator_agent", llm=self.llm, memory=self.memory)
        self.operator_agent.set_agent_registry({
            "recommendation_agent": self.recommendation_agent,
            "order_query_agent": self.order_query_agent,
            "order_placement_agent": self.order_placement_agent,
            "fraudulent_transaction_agent": self.fraudulent_transaction_agent,
        })

        # Register agents in the operator agent
        self.agent_registry = {
            "recommendation_agent": self.recommendation_agent,
            "order_placement_agent": self.order_placement_agent,
            "order_query_agent": self.order_query_agent,
            "fraudulent_transaction_agent": self.fraudulent_transaction_agent,
        }

        # Build the state graph
        self.state_graph = StateGraph(MultiAgentState)
        self.define_graph()

        self.greeting_message = (
            "Welcome! I'm BookWorm, your virtual assistant. "
            "I'm here to help you browse and find the perfect book for your collection. "
            "Ready to start exploring?"
        )

    def define_graph(self):
        self.state_graph.add_node("user_proxy_agent", self.user_proxy_agent)
        self.state_graph.add_node("operator_agent", self.operator_agent)
        self.state_graph.add_node("recommendation_agent", self.recommendation_agent)
        self.state_graph.add_node("order_placement_agent", self.order_placement_agent)
        self.state_graph.add_node("order_query_agent", self.order_query_agent)
        self.state_graph.add_node("fraudulent_transaction_agent", self.fraudulent_transaction_agent)

        self.state_graph.set_entry_point("user_proxy_agent")
        self.state_graph.add_edge("user_proxy_agent", "operator_agent")
        
        def route_after_operator(state):
            # Get the last message from operator_agent to determine routing
            if hasattr(state, 'messages') and state.messages:
                last_message = state.messages[-1]
                if hasattr(last_message, 'additional_kwargs'):
                    next_node = last_message.additional_kwargs.get('next_node', 'END')
                    return next_node
            return "END"
        
        self.state_graph.add_conditional_edges(
            "operator_agent",
            route_after_operator,
            {
                "END": "__end__",
                "recommendation_agent": "recommendation_agent",
                "order_placement_agent": "order_placement_agent", 
                "order_query_agent": "order_query_agent",
                "fraudulent_transaction_agent": "fraudulent_transaction_agent"
            }
        )
        
        # Add edges from specific agents back to end
        self.state_graph.add_edge("recommendation_agent", "__end__")
        self.state_graph.add_edge("order_placement_agent", "__end__")
        self.state_graph.add_edge("order_query_agent", "__end__")
        self.state_graph.add_edge("fraudulent_transaction_agent", "__end__")
        self.compiled_graph = self.state_graph.compile()

    async def chat(self, user_input: str):
        logging.info(f"Received user input: {user_input}")
        try:
            # Preprocess user input
            preprocessed_input = self.user_proxy_agent.preprocess_message({"message": user_input})
            logging.info(f"Preprocessed input: {preprocessed_input}")

            # Route the message through the operator agent
            agent_or_response = await self.operator_agent.on_message(preprocessed_input.get("message", ""))
            logging.info(f"Agent or response: {agent_or_response}")

            if isinstance(agent_or_response, dict):
                # Extract content from messages if response field is empty
                if not agent_or_response.get("response") and agent_or_response.get("messages"):
                    messages = agent_or_response["messages"]
                    if messages and isinstance(messages[0], dict):
                        agent_or_response["response"] = messages[0].get("content", "")
                    elif messages and hasattr(messages[0], "content"):
                        agent_or_response["response"] = messages[0].content
                
                final_response = self.user_proxy_agent.postprocess_response(agent_or_response)
                logging.info(f"Final response: {final_response}")
                return final_response

            # If an agent is returned, process the request with that agent
            agent = agent_or_response
            if hasattr(agent, "__call__"):
                if asyncio.iscoroutinefunction(agent.__call__):
                    response = await agent(preprocessed_input)
                else:
                    response = agent(preprocessed_input)
                logging.info(f"Response from agent: {response}")
                return self.user_proxy_agent.postprocess_response(response)

            return {
                "type": "error",
                "response": "No valid agent or response could be determined."
            }
        except Exception as e:
            logging.error(f"Error in chat method: {str(e)}")
            raise e


    def run_chatbot(self):
        print("Welcome to the BookWorm Assistant! Type 'exit' to quit.")
        while True:
            user_input = input("You: ")
            if user_input.lower() == "exit":
                print("Goodbye!")
                break

            response = self.chat(user_input)
            if response.get("type") == "response":
                print(f"Assistant: {response.get('content')}")
            elif response.get("type") == "end":
                print(response.get("response"))
                break


if __name__ == "__main__":
    chatbot_service = ChatbotService()
    chatbot_service.run_chatbot()
