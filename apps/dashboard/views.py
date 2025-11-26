from django.shortcuts import render
from django.views.generic import TemplateView
from services.tmdb import TMDBService

# Create your views here.
tmdb_service = TMDBService()

class HomePageView(TemplateView):
    """
    Serves the main dashboard homepage.
    This view now fetches dynamic data for the movie shelves,
    mimicking the original application's dashboard.
    """
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Welcome to MirAI'
        
        trending_data = tmdb_service.get_trending_movies()
        context['trending_movies'] = trending_data.get('results', [])[:10] if trending_data else []
        
        return context

class WatchlistPageView(TemplateView):
    """
    Serves the user's watchlist page. (Placeholder)
    """
    template_name = "dashboard/watchlist.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'My Watchlist'
        context['watchlist_items'] = [] # Placeholder
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