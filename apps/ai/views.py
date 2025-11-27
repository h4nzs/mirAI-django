import json
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from services.ai_google import AIGoogleService
from services.tmdb import TMDBService

# An instance of our services
ai_service = AIGoogleService()
tmdb_service = TMDBService()

class ChatPageView(TemplateView):
    """
    A view to render the user-facing chat page UI.
    """
    template_name = "pages/chat.html"

@csrf_exempt
@require_POST
def chat_endpoint(request):
    """
    A view that acts as a JSON API endpoint for the AI service.
    It enriches AI recommendations with full movie details from TMDB.
    """
    try:
        data = json.loads(request.body)
        prompt = data.get('prompt')
        chat_type = data.get('type', 'general')

        if not prompt:
            return JsonResponse({'error': 'Prompt is required.'}, status=400)

        response_data = None
        if chat_type == 'recommendation':
            response_data = ai_service.get_recommendations(prompt)
        elif chat_type == 'similar':
            # Get initial suggestions from AI
            ai_suggestions = ai_service.suggest_similar_movies(prompt)
            
            # Enrich the suggestions with full TMDB details
            if ai_suggestions and 'similar_movies' in ai_suggestions:
                enriched_movies = []
                for movie_suggestion in ai_suggestions['similar_movies']:
                    if 'tmdb_id' in movie_suggestion:
                        # Fetch full details using the ID
                        movie_details = tmdb_service.get_movie_details(movie_suggestion['tmdb_id'])
                        if movie_details:
                            enriched_movies.append(movie_details)
                response_data = {'similar_movies': enriched_movies}
            else:
                response_data = ai_suggestions # Fallback if enrichment fails
        else: # 'general'
            response_data = ai_service.general_chat(prompt)

        if response_data:
            return JsonResponse(response_data)
        else:
            return JsonResponse({'error': 'Failed to get a response from the AI service.'}, status=500)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON in request body.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'}, status=500)