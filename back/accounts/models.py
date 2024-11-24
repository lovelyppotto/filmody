from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    # 닉네임 필드 추가
    nickname = models.CharField(max_length=10)
    # 정보 수정 페이지에서 리뷰 볼 지 말 지 선택할 수 있도록 추가
    show_reviews = models.BooleanField(default=True)
    profile_image = models.ImageField(
        upload_to='profile_images/',
        default='images/default.png',
        verbose_name=' '
    )
    # 팔로우
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following')

