from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationBufferMemory
from langchain.llms import OpenAI
from langchain_core.messages import AIMessage
import asyncio
import logging
import re
import json
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO)

def normalize_title(title: str) -> str:
    return re.split(r":|–|-", title)[-1].strip()

from backend.app.services.graphql_service import graphql_service

class RecommendationAgent:
    def __init__(self, llm, memory):
        self.llm = llm
        self.memory = memory
        self.recommendation_provided = False
        self.ready_for_recommendations = False
        self.recommended_books = set()
        self.question_count = 0
        self.MIN_QUESTIONS = 4
        self.out_of_context_count = 0
        self.current_user_input = ""
        self.genre_request_count = {}
        self.last_recommended_genre = None

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
                    7. Focus especially on the most recent preferences and feedback provided by the user
                    8. If user requests specific genres (horror, fantasy, etc.), prioritize those genres
                    9. Even with limited information, provide relevant recommendations based on what the user has asked for
                    10. Recommend classic, well-known books and series that are commonly found in databases
                    11. For horror: focus on Stephen King classics, classic horror novels
                    12. For fantasy: focus on Tolkien, popular fantasy series
                    13. For sci-fi: focus on classic sci-fi novels and popular series
                    14. Use simple, common titles without subtitles when possible""",
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
        # Store the current user input for genre detection
        self.current_user_input = user_input
        
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

        # Check if this is a direct request for recommendations
        if self.ready_for_recommendations or self.check_readiness(user_input):
            self.memory.chat_memory.add_user_message(user_input)
            self.ready_for_recommendations = True
            recommendations = await self.recommend_books()
            self.recommendation_provided = True
            return {"type": "recommendation", "response": recommendations}
        
        response = await self.conversation.ainvoke({"input": user_input})
        self.memory.chat_memory.add_user_message(user_input)
        self.memory.chat_memory.add_ai_message(response)

        if self.detect_refresh_request(user_input) and self.last_recommended_genre:
            recommendations = await self.recommend_books(user_input)
            return {"type": "recommendation", "response": recommendations}
        
        if self.check_readiness(user_input):
            self.ready_for_recommendations = True
            recommendations = await self.recommend_books(user_input)
            self.recommendation_provided = True
            return {"type": "recommendation", "response": recommendations}

        if "?" in response and not self.ready_for_recommendations:
            self.question_count += 1

        return {"type": "question", "response": response}

    async def on_message(self, user_input: str) -> Dict:
        """
        Process user input and return a structured response.
        """
        try:
            response = await self.chat(user_input)  # Ensure this is awaited
            
            from langchain_core.messages import AIMessage
            
            if response.get("type") == "recommendation":
                recommendations = response.get("response", [])
                if recommendations:
                    return {"messages": [AIMessage(content="RECOMMENDATION_DATA")], "recommendations": recommendations}
                else:
                    return {"messages": [AIMessage(content="I couldn't find any book recommendations at the moment. Please try again or provide more specific preferences.")]}
            
            elif response.get("type") in ["question", "system"]:
                content = response.get("response", "I'm here to help you with book recommendations!")
                return {"messages": [AIMessage(content=content)]}
            
            else:
                content = response.get("response", "I'm here to help you with book recommendations!")
                return {"messages": [AIMessage(content=content)]}
                
        except Exception as e:
            logging.error(f"Error in RecommendationAgent.on_message: {str(e)}")
            from langchain_core.messages import AIMessage
            return {"messages": [AIMessage(content=f"I'm sorry, I encountered an error while processing your request. Please try again.")]}


    def detect_refresh_request(self, user_input: str) -> bool:
        refresh_keywords = [
            "different", "other", "more", "another", "new", "fresh", 
            "change", "vary", "different books", "other books", "show me more",
            "what else", "anything else", "other options"
        ]
        user_lower = user_input.lower()
        return any(keyword in user_lower for keyword in refresh_keywords)

    def check_readiness(self, user_input: str) -> bool:
        sufficient_context = self.question_count >= self.MIN_QUESTIONS
        detailed_response = len(self.memory.chat_memory.messages) > 3
        
        # Check if user is directly requesting recommendations
        direct_request_keywords = [
            "recommend", "suggest", "show me", "i want", "looking for", 
            "find me", "books about", "books on", "horror books", "fantasy books",
            "romance books", "sci-fi books", "mystery books", "thriller books"
        ]
        
        user_input_lower = user_input.lower()
        direct_request = any(keyword in user_input_lower for keyword in direct_request_keywords)
        if direct_request:
            return True

        if "genre" in user_input_lower and self.question_count < self.MIN_QUESTIONS:
            self.ask_follow_up_questions(user_input)

        return sufficient_context or detailed_response

    def ask_follow_up_questions(self, response: str):
        """
        Adds follow-up questions based on user-provided information.
        """
        if "genre" in response.lower() and self.question_count < self.MIN_QUESTIONS:
            follow_up_question = (
                "What specific type within this genre do you enjoy reading?"
            )
            self.memory.chat_memory.add_ai_message(follow_up_question)
            self.question_count += 1

        if self.question_count == 3:
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


    async def recommend_books(self, user_input: str = "") -> List[Dict[str, Any]]:
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

                    Recommend 5 personalized books. Focus on contemporary popular books published after 2010 that are likely to be in modern book databases. Respond ONLY with a JSON array of objects. 
                    Each object must have these keys: 
                    - "Title": The book's full title (string) [X DO NOT ADD AUTHORS NAME]
                    - "ReasonForRecommendation": A brief explanation for the recommendation (string) 
                    - "Price": Price in dollars (without currency symbols) 

                    For horror specifically, consider: Fourth Wing, A Court of Thorns and Roses, Dune, and similar popular contemporary titles.
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

            if not processed_books:
                from backend.app.services.recommendation_service import get_trending_books, get_genre_specific_books
                try:
                    user_request = self.current_user_input.lower() if self.current_user_input else ""
                    
                    detected_genre = None
                    genre_keywords = {
                        "horror": ["horror", "scary", "frightening", "spooky"],
                        "fantasy": ["fantasy", "magic", "dragon", "wizard"],
                        "romance": ["romance", "love", "romantic"],
                        "sci-fi": ["sci-fi", "science fiction", "space", "futuristic"],
                        "mystery": ["mystery", "detective", "crime"],
                        "thriller": ["thriller", "suspense", "action"]
                    }
                    
                    for genre, keywords in genre_keywords.items():
                        if any(keyword in user_request for keyword in keywords):
                            detected_genre = genre
                            break
                    
                    if detected_genre:
                        if detected_genre not in self.genre_request_count:
                            self.genre_request_count[detected_genre] = 0
                        
                        offset = self.genre_request_count[detected_genre] * 15
                        self.genre_request_count[detected_genre] += 1
                        
                        fallback_books = await get_genre_specific_books(detected_genre, 15, offset)
                        self.last_recommended_genre = detected_genre
                    else:
                        fallback_books = await get_trending_books()
                        
                    display_limit = min(12, len(fallback_books))
                    total_available = len(fallback_books)
                    
                    
                    for book in fallback_books[:display_limit]:
                        processed_book = {
                            "title": book.get("title", "Unknown Title"),
                            "author": book.get("author", "Unknown Author"),
                            "Price": book.get("price", "9.99"),
                            "ReasonForRecommendation": self.get_recommendation_reason(detected_genre, book),
                            "pages": book.get("pages", "N/A"),
                            "release_year": book.get("release_year", "N/A"),
                            "image_url": book.get("image_url", "https://via.placeholder.com/100x150?text=No+Image"),
                            "rating": book.get("rating", "N/A"),
                            "description": book.get("description", "No description available.")
                        }
                        processed_books.append(processed_book)
                        
                except Exception as e:
                    pass

            return processed_books
        
        except Exception as e:
            pass
            return []

    def get_recommendation_reason(self, detected_genre: str, book: Dict) -> str:
        if not detected_genre:
            return "Popular book that matches your reading interests"
        
        request_count = self.genre_request_count.get(detected_genre, 1)
        
        # Dynamic reasons based on request count
        if request_count == 1:
            return f"Excellent {detected_genre} book that matches your preferences"
        elif request_count == 2:
            return f"Another fantastic {detected_genre} selection you might enjoy"
        elif request_count == 3:
            return f"Here's a different {detected_genre} book to explore"
        else:
            return f"More {detected_genre} variety for your reading list"

    def reset_state(self):
        self.memory.clear()
        self.recommendation_provided = False
        self.ready_for_recommendations = False
        self.recommended_books.clear()
        self.question_count = 0

    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Callable interface for langgraph compatibility.
        Processes the user input and returns the updated state with recommendations.
        """
        user_input = state.get('message', '')
        recommendations = self.recommend_books(user_input)
        state['recommendations'] = recommendations
        return state
