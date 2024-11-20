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
        )

class BoxOfficeSerializer(serializers.ModelSerializer):
    movie = MovieListSerializer(read_only=True)

    class Meta:
        model = BoxOffice
        fields = [
            'rank',
            'rank_date',
            'movie'
        ]
