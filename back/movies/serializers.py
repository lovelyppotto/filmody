from pyexpat import model
from rest_framework import serializers
from dataclasses import fields
from .models import Movie, BoxOffice, Director

class MovietitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('title',)


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ('id', 'name',)

class MovieListSerializer(serializers.ModelSerializer):
    director = DirectorSerializer(many=True, read_only=True)
    # 정렬 및 필터링에 필요한 정보
    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'director', 'genre', 
            'open_year', 'rating', 'poster_url'
        ]

class MovieDetailSerializer(serializers.ModelSerializer):
    # 세부 정보에 넘길 내역들
    like_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    director = DirectorSerializer(many=True, read_only=True)
    class Meta:
        model = Movie
        fields = (
            'id',
            'title',
            'director',
            'genre',
            'plot',
            'open_year',
            'poster_url',
            'like_count',
            'is_liked'
        )
    
    def get_like_count(self, obj):
        return obj.get_like_count()
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        print(request)
        print(
            request.user)
        print(obj.like_users.filter(pk=request.user.pk).exists())
        if request and request.user.is_authenticated:
            return obj.like_users.filter(pk=request.user.pk).exists()
        return False

class BoxOfficeSerializer(serializers.ModelSerializer):
    movie = MovieListSerializer(read_only=True)

    class Meta:
        model = BoxOffice
        fields = [
            'rank',
            'rank_date',
            'movie'
        ]
