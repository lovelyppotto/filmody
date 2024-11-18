from django.db import models

# Create your models here.
class Movie(models.Model):
    rank = models.IntegerField()
    title = models.CharField(max_length=200)
    audience_acc = models.IntegerField()
    director = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    poster_url = models.URLField(max_length=500)
    plot = models.TextField()
    actors = models.CharField(max_length=500)
    production_year = models.CharField(max_length=4)
    show_time = models.CharField(max_length=10)
    nation = models.CharField(max_length=100)
    rating = models.CharField(max_length=100)
    created_at = models.DateField()