from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup,),
    path('delete/', views.delete_account,),
    path('profile-image/', views.delete_profile_image)
]
