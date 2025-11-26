from django.urls import path
from . import views

app_name = 'ai'

urlpatterns = [
    # The API endpoint for all AI chat functionalities
    path('chat/', views.chat_endpoint, name='chat'),
]
