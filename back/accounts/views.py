from urllib import request
from django.conf import settings
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from .serializers import SignUpSerializer
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
    user.profile_image = 'images/default.png'
    user.save()
    return Response({'profile_image':  f'{settings.BASE_URL}/static/images/default.png'}, status=status.HTTP_200_OK)

# 프로필 상세 페이지 구현
@api_view(['GET'])
def user_profile_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    # 유저가 만든 플레이리스트
    user_playlists = Playlist.objects.filter(user=user)
    # 좋아요한 플레이리스트
    liked_playlists = Playlist.objects.filter(likes=user)
    # 좋아요한 영화 목록
    liked_movies = Movie.objects.filter(like_users=user)
    data = {
        'user_info': {
            'username': user.username,
            'nickname': user.nickname,
            'profile_image': user.profile_image.url if user.profile_image else None,
        },
        'playlists': PlaylistSerializer(user_playlists, many=True).data,
        'liked_playlists': PlaylistSerializer(liked_playlists, many=True).data,
        'liked_movies': MovieListSerializer(liked_movies, many=True).data
    }

    return Response(data, status=status.HTTP_200_OK)
    
from rest_framework.parsers import MultiPartParser, FormParser

# # 프로필 이미지 업데이트
# @api_view(['PATCH'])
# @permission_classes([IsAuthenticated])
# @parser_classes([MultiPartParser, FormParser])
# def update_profile_image(request):
#     user = request.user
    
#     if 'profile_image' not in request.FILES:
#         return Response({'error': '이미지 파일이 필요합니다.'}, status=status.HTTP_400_BAD_REQUEST)
    
#     # 기존 이미지가 있고 기본 이미지가 아니면 삭제
#     if user.profile_image and 'default.png' not in user.profile_image.name:
#         user.profile_image.delete(save=False)
    
#     # 새 이미지 저장
#     user.profile_image = request.FILES['profile_image']
#     user.save()
    
#     return Response({
#         'profile_image': request.build_absolute_uri(user.profile_image.url)
#     }, status=status.HTTP_200_OK)