// stores/chat.js
import { ref } from 'vue'
import { defineStore } from 'pinia'
import OpenAI from 'openai'
import { useAuthStore } from './auth'

export const useChatStore = defineStore('chat', () => {
  const messages = ref([])
  const loading = ref(false)
  const error = ref(null)
  const authStore = useAuthStore()

  // OpenAI 클라이언트 초기화
  const openai = new OpenAI({
    apiKey: import.meta.env.VITE_OPENAI_API_KEY,
    dangerouslyAllowBrowser: true  // 브라우저에서 사용하기 위해 필요
  })

  const sendMessage = (message) => {
    loading.value = true
    error.value = null
    
    // 사용자 메시지 바로 추가
    messages.value.push({
      content: message,
      is_bot: false,
      timestamp: new Date().toISOString()
    })

    openai.chat.completions.create({
      model: "gpt-4o-mini",
      messages: [{ role: "user", content: message }]
    })
      .then(response => {
        // GPT 응답 추가
        messages.value.push({
          content: response.choices[0].message.content,
          is_bot: true,
          timestamp: new Date().toISOString()
        })
      })
      .catch(err => {
        error.value = '메시지 전송 실패'
        console.error('Error:', err)
      })
      .finally(() => {
        loading.value = false
      })
  }

  const clearMessages = () => {
    messages.value = []
  }

  return {
    messages,
    loading,
    error,
    sendMessage,
    clearMessages
  }
})