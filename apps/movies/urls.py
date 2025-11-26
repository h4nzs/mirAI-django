from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    # Example: /movies/
    path('', views.discover_movies_view, name='list'),
    
    # Example: /movies/search/?query=inception
    path('search/', views.search_view, name='search'),

    # Example: /movies/trending/
    path('trending/', views.trending_movies_view, name='trending'),
    
    # Example: /movies/27205/
    path('<int:movie_id>/', views.movie_detail_view, name='detail'),
]
