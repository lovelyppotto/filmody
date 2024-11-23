from django.urls import path
from . import views

urlpatterns = [
    path('message/', views.chat_message, name='chat_message'),
    path('conversations/', views.conversation_list, name='conversation_list'),
]