from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from services.tmdb import TMDBService
from services.ai_google import AIGoogleService
from movies.models import Watchlist

tmdb_service = TMDBService()
ai_service = AIGoogleService()

def home(request):
    """
    Renders the correct homepage based on authentication status.
    - Authenticated users see the main dashboard with personalized recommendations.
    - Unauthenticated users see the landing page.
    """
    if request.user.is_authenticated:
        # Logic for the authenticated user's dashboard
        trending_data = tmdb_service.get_trending_movies()
        ai_recommendations = []
        
        # Get AI recommendations based on the latest watchlist item
        latest_watchlist_item = Watchlist.objects.filter(user=request.user).first()
        if latest_watchlist_item:
            ai_suggestions = ai_service.suggest_similar_movies(latest_watchlist_item.title)
            if ai_suggestions and 'similar_movies' in ai_suggestions:
                # Fetch full details for each AI suggestion
                for suggestion in ai_suggestions['similar_movies'][:5]: # Limit to 5
                    if 'tmdb_id' in suggestion:
                        details = tmdb_service.get_movie_details(suggestion['tmdb_id'])
                        if details:
                            ai_recommendations.append(details)
        
        # If no AI recommendations could be generated (e.g., empty watchlist), show popular movies instead.
        if not ai_recommendations:
            popular_data = tmdb_service.get_popular_movies()
            if popular_data and 'results' in popular_data:
                ai_recommendations = popular_data['results'][:5]


        context = {
            'page_title': 'Dashboard',
            'trending_movies': trending_data.get('results', [])[:10] if trending_data else [],
            'ai_recommendations': ai_recommendations,
        }
        return render(request, 'pages/dashboard.html', context)
    else:
        # Show the public landing page
        return render(request, 'pages/landing.html')


class WatchlistPageView(LoginRequiredMixin, ListView):
    """
    Displays the movies in the currently logged-in user's watchlist.
    """
    model = Watchlist
    template_name = 'dashboard/watchlist.html'
    context_object_name = 'watchlist_items'

    def get_queryset(self):
        # Return the watchlist items for the current user
        return Watchlist.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'My Watchlist'
        return context


class FavoritesPageView(TemplateView):
    """
    Serves the user's favorites page. (Placeholder)
    """
    template_name = "dashboard/favorites.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'My Favorites'
        context['favorite_items'] = [] # Placeholder
        return context