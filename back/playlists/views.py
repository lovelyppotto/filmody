from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from .models import Playlist
from .serializers import PlaylistSerializer, PlaylistCreateSerializer
from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def search_movie_ost(request):
    movie_title = request.query_params.get('title')
    # 임시로 하드코딩된 결과 반환
    return Response({
        'tracks': [
            {'name': 'Sample OST 1', 'artist': 'Artist 1'},
            {'name': 'Sample OST 2', 'artist': 'Artist 2'},
        ]
    })

# class PlaylistViewSet(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     serializer_class = PlaylistSerializer

#     def get_queryset(self):
#         return Playlist.objects.filter(user=self.request.user)

#     def create(self, request):
#         serializer = PlaylistCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             try:
#                 # Spotify API 설정
#                 sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
#                     client_id=settings.SPOTIFY_CLIENT_ID,
#                     client_secret=settings.SPOTIFY_CLIENT_SECRET,
#                     redirect_uri="http://127.0.0.1:8000",
#                     scope="playlist-modify-public"
#                 ))

#                 # 영화 OST 검색
#                 movie_title = serializer.validated_data['movie_title']
#                 search_query = f"{movie_title} soundtrack"
#                 results = sp.search(q=search_query, type="track", limit=10)

#                 # Spotify 플레이리스트 생성
#                 spotify_playlist = sp.user_playlist_create(
#                     user=sp.current_user()["id"],
#                     name=f"{movie_title} OST Playlist",
#                     public=True
#                 )

#                 # 검색된 트랙 추가
#                 track_uris = [track["uri"] for track in results["tracks"]["items"]]
#                 sp.playlist_add_items(spotify_playlist["id"], track_uris)

#                 # DB에 플레이리스트 저장
#                 playlist = Playlist.objects.create(
#                     name=serializer.validated_data['name'],
#                     user=request.user,
#                     spotify_playlist_id=spotify_playlist["id"]
#                 )

#                 return Response(
#                     PlaylistSerializer(playlist).data,
#                     status=status.HTTP_201_CREATED
#                 )

#             except Exception as e:
#                 return Response(
#                     {'error': str(e)},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )

#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )

#     @action(detail=True, methods=['post'])
#     def add_tracks(self, request, pk=None):
#         playlist = self.get_object()
#         track_uris = request.data.get('track_uris', [])
        
#         try:
#             sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
#                 client_id=settings.SPOTIFY_CLIENT_ID,
#                 client_secret=settings.SPOTIFY_CLIENT_SECRET,
#                 redirect_uri="http://127.0.0.1:8000",
#                 scope="playlist-modify-public"
#             ))
            
#             sp.playlist_add_items(playlist.spotify_playlist_id, track_uris)
#             return Response({'status': 'tracks added'})
#         except Exception as e:
#             return Response(
#                 {'error': str(e)},
#                 status=status.HTTP_400_BAD_REQUEST
#             )