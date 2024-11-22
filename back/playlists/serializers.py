from rest_framework import serializers
from .models import Playlist, PlaylistReview, PlaylistVideo

class PlaylistSerializer(serializers.ModelSerializer):
    cover_img = serializers.ImageField(required=False)
    user = serializers.PrimaryKeyRelatedField(source='user.id', read_only=True)
    user_nickname = serializers.CharField(source='user.nickname', read_only=True)  # 추가
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
       model = Playlist 
       fields = ['id', 'title', 'cover_img', 'is_public', 'created_at', 'updated_at', 'user', 'user_nickname', 'likes_count', 'is_liked']
       read_only_fields = ['user']

    def get_cover_img(self, obj):
        if obj.cover_img:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.cover_img.url)
        return None

    def create(self, validated_data):
        print('Validated data:', validated_data)
        instance = super().create(validated_data)
        print('Created instance:', instance, instance.cover_img)
        return instance
   
    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user in obj.likes.all()
        return False
    
    

class PlaylistReviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()  # 추가

    class Meta:
        model = PlaylistReview
        fields = ['id', 'user', 'content', 'created_at', 'updated_at', 'is_liked', 'likes_count', 'is_owner']
        read_only_fields = ['user', 'playlist']

    def get_user(self, obj):
        return obj.user.nickname
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False
    
    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_is_owner(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj
    
    
class PlaylistVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaylistVideo
        fields = ['id', 'video_id', 'title', 'thumbnail_url', 'order_num', 'published_at']
        read_only_fields = ['id', 'order_num']