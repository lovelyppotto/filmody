<!-- components/ChatBotModal.vue -->
<template>
  <div class="modal-backdrop" @click.self="$emit('close')">
    <div class="chat-interface">
      <div class="modal-header">
        <h3>Recommend ChatBot</h3>
        <button class="close-button" @click="$emit('close')">×</button>
      </div>
      <div class="chat-area">
        <!-- 기존 내용 -->
        <div class="messages" ref="messageContainer">
          <div 
            v-for="(message, index) in store.messages" 
            :key="index"
            :class="['message', message.is_bot ? 'bot' : 'user']"
          >
            {{ message.content }}
          </div>
        </div>
        <div class="input-area">
          <input 
            v-model="messageInput"
            @keyup.enter="handleSend"
            placeholder="메시지를 입력하세요..."
            :disabled="store.loading"
          />
          <button 
            @click="handleSend"
            :disabled="store.loading || !messageInput.trim()"
          >
            전송
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
 
 <script setup>
import { ref, watch, nextTick } from 'vue'  // nextTick 추가
import { useChatStore } from '@/stores/chat'

const store = useChatStore()
const messageInput = ref('')
const messageContainer = ref(null)


defineEmits(['close'])  // close 이벤트 정의

// 메시지 전송 처리
const handleSend = () => {
  if (messageInput.value.trim()) {
    store.sendMessage(messageInput.value)
    messageInput.value = ''
  }
}

// 스크롤을 최신 메시지로 이동
const scrollToBottom = () => {
  if (messageContainer.value) {
    messageContainer.value.scrollTop = messageContainer.value.scrollHeight
  }
}

// messages가 변경될 때마다 스크롤
watch(
  () => store.messages,
  () => {
    nextTick(scrollToBottom)
  },
  { deep: true }
)
</script>
 
 <style scoped>

.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(233, 233, 233, 0.3);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.chat-interface {
  width: 80%;
  max-width: 800px;
  height: 80vh;
  background: white;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid #eee;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0 0.5rem;
}

.chat-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
 .chat-interface {
  height: 600px;
  margin: 0 auto;
  max-width: 800px;
 }
 
 .chat-area {
  height: 100%;
  display: flex;
  flex-direction: column;
 }
 
 .messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
 }
 
 .message {
  margin: 10px 0;
  padding: 10px;
  border-radius: 8px;
  max-width: 70%;
 }
 
 .message.user {
  background-color: #e3f2fd;
  margin-left: auto;
 }
 
 .message.bot {
  background-color: #f5f5f5;
 }
 
 .input-area {
  padding: 20px;
  border-top: 1px solid #eee;
  display: flex;
  gap: 10px;
 }
 
 input {
  flex: 1;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
 }
 
 button {
  padding: 8px 16px;
  background-color: #34396e;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
 }
 
 button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
 }
 </style>