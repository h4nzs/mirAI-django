from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

class HomePageView(TemplateView):
    """
    Serves the main dashboard homepage.
    This view will eventually pass dynamic data to the template, such as
    trending movies or personalized recommendations.
    """
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'MirAI Dashboard'
        # Placeholder for future dynamic content
        context['trending_movies'] = [] 
        context['for_you_movies'] = []
        return context

class WatchlistPageView(TemplateView):
    """
    Serves the user's watchlist page. (Placeholder)
    This view will fetch the user's saved movies.
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
    This view will fetch the user's favorite movies.
    """
    template_name = "dashboard/favorites.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'My Favorites'
        context['favorite_items'] = [] # Placeholder
        return context