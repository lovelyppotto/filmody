from urllib import request
from django.conf import settings
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from .serializers import SignUpSerializer

@api_view(['POST'])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_account(request):
    user = request.user
    password = request.data.get('password')

    # 비밀번호 검증
    if not user.check_password(password):
        return Response({'error':'비밀번호가 올바르지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
    
    # 계정 삭제
    user.delete()
    return Response({'message':'회원 탈퇴가 완료되었습니다.'}, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_profile_image(request):
    user = request.user
    if user.profile_image and 'default.png' not in user.profile_image.name:
        user.profile_image.delete(save=False)
    user.profile_image = 'images/default.png'
    user.save()
    return Response({'profile_image':  f'{settings.BASE_URL}/static/images/default.png'}, status=status.HTTP_200_OK)