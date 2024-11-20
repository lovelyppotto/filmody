from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from .serializers import SignUpSerializer


class SignUpView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request):
        user = request.user
        password = request.data.get('password')

        # 비밀번호 검증
        if not user.check_password(password):
            return Response({"error":"비밀번호가 올바르지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        # 계정 삭제
        user.delete()
        return Response({"message":"회원 탈퇴가 완료되었습니다."}, status=status.HTTP_200_OK)