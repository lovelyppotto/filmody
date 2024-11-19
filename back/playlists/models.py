from pyexpat import model
from django.db import models
from accounts.models import User
from movies.models import Movie

# Create your models here.
class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    cover_img = models.CharField(max_length=200)
    is_public = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_playlists', blank=True)

    class Meta:
        ordering = ['-created_at']
        
class PlayListMovies(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    order_num = models.IntegerField()

class PlaylistSong(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    spotify_id = models.CharField(max_length=255)
    song_title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255, blank=True)
    order_num = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class PlaylistReview(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_reviews', blank=True)