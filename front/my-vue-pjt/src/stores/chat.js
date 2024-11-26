// stores/chat.js
import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useAuthStore } from './auth'

export const useChatStore = defineStore('chat', () => {
  const messages = ref([])
  const loading = ref(false)
  const error = ref(null)
  const authStore = useAuthStore()

  const sendMessage = async (message) => {
    loading.value = true
    error.value = null
    
    // 사용자 메시지 바로 추가
    messages.value.push({
      content: message,
      is_bot: false,
      timestamp: new Date().toISOString()
    })

    try {
      const response = await axios.post('/v1/chat/completions', {
        model: "gpt-4o-mini",
        messages: [{ role: "user", content: message }]
      }, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${import.meta.env.VITE_OPENAI_API_KEY}`
        }
      })

      // GPT 응답 추가
      messages.value.push({
        content: response.data.choices[0].message.content,
        is_bot: true,
        timestamp: new Date().toISOString()
      })
    } catch (err) {
      error.value = '메시지 전송 실패'
      console.error('Error:', err)
    } finally {
      loading.value = false
    }
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