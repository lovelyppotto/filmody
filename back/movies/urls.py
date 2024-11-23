from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_list), 
    path('search/', views.movie_search),
    path('<int:movie_id>/', views.movie_detail),
    path('recommend/', views.box_office),
    path('<int:movie_id>/like/', views.movie_likes),
    path('library/movies/', views.library_movies),
]