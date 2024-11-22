from sqlite3 import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from .models import Playlist, PlaylistReview, PlaylistVideo
from .serializers import PlaylistSerializer, PlaylistReviewSerializer, PlaylistVideoSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.db.models import Q


# 플레이리스트 조회 / 생성
# 나중에 페이지네이션추가하면될듯합니다
@api_view(['GET'])
@permission_classes([AllowAny])
def public_playlist_view(request):
    if request.user.is_authenticated:
        public_playlists = Playlist.objects.filter(is_public=True)
        user_playlists = Playlist.objects.filter(user=request.user)
        playlists = (public_playlists | user_playlists).distinct()
        # print('현재 사용자:', request.user)
        # print('플레이리스트:', playlists.values())  # 데이터베이스에서 실제 값 확인
    else:
        playlists = Playlist.objects.filter(is_public=True)
    
    serializer = PlaylistSerializer(playlists, many=True, context={'request': request})
    # print('직렬화된 데이터:', serializer.data)  # 직렬화된 결과 확인
    return Response(serializer.data)

# 플레이리스트 생성
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_playlist_view(request):
    print('FILES:', request.FILES)
    print('POST data:', request.POST)
    print('Request data:', request.data)
    
    serializer = PlaylistSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        print('Serializer valid data:', serializer.validated_data)
        instance = serializer.save(user=request.user)
        print('Saved instance:', instance, instance.cover_img)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    print('Serializer errors:', serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def playlist_detail_view(request, playlist_id):
    try:
        playlist = Playlist.objects.get(id=playlist_id)
        
        # GET 요청일 때는 공개 여부 확인
        if request.method == 'GET':
            if not playlist.is_public and playlist.user != request.user:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = PlaylistSerializer(playlist, context={'request': request})
            return Response(serializer.data)
            
        # PUT, DELETE는 소유자만
        if playlist.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
            
        if request.method == 'PUT':
            serializer = PlaylistSerializer(playlist, data=request.data, partial=True, context={'request': request})  # context 추가
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        elif request.method == 'DELETE':
            playlist.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
            
    except Playlist.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def playlist_video_view(request, playlist_id):
    try:
        if request.method == 'GET':
            playlist = Playlist.objects.get(
                Q(id=playlist_id) & 
                (Q(is_public=True) | Q(user=request.user))
            )
        else:
            # POST, DELETE는 소유자만
            playlist = Playlist.objects.get(id=playlist_id, user=request.user)
    except Playlist.DoesNotExist:
        return Response({'error': '플레이리스트를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        videos = PlaylistVideo.objects.filter(playlist=playlist).order_by('order_num')
        serializer = PlaylistVideoSerializer(videos, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # 마지막 order_num 가져오기
        last_video = PlaylistVideo.objects.filter(playlist=playlist).order_by('-order_num').first()
        next_order = (last_video.order_num + 1) if last_video else 1
        
        video_data = {
            'playlist': playlist,
            'video_id': request.data.get('video_id'),
            'title': request.data.get('title'),
            'thumbnail_url': request.data.get('thumbnail_url'),
            'published_at': request.data.get('published_at'),
            'order_num': next_order
        }
        
        try:
            playlist_video = PlaylistVideo.objects.create(**video_data)
            return Response(PlaylistVideoSerializer(playlist_video).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        video_id = request.query_params.get('video_id')  # URL 파라미터로 변경
        if not video_id:
            return Response({'error': 'video_id가 필요합니다.'}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            video = PlaylistVideo.objects.get(playlist=playlist, video_id=video_id)
            video.delete()
            
            # 순서 재정렬
            remaining_videos = PlaylistVideo.objects.filter(playlist=playlist).order_by('order_num')
            for index, video in enumerate(remaining_videos, 1):
                video.order_num = index
                video.save()
                
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PlaylistVideo.DoesNotExist:
            return Response({'error': '영상을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)



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
