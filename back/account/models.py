from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    # 닉네임 필드 추가
    nickname = models.CharField(max_length=10)