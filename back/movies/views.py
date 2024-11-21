from django.shortcuts import render, get_object_or_404
from pytz import timezone
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from yaml import serialize
from .serializers import MovieListSerializer, MovieDetailSerializer
from rest_framework.decorators import api_view, permission_classes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from .models import Movie, Director, BoxOffice
from django.db.models import Q

@extend_schema(
    summary="영화 목록 조회 및 검색",
    description="전체 영화 목록을 반환하며, 검색어가 있을 경우 영화 제목 또는 감독명으로 검색합니다.",
    parameters=[
        OpenApiParameter(
            name='search',
            type=OpenApiTypes.STR,
            description='검색어 (영화 제목 또는 감독명)',
            required=False
        ),
        OpenApiParameter(
            name='sort_by',
            type=OpenApiTypes.STR,
            description='정렬 기준 (rank, audience_acc, title)',
            required=False
        ),
        OpenApiParameter(
            name='order',
            type=OpenApiTypes.STR,
            description='정렬 방향 (asc, desc)',
            required=False
        )
    ],
    responses=MovieListSerializer,
    tags=['movies']
)
@api_view(['GET'])
def movie_list(request):
    movies = Movie.objects.all()
    
    # 정렬 처리
    sort_by = request.query_params.get('sort_by', 'rank')
    order = request.query_params.get('order', 'asc')
    
    if order == 'desc':
        sort_by = f'-{sort_by}'
    
    movies = movies.order_by(sort_by)
    
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)


# 영화 검색 기능 분리
@api_view(['GET'])
def movie_search(request):
    # 검색어 가져오는 변수
    search = request.query_params.get('search', '').strip()
    movies = Movie.objects.filter(
            Q(title__icontains=search) |  # 영화 제목으로 검색
            Q(director__name__icontains=search)  # 감독명으로 검색
        ).distinct().order_by('rank')  # distinct() 추가
    
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)


@extend_schema(
    summary="영화 상세 정보 조회",
    description="특정 영화의 상세 정보를 반환합니다.",
    parameters=[
        OpenApiParameter(
            name='movie_id',
            type=OpenApiTypes.INT,
            description='영화 ID',
            required=True,
            location=OpenApiParameter.PATH
        )
    ],
    responses=MovieDetailSerializer,
    tags=['movies']
)
@api_view(['GET'])
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    serializer = MovieDetailSerializer(movie, context={'request':request})
    return Response(serializer.data)

@api_view(['GET'])
def box_office(request):
    try:
        movies = Movie.objects.all().order_by('pk')[:10]
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def movie_likes(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    user = request.user

    # 이미 좋아요를 눌렀을 때
    if movie.like_users.filter(id=user.id).exists():
        movie.like_users.remove(user)
        liked = False
    else:
        movie.like_users.add(user)
        liked = True

    serializer = MovieDetailSerializer(movie, context={'request': request})
    data = {
        'liked':liked,
        'like_count':movie.like_users.count()
    }
    return Response(data) # 좋아요 상태랑 수를 응답 보냄

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def library_movies(request):
    user = request.user
    liked_movies = user.liked_movies.all()
    serializer = MovieListSerializer(liked_movies, many=True)
    return Response(serializer.data)