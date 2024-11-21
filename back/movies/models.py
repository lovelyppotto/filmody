from django.conf import settings
from django.db import models
from accounts.models import User

# movies/models.py

from django.db import models

class Director(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Movie(models.Model):
    rank = models.IntegerField()
    title = models.CharField(max_length=100)
    audience_acc = models.IntegerField()
    director = models.ManyToManyField(Director, related_name='movies')
    genre = models.CharField(max_length=100)
    poster_url = models.CharField(max_length=500)
    plot = models.TextField()
    actors = models.CharField(max_length=200)
    open_year = models.CharField(max_length=4)
    nation = models.CharField(max_length=50)
    rating = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    # 해당 영화에 좋아요 누른 유저들
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_movies', blank=True)

    # 좋아요 수 카운트
    def get_like_count(self):
        return self.like_users.count()
    
    # 좋아요 눌렀는지
    def get_is_liked(self, user):
        return self.like_users.filter(id=user.id).exists()

class BoxOffice(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rank_date = models.DateField()
    rank = models.IntegerField()
