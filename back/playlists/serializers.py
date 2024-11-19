from rest_framework import serializers
# from .models import 

from rest_framework import serializers
from .models import Playlist

class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ['id', 'name', 'spotify_playlist_id', 'created_at', 'updated_at']
        read_only_fields = ['user']

class PlaylistCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    movie_title = serializers.CharField(max_length=200)