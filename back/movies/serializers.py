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
        fields = ('name',)

class MovieListSerializer(serializers.ModelSerializer):
    # 정렬 및 필터링에 필요한 정보
    class Meta:
        model = Movie
        fields = (
            'id',
            'rank',
            'title',
            'audience_acc',
            'genre',
            'open_year',
        )

class MovieDetailSerializer(serializers.ModelSerializer):
    # 세부 정보에 넘길 내역들
    director = DirectorSerializer(read_only=True)  # 감독 이름만 표시
    
    class Meta:
        model = Movie
        fields = (
            'id',
            'title',
            'director',
            'genre',
            'plot',
            'open_year',
        )