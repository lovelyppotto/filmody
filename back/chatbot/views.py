from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import ConversationSerializer
import openai
from django.conf import settings

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chat_message(request):
    # 새로운 대화 생성 또는 기존 대화 가져오기
    conversation_id = request.data.get('conversation_id')
    if conversation_id:
        try:
            conversation = Conversation.objects.get(id=conversation_id, user=request.user)
        except Conversation.DoesNotExist:
            return Response({'error': '대화를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
    else:
        conversation = Conversation.objects.create(user=request.user)

    user_message = request.data.get('message')
    if not user_message:
        return Response({'error': '메시지가 필요합니다.'}, status=status.HTTP_400_BAD_REQUEST)

    # 사용자 메시지 저장
    Message.objects.create(
        conversation=conversation,
        content=user_message,
        is_bot=False
    )

    try:
        openai.api_key = settings.OPENAI_API_KEY
        response = openai.ChatCompletion.create(
            model="gpt-4-mini",  # GPT-4 mini 모델 지정
            messages=[{"role": "user", "content": user_message}],
            max_tokens=2000,     # 필요에 따라 조절 가능
            temperature=0.7      # 응답의 창의성 수준 (0-1)
        )
        
        bot_message = response.choices[0].message.content
        
        # 봇 응답 저장
        Message.objects.create(
            conversation=conversation,
            content=bot_message,
            is_bot=True
        )

        # 전체 대화 내용 반환
        serializer = ConversationSerializer(conversation)
        return Response(serializer.data)

    except Exception as e:
        return Response(
            {'error': f'GPT 응답 중 오류가 발생했습니다: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def conversation_list(request):
    conversations = Conversation.objects.filter(user=request.user)
    serializer = ConversationSerializer(conversations, many=True)
    return Response(serializer.data)