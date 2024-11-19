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
    director = models.ForeignKey(Director, on_delete=models.CASCADE, related_name='movies')
    genre = models.CharField(max_length=100)
    poster_url = models.CharField(max_length=500)
    plot = models.TextField()
    actors = models.CharField(max_length=200)
    open_year = models.CharField(max_length=4)
    nation = models.CharField(max_length=50)
    rating = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)


class BoxOffice(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rank_date = models.DateField()
    rank = models.IntegerField()
