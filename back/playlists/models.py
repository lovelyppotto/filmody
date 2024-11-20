from django.db import models
from django.contrib.auth.models import User
from movies.models import Movie
from django.conf import settings

class Playlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='playlists')
    title = models.CharField(max_length=50)
    cover_img = models.ImageField(upload_to='uploads/', blank=True, null=True)
    is_public = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_playlists', blank=True)  

    class Meta:
        ordering = ['-created_at']

class PlayListMovies(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    order_num = models.IntegerField()

# 플레이리스트에 속한 영상 관리
class PlaylistVideo(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    video_id = models.CharField(max_length=20)
    title = models.CharField(max_length=255)
    thumbnail_url = models.CharField(max_length=200)
    order_num = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order_num']

# 플레이리스트 리뷰 모델
class PlaylistReview(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_review', blank=True)

    class Meta:
        ordering = ['-created_at']
        # 사용자당 리뷰 하나로 제한(도배금지)
        unique_together = ['user', 'playlist']