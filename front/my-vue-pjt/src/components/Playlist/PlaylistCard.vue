<template>
  <div class="card h-100 hover:shadow-lg transition-all cursor-pointer">
    <!-- 이미지 섹션 -->
    <div class="position-relative">
      <img 
        v-if="playlist.cover_img"
        :src="imgSrc"
        :alt="playlist.title"
        class="card-img-top"
        style="height: 200px; object-fit: cover;"
        @error="handleImageError"
      />
      <div 
        v-else 
        class="card-img-top bg-light d-flex align-items-center justify-content-center"
        style="height: 200px;"
      >
        <span class="text-muted">No Image</span>
      </div>
    </div>
    
    <!-- 카드 본문 -->
    <div class="card-body">
      <h5 class="card-title mb-1 text-truncate">{{ playlist.title }}</h5>
      <p class="card-text">
        <small class="text-muted">{{ formatDate(playlist.created_at) }}</small>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'  // 조건부로 사용

const props = defineProps({
  playlist: {
    type: Object,
    required: true
  },
  useBaseUrl: {  // BASE_URL 사용 여부를 prop으로 받음
    type: Boolean,
    default: false
  }
})

// 이미지 소스를 computed로 처리
const imgSrc = computed(() => {
  if (!props.playlist.cover_img) return ''
  
  // useBaseUrl이 true일 때만 BASE_URL 적용
  if (props.useBaseUrl) {
    const authStore = useAuthStore()
    return `${authStore.BASE_URL}${props.playlist.cover_img}`
  }
  
  return props.playlist.cover_img
})

const handleImageError = (e) => {
  const parentDiv = e.target.parentElement
  parentDiv.innerHTML = `
    <div 
      class="card-img-top bg-light d-flex align-items-center justify-content-center"
      style="height: 200px;"
    >
      <span class="text-muted">Image Error</span>
    </div>
  `
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script>

<style scoped>
.card {
  border: 1px solid rgba(0,0,0,.125);
  border-radius: 0.5rem;
  background-color: white;
}

.card:hover {
  transform: translateY(-2px);
}

.card-body {
  padding: 1rem;
}

.card-title {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.text-muted {
  color: #6c757d;
}
</style>