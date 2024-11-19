from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Playlist, PlaylistReview, PlaylistVideo
from .serializers import PlaylistSerializer, PlaylistReviewSerializer, PlaylistVideoSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter


# 플레이리스트 조회 / 생성
# 나중에 페이지네이션추가하면될듯합니다
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def playlist_view(request):
    if request.method == 'POST':
        serializer = PlaylistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'GET':
        public_playlists = Playlist.objects.filter(is_public=True)
        user_playlists = Playlist.objects.filter(user=request.user)
        playlists = public_playlists | user_playlists
        
        serializer = PlaylistSerializer(playlists, many=True)
        return Response(serializer.data)
    

@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def add_video(request, playlist_id):
    # 플레이리스트 영상 추가하는 뷰 함수
    try:
        playlist = Playlist.objects.get(id=playlist_id, user=request.user)
        
        # 현재 플레이리스트의 마지막 order_num 가져오기
        last_video = PlaylistVideo.objects.filter(playlist=playlist).order_by('-order_num').first()
        next_order = (last_video.order_num + 1) if last_video else 1
        
        video_data = {
            'playlist': playlist,
            'video_id': request.data.get('video_id'),
            'title': request.data.get('title'),
            'thumbnail_url': request.data.get('thumbnail_url'),
            'order_num': next_order
        }
        
        playlist_video = PlaylistVideo.objects.create(**video_data)
        return Response(PlaylistVideoSerializer(playlist_video).data, status=status.HTTP_201_CREATED)
        
    except Playlist.DoesNotExist:
        return Response({'error': '플레이리스트를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_video(request, playlist_id, video_id):
    try:
        # 특정 플레이리스트 및 내부 영상 찾기
        playlist_video = PlaylistVideo.objects.get(
            playlist_id=playlist_id, 
            video_id=video_id,
            # __: 외래키 연관 모델 필드 필터링, 조인과 필드 탐색 위해 사용
            playlist__user=request.user  # 현재 사용자의 플레이리스트인지 확인
        )
        
        # 영상 삭제
        playlist_video.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    except PlaylistVideo.DoesNotExist:
        return Response(
            {"detail": "해당 영상을 찾을 수 없습니다."}, 
            status=status.HTTP_404_NOT_FOUND
        )


# 리뷰 생성, 수정, 삭제 처리
@api_view(['POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def review_manage(request, playlist_id):
    """
    POST: 새 리뷰 생성
    PUT: 기존 리뷰 수정
    DELETE: 리뷰 삭제
    """
    # 플레이리스트 존재 여부 확인
    try:
        playlist = Playlist.objects.get(id=playlist_id)
    except Playlist.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        # 새 리뷰 생성
        serializer = PlaylistReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, playlist=playlist)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 기존 리뷰 존재 여부 확인 (수정/삭제)
    try:
        review = PlaylistReview.objects.get(user=request.user, playlist=playlist)
    except PlaylistReview.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        # 리뷰 수정
        serializer = PlaylistReviewSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # 리뷰 삭제
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def playlist_reviews(request, playlist_id):
    # 특정 플레이리스트의 모든 리뷰를 조회하는 뷰 함수
    # 리뷰는... 비동기로 계속 밑으로 내려가게 하면 되지않을까?
    try:
        playlist = Playlist.objects.get(id=playlist_id)
        reviews = PlaylistReview.objects.filter(playlist=playlist)
        serializer = PlaylistReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    except Playlist.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


# 플레이리스트 좋아요/좋아요 취소
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_like(request, playlist_id):
    try:
        playlist = Playlist.objects.get(id=playlist_id)
        
        if request.user in playlist.likes.all():
            playlist.likes.remove(request.user)
            liked = False
        else:
            playlist.likes.add(request.user)
            liked = True
            
        return Response({
            'liked': liked,
            'likes_count': playlist.likes.count()
        })
        
    except Playlist.DoesNotExist:
        return Response({'error': '플레이리스트를 찾을 수 없습니다.'}, 
                      status=status.HTTP_404_NOT_FOUND)
