from tkinter import CASCADE
from django.db import models
from accounts.models import User

# movies/models.py

class Movie(models.Model):
    rank = models.IntegerField()                    # 순위
    title = models.CharField(max_length=200)        # 영화명
    audience_acc = models.IntegerField()            # 관객수 
    director = models.CharField(max_length=200)     # 감독명
    genre = models.CharField(max_length=100)        # 장르
    poster_url = models.URLField(max_length=500)    # 포스터
    plot = models.TextField()                       # 줄거리
    actors = models.CharField(max_length=500)       # 배우
    open_year = models.CharField(max_length=4)      # 개봉년도
    nation = models.CharField(max_length=100)       # 국가
    rating = models.CharField(max_length=100)       # 평점
    created_at = models.DateField()                 # 등록일
    likes = models.ManyToManyField(User, related_name='liked_movies', blank=True)

class BoxOffice(models.Model):
    movie = models.ForeignKey(Movie, on_delete=CASCADE)
    rank_date = models.DateField()
    rank = models.IntegerField()
