from django.contrib import admin
from django.urls import path
from .views import DeleteAccountView, SignUpView

urlpatterns = [
    path('delete/',DeleteAccountView.as_view(),name='delete-account'),
    path('signup/', SignUpView.as_view(), name='signup'),
]
