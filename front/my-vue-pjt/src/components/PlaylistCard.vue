<!-- components/PlaylistCard.vue -->
<template>
    <div class="playlist-card p-4 rounded-lg shadow-md bg-white hover:shadow-lg transition-shadow">
      <!-- 썸네일 영역 -->
      <div class="aspect-square bg-gray-100 rounded-md overflow-hidden mb-4">
        <img 
          :src="thumbnailSrc"
          :alt="playlist.title"
          class="w-full h-full object-cover"
        >
      </div>
  
      <!-- 플레이리스트 정보 -->
      <div class="playlist-info">
        <h3 class="font-bold text-lg mb-1 truncate">{{ playlist.title }}</h3>
        <div class="flex items-center text-sm text-gray-500">
          <span v-if="!playlist.is_public" class="mr-2">🔒</span>
          <span class="text-xs">
            {{ formatDate(playlist.created_at) }}
          </span>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { computed } from 'vue'
  
  const props = defineProps({
    playlist: {
      type: Object,
      required: true
    }
  })
  
  // 썸네일 URL 계산
  const thumbnailSrc = computed(() => {
    if (props.playlist.cover_img) {
      return props.playlist.cover_img
    }
    // 기본 이미지 반환
    return '/default-playlist-cover.jpg'  // 기본 이미지 경로
  })
  
  // 날짜 포맷팅
  const formatDate = (dateString) => {
    if (!dateString) return ''
    const date = new Date(dateString)
    return date.toLocaleDateString()
  }
  </script>
  
  <style scoped>
  .playlist-card {
    width: 100%;
    max-width: 320px;
    transition: all 0.2s ease;
  }
  
  .playlist-card:hover {
    transform: translateY(-2px);
  }
  </style>