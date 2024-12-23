<template>
  <div class="container py-4 relative min-h-screen">
    <!-- 헤더 섹션 -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h2 class="text-2xl"><i class="fa-solid fa-music" style="color: #253c65; font-weight: 900;"></i> Playlist</h2>
        <p class="text-gray-600 font-subtitle">{{ playlistCount }} Playlists, Find your favorite music!</p>
      </div>
      <button 
        v-if="authStore.token"
        @click="openModal"
        class="btn btn-primary"
      >
        새 플레이리스트
      </button>
    </div>


    <!-- 로딩 상태 -->
    <div v-if="playlistStore.loading" class="text-center py-4">
      <p>로딩중...</p>
    </div>

    <!-- 플레이리스트 그리드 -->
    <div v-else class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
      <div 
        v-for="playlist in playlistStore.playlists" 
        :key="playlist.id"
        class="col"
      >
        <PlaylistCard
          :playlist="playlist"
          @click="navigateToDetail(playlist.id)"
        />
      </div>
    </div>

    <!-- 플레이리스트 생성 모달 -->
    <CreatePlaylistModal
      v-if="isModalOpen"
      v-model="isModalOpen"
      :loading="playlistStore.loading"
      @submit="handleCreatePlaylist"
      @close="closeModal"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { usePlaylistStore } from '@/stores/playlist'
import { useAuthStore } from '@/stores/auth'
import PlaylistCard from '@/components/Playlist/PlaylistCard.vue'
import CreatePlaylistModal from '@/components/Playlist/CreatePlaylistModal.vue'

const router = useRouter()
const authStore = useAuthStore()
const playlistStore = usePlaylistStore()
const isModalOpen = ref(false)

// 모달 열기
const openModal = () => {
  isModalOpen.value = true
}

// 모달 닫기
const closeModal = () => {
  isModalOpen.value = false
}

// 플레이리스트 생성 처리
const handleCreatePlaylist = (formData) => {
  playlistStore.createPlaylist(formData)
    .then(() => {
      closeModal()
      return playlistStore.fetchPlaylists()
    })
    .catch(error => {
      console.error('플레이리스트 생성 실패:', error)
    })
}

// 상세 페이지 이동
const navigateToDetail = (playlistId) => {
  router.push(`/playlist/${playlistId}`)
}

// 플레이리스트 수를 계산하는 computed 속성
const playlistCount = computed(() => {
  return playlistStore.playlists?.length || 0
})

// 초기 데이터 로드
onMounted(() => {
  playlistStore.fetchPlaylists()
})
</script>

<style scoped>
.font-subtitle {
  font-family: 'Nunito', sans-serif;
  font-size: 18px;
}
</style>