from rest_framework import serializers
from .models import Playlist, PlaylistReview, PlaylistVideo

class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ['id', 'title', 'cover_img', 'is_public', 'created_at', 'updated_at']
        read_only_fields = ['user']

    def get_cover_img(self, obj):
        request = self.context.get('request')
        if obj.cover_img:
            return request.build_absolute_uri(obj.cover_img.url)
        return None

class PlaylistReviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = PlaylistReview
        fields = ['id', 'user', 'content', 'created_at', 'updated_at']
        read_only_fields = ['user', 'playlist']

    def get_user(self, obj):
        return obj.user.nickname # 유저 nickname만 반환
    
class PlaylistVideoSerializer(serializers.ModelSerializer):
   class Meta:
       model = PlaylistVideo
       fields = ['id', 'video_id', 'title', 'thumbnail_url', 'order_num']
       read_only_fields = ['id', 'order_num']