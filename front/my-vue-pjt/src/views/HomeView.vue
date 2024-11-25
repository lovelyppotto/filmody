<template>
    <div class="container py-4">
      <!-- 헤더 영역 -->
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h1 class="h3 mb-0 fw-bold text-center align-items-center"><i class="fa-solid fa-fire" style="color: #f70000;"></i> Hot Playlist <i class="fa-solid fa-fire" style="color: #f70000;"></i></h1>
      </div>
  
      <!-- 로딩 상태 -->
      <div v-if="playlistStore.loading" class="text-center py-4">
        <p>로딩중...</p>
      </div>
  
      <!-- 플레이리스트 그리드 -->
      <div v-else class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
        <div 
          v-for="playlist in sortedPlaylists" 
          :key="playlist.id"
          class="col"
        >
          <div class="polaroid" @click="navigateToDetail(playlist.id)" @mouseover="tiltCard" @mouseleave="resetCard">
            <img :src="playlist.cover_img || 'https://cdn.imweb.me/upload/S20210807d1f68b7a970c2/7170113c6a983.jpg'" alt="Playlist Cover">
            <div class="polaroid-text">{{ playlist.title }}</div>
            <div class="polaroid-user">{{ playlist.user_nickname }}</div>
            <div class="polaroid-likes">
              <i class="fa-solid fa-heart"></i> {{ playlist.likes_count }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, computed } from 'vue'
  import { useRouter } from 'vue-router'
  import { usePlaylistStore } from '@/stores/playlist'
  import { useAuthStore } from '@/stores/auth'
  
  const router = useRouter()
  const authStore = useAuthStore()
  const playlistStore = usePlaylistStore()
  const isModalOpen = ref(false)
  
  // 상세 페이지 이동
  const navigateToDetail = (playlistId) => {
    router.push(`/playlist/${playlistId}`)
  }
  
  // 좋아요 순으로 정렬된 플레이리스트 목록
  const sortedPlaylists = computed(() => {
    return [...playlistStore.playlists].sort((a, b) => b.likes_count - a.likes_count)
  })
  
const tiltCard = (event) => {
  const card = event.currentTarget
  card.style.transform = 'rotate(-10deg)'
}

const resetCard = (event) => {
  event.currentTarget.style.transform = 'rotate(0deg)'
}
  
  // 초기 데이터 로드
  onMounted(() => {
    playlistStore.fetchPlaylists()
  })
  </script>
  
  <style scoped>
.polaroid {
  position: relative;
  background: #fff;
  border: solid #fff;
  border-width: 6px 6px 80px 6px;
  box-shadow: 2px 2px 8px #333;
  height: 350px;
  width: 100%;
  cursor: pointer;
  transition: transform 0.3s;
  transform-origin: center center;
}

.polaroid:hover {
  box-shadow: 4px 4px 12px #333;
}

.polaroid img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-bottom: solid 6px #fff;
}

.polaroid-info {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 10px;
  background-color: #fff;
  text-align: center;
}

.polaroid-text {
  font-size: 16px;
  font-family: Arial, sans-serif;
  color: #000;
  line-height: 1.2;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  padding-bottom: 5px;
  margin-bottom: 5px;
  margin-left: 10px;
}

.polaroid-user {
  font-size: 14px;
  font-family: Arial, sans-serif;
  color: #666;
  line-height: 1.2;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-bottom: 5px;
  margin-left: 10px;
}

.polaroid-likes {
  font-size: 14px;
  color: #000;
  margin-left: 10px;
}

.polaroid-likes i {
  color: #f70000;
  margin-right: 5px;
}
  </style>