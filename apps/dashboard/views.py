from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from services.tmdb import TMDBService
from movies.models import Watchlist

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