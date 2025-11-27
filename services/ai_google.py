import os
import json
import logging
import google.generativeai as genai
from dotenv import load_dotenv
from typing import Dict, Any, Optional

# --- Setup ---
# Load environment variables from .env file located at the project root.
load_dotenv()

# Configure logging to display informational messages.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Constants ---
# Retrieve the Google AI API key from environment variables.
GOOGLE_AI_API_KEY = os.getenv("GOOGLE_AI_API_KEY")

# --- Service Class ---
class AIGoogleService:
    """
    A service class for interacting with the Google AI (Gemini) API.
    This service is responsible for handling all AI-powered features,
    such as movie recommendations and chat.
    """

    def __init__(self):
        """
        Initializes the AIGoogleService, configures the API key, and sets up
        the generative models.
        """
        if not GOOGLE_AI_API_KEY:
            logger.error("GOOGLE_AI_API_KEY environment variable not set.")
            raise ValueError("GOOGLE_AI_API_KEY must be set in your environment.")
        
        genai.configure(api_key=GOOGLE_AI_API_KEY)
        
        # Model configured to specifically return JSON for structured data needs.
        self.json_model = genai.GenerativeModel(
            'gemini-flash-latest',
            generation_config={"response_mime_type": "application/json"}
        )
        
        # A separate model instance for handling general, freeform chat.
        self.chat_model = genai.GenerativeModel('gemini-flash-latest')

    def _generate_json_response(self, prompt: str) -> Optional[Dict[str, Any]]:
        """
        A private helper method to generate content and parse the JSON response.

        Args:
            prompt (str): The prompt to send to the generative model.

        Returns:
            Optional[Dict[str, Any]]: A Python dictionary parsed from the JSON response,
                                      or None if an error occurs.
        """
        try:
            response = self.json_model.generate_content(prompt)
            # The response text is expected to be a valid JSON string.
            return json.loads(response.text)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON from AI response: {e}")
            raw_text = getattr(response, 'text', 'N/A')
            logger.error(f"Raw AI response was: {raw_text}")
            return None
        except Exception as e:
            logger.error(f"An unexpected error occurred with Google AI API: {e}")
            return None

    def get_recommendations(self, movie_query: str) -> Optional[Dict[str, Any]]:
        """
        Generates movie recommendations based on a natural language query from a user.

        Args:
            movie_query (str): The user's request (e.g., "movies like Blade Runner").

        Returns:
            A dictionary containing a list of recommended movies, or None.
        """
        prompt = f"""
        You are a movie recommendation expert named MirAI.
        A user is looking for movies. Their request is: "{movie_query}".
        
        Analyze the user's request and provide 5 relevant movie recommendations.
        For each movie, include the title, estimated year of release, and a brief, compelling reason for the recommendation.
        
        Your response MUST be a valid JSON object with a single key "recommendations".
        The value of "recommendations" must be an array of objects, where each object has the keys "title", "year", and "reason".
        
        Example response format:
        {{
          "recommendations": [
            {{
              "title": "Example Movie 1",
              "year": 2021,
              "reason": "This movie fits your request because of its similar themes and visual style."
            }}
          ]
        }}
        """
        return self._generate_json_response(prompt)

    def suggest_similar_movies(self, movie_title: str) -> Optional[Dict[str, Any]]:
        """
        Suggests movies that are similar to a given movie title.

        Args:
            movie_title (str): The title of the movie to find similarities for.

        Returns:
            A dictionary containing a list of similar movies, or None.
        """
        prompt = f"""
        You are a movie recommendation expert named MirAI.
        A user wants to find movies that are similar to "{movie_title}".
        
        Provide a list of 5 movies that are similar in genre, theme, or style.
        IMPORTANT: You must find the correct TMDB ID for each movie.
        
        Your response MUST be a valid JSON object with a single key "similar_movies".
        The value must be an array of objects, each with a "title", "year", and "tmdb_id".
        
        Example response format:
        {{
          "similar_movies": [
            {{ "title": "Similar Movie 1", "year": 2020, "tmdb_id": 12345 }},
            {{ "title": "Similar Movie 2", "year": 2018, "tmdb_id": 67890 }}
          ]
        }}
        """
        return self._generate_json_response(prompt)

    def general_chat(self, prompt: str) -> Optional[Dict[str, Any]]:
        """
        Handles general, non-structured chat with the user, acting as a friendly AI assistant.

        Args:
            prompt (str): The user's chat message.

        Returns:
            A dictionary containing the AI's text response, or None.
        """
        full_prompt = f"""
        You are a helpful and friendly movie-loving assistant named MirAI.
        Engage in a friendly and conversational way with the user. Do not try to output JSON.
        
        User's message: "{prompt}"
        """
        try:
            response = self.chat_model.generate_content(full_prompt)
            # We return a dict to maintain a consistent return type across the service.
            return {"response": response.text}
        except Exception as e:
            logger.error(f"An unexpected error occurred during general chat: {e}")
            return None

# --- Example Usage (for direct testing of this script) ---
# if __name__ == '__main__':
#     if not GOOGLE_AI_API_KEY:
#         print("Please set the GOOGLE_AI_API_KEY environment variable in a .env file to run tests.")
#     else:
#         ai_service = AIGoogleService()

#         # --- Test recommendations ---
#         recs = ai_service.get_recommendations("I want a funny sci-fi movie that doesn't take itself too seriously.")
#         if recs:
#             print("--- Recommendations ---")
#             print(json.dumps(recs, indent=2))

#         # --- Test similar movies ---
#         similar = ai_service.suggest_similar_movies("The Matrix")
#         if similar:
#             print("\n--- Similar Movies ---")
#             print(json.dumps(similar, indent=2))
        
#         # --- Test general chat ---
#         chat_resp = ai_service.general_chat("What was the best movie of the 1990s?")
#         if chat_resp:
#             print("\n--- General Chat ---")
#             print(chat_resp['response'])
