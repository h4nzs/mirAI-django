import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from services.ai_google import AIGoogleService

# An instance of our AI service
ai_service = AIGoogleService()

@csrf_exempt
@require_POST
def chat_endpoint(request):
    """
    A view that acts as a JSON API endpoint for the AI service.
    It expects a POST request with a JSON body containing 'prompt' and 'type'.
    
    'type' can be one of: 'recommendation', 'similar', 'general'.
    """
    try:
        data = json.loads(request.body)
        prompt = data.get('prompt')
        chat_type = data.get('type', 'general')

        if not prompt:
            return JsonResponse({'error': 'Prompt is required.'}, status=400)

        response_data = None
        if chat_type == 'recommendation':
            # For queries like "find movies similar to..."
            response_data = ai_service.get_recommendations(prompt)
        elif chat_type == 'similar':
            # For a single movie title to find similar ones
            response_data = ai_service.suggest_similar_movies(prompt)
        else: # 'general'
            # For general conversation
            response_data = ai_service.general_chat(prompt)

        if response_data:
            return JsonResponse(response_data)
        else:
            return JsonResponse({'error': 'Failed to get a response from the AI service.'}, status=500)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON in request body.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'}, status=500)