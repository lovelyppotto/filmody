<template>
  <div class="card h-100 hover:shadow-lg transition-all cursor-pointer">
    <!-- 이미지 섹션 -->
    <div class="position-relative">
      <img 
        v-if="playlist.cover_img"
        :src="playlist.cover_img"
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
import { ref } from 'vue'

const props = defineProps({
  playlist: {
    type: Object,
    required: true
  }
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