from urllib import request
from django.conf import settings
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from .serializers import SignUpSerializer, ProfileSerializer
from .models import User
from playlists.models import Playlist
from playlists.serializers import PlaylistSerializer
from movies.models import Movie
from movies.serializers import MovieListSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import parser_classes

# 회원가입
@api_view(['POST'])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 회원 탈퇴
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_account(request):
    user = request.user
    password = request.data.get('password')

    # 비밀번호 검증
    if not user.check_password(password):
        return Response({'error':'비밀번호가 올바르지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
    
    # 계정 삭제
    user.delete()
    return Response({'message':'회원 탈퇴가 완료되었습니다.'}, status=status.HTTP_200_OK)

# 프로필 사진 삭제
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_profile_image(request):
    user = request.user
    if user.profile_image and 'default.png' not in user.profile_image.name:
        user.profile_image.delete(save=False)
    user.profile_image = 'static/images/default.png'
    user.save()
    return Response({'profile_image':  f'{settings.BASE_URL}/static/images/default.png'}, status=status.HTTP_200_OK)

# 프로필 상세 페이지 구현
@api_view(['GET'])
def user_profile_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)

    # ProfileSerializer를 사용하여 user_info 직렬화
    profile_serializer = ProfileSerializer(user, context={'request': request})

    # 유저가 만든 플레이리스트
    user_playlists = Playlist.objects.filter(user=user)
    # 좋아요한 플레이리스트
    liked_playlists = Playlist.objects.filter(likes=user)
    # 좋아요한 영화 목록
    liked_movies = Movie.objects.filter(like_users=user)

    data = {
        'user_info': profile_serializer.data,
        'playlists': PlaylistSerializer(user_playlists, many=True).data,
        'liked_playlists': PlaylistSerializer(liked_playlists, many=True).data,
        'liked_movies': MovieListSerializer(liked_movies, many=True).data
    }

    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def follow(request, user_id):
    target = get_object_or_404(User, id=user_id)
    
    # 자신을 팔로우하는 것 방지
    if request.user == target:
        return Response(
            {'error': '자신을 팔로우할 수 없습니다.'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if request.method == 'POST':
        # 이미 팔로우한 경우
        if request.user in target.followers.all():
            target.followers.remove(request.user)
            return Response({'status': 'unfollowed'})
        else:
            target.followers.add(request.user)
            return Response({'status': 'followed'})
    
    serializer = ProfileSerializer(target, context={'request': request})
    return Response(serializer.data)