from sqlite3 import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from yaml import serialize
from .models import Playlist, PlaylistReview, PlaylistVideo
from .serializers import PlaylistSerializer, PlaylistReviewSerializer, PlaylistVideoSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.db.models import Q


# 플레이리스트 조회 / 생성
# 나중에 페이지네이션추가하면될듯합니다
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def playlist_view(request):
    if request.method == 'POST':
        print('FILES:', request.FILES)
        print('POST data:', request.POST)
        print('Request data:', request.data)  # 추가
        
        serializer = PlaylistSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            print('Serializer valid data:', serializer.validated_data)  # 추가
            instance = serializer.save(user=request.user)
            print('Saved instance:', instance, instance.cover_img)  # 추가
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        print('Serializer errors:', serializer.errors)  # 추가
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'GET':
        public_playlists = Playlist.objects.filter(is_public=True)
        user_playlists = Playlist.objects.filter(user=request.user)
        playlists = public_playlists | user_playlists
        
        serializer = PlaylistSerializer(playlists, many=True, context={'request': request})
        return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def playlist_detail_view(request, playlist_id):
    try:
        # 공개 플레이리스트이거나 본인의 플레이리스트만 조회 가능
        playlist = Playlist.objects.get(
            Q(id=playlist_id) & 
            (Q(is_public=True) | Q(user=request.user))
        )
    except Playlist.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PlaylistSerializer(playlist)
        return Response(serializer.data)
    
    # 본인의 플레이리스트만 수정/삭제 가능
    if playlist.user != request.user:
        return Response(status=status.HTTP_403_FORBIDDEN)

    if request.method == 'PUT':
        serializer = PlaylistSerializer(playlist, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        playlist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def playlist_video_view(request, playlist_id):
    try:
        playlist = Playlist.objects.get(id=playlist_id, user=request.user)
    except Playlist.DoesNotExist:
        return Response({'error': '플레이리스트를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        # 마지막 order_num 가져오기
        last_video = PlaylistVideo.objects.filter(playlist=playlist).order_by('-order_num').first()
        next_order = (last_video.order_num + 1) if last_video else 1
        
        # 프론트엔드에서 보내는 데이터 구조에 맞게 수정
        video_data = {
            'playlist': playlist,
            'video_id': request.data.get('video_id'),
            'title': request.data.get('title'),
            'description': request.data.get('description', ''),  # description 필드 추가
            'thumbnail_url': request.data.get('thumbnail_url'),
            'order_num': next_order
        }
        
        try:
            playlist_video = PlaylistVideo.objects.create(**video_data)
            return Response(PlaylistVideoSerializer(playlist_video).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        video_id = request.data.get('video_id')
        if not video_id:
            return Response({'error': 'video_id가 필요합니다.'}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            video = PlaylistVideo.objects.get(playlist=playlist, id=video_id)
            video.delete()
            
            # 순서 재정렬
            remaining_videos = PlaylistVideo.objects.filter(playlist=playlist).order_by('order_num')
            for index, video in enumerate(remaining_videos, 1):
                video.order_num = index
                video.save()
                
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PlaylistVideo.DoesNotExist:
            return Response({'error': '영상을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        

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
            try:
                serializer.save(user=request.user, playlist=playlist)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response(
                    {'error': '이미 해당 플레이리스트의 리뷰를 작성하셨습니다.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def review_toggle_like(request, playlist_id, review_id):
    try:
        review = PlaylistReview.objects.get(
            id=review_id,
            playlist_id=playlist_id
        )
    except PlaylistReview.DoesNotExist:
        return Response({"error": "리뷰를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

    # is_owner 체크 부분 제거

    # 좋아요 토글
    if review.likes.filter(id=request.user.id).exists():
        review.likes.remove(request.user)
        is_liked = False
    else:
        review.likes.add(request.user)
        is_liked = True
    
    return Response({
        'is_liked': is_liked,
        'likes_count': review.likes.count()
    })


# 플레이리스트 좋아요/좋아요 취소
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def playlist_toggle_like(request, playlist_id):
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
