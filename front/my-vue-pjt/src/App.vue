<template>
  <AppNavbar />
  <!-- 챗봇 버튼 -->
  <button class="chat-button" @click="openChat">
    <i class="fas fa-comments"></i>
    <!-- <span>영화 추천받기</span> -->
  </button>

    <Teleport to="body">
      <Transition name="fade">
        <ChatBotModal 
          v-if="showChat" 
          @close="closeChat"
        />
      </Transition>
    </Teleport>
  <div class="content-wrapper">
    <RouterView />
  </div>
</template>

<script setup>
import AppNavbar from "@/components/Common/AppNavbar.vue";
import ChatBotModal from "@/components/Common/ChatBotModal.vue";
import { RouterView, RouterLink } from 'vue-router'
import { useAuthStore } from "@/stores/auth";
import { ref, onMounted } from "vue";
import axios from "axios";

const store = useAuthStore()


// 토큰이 있으면 로그인 상태 유지
onMounted(() => {
  const token = localStorage.getItem('token')
  if(token) {
    axios({
      method:'get',
      url:`${store.BASE_URL}/accounts/user/`,
      headers: {
        Authorization: `Token ${token}`
      }
    })
    .then(() => {
      store.token = token
    })
    .catch(() => {
      // 토큰이 만료됐거나 유효하지 않을 때
      localStorage.removeItem('token')
      store.token = null
    })
  }
})

const showChat = ref(false)

const openChat = () => {
  showChat.value = true
}

const closeChat = () => {
  showChat.value = false
}

</script>

<style scoped>
@import "@/assets/index.css";

.content-wrapper {
  margin-top: 65px;
  /* 또는 */
  /* 필요한 경우 추가 스타일 */
  width: 100%;
  min-height: calc(100vh - 56px);
  font-family: Nanum;
}

.chat-button {
  position: fixed;
  z-index: 98;
  bottom: 2rem;
  right: 2rem;
  padding: 1rem;
  background-color: #2f3842aa;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  transition: transform 0.2s;
}

.chat-button:hover {
  transform: translateY(-2px);
  background-color: #192c3eec;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 모달 슬라이드 효과도 추가 */
.fade-enter-active .chat-interface {
  animation: slide-up 0.3s ease;
}

.fade-leave-active .chat-interface {
  animation: slide-down 0.3s ease;
}

@keyframes slide-up {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

@keyframes slide-down {
  from {
    transform: translateY(0);
    opacity: 1;
  }
  to {
    transform: translateY(20px);
    opacity: 0;
  }
}
</style>
