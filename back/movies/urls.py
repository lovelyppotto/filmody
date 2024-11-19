from django.urls import path
from .views import MovieListAPI, MovieDetailAPI

urlpatterns = [
    path('', MovieListAPI.as_view()),
    path('<int:movie_id>/', MovieDetailAPI.as_view()),
]