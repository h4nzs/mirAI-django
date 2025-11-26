from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('watchlist/', views.WatchlistPageView.as_view(), name='watchlist'),
    path('favorites/', views.FavoritesPageView.as_view(), name='favorites'),
]
