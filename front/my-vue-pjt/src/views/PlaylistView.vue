<template>
  <div class="container py-4">
    <!-- 헤더 영역 -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1 class="h3 mb-0">내 플레이리스트</h1>
      <button 
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
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { usePlaylistStore } from '@/stores/playlist'
import PlaylistCard from '@/components/PlaylistCard.vue'
import CreatePlaylistModal from '@/components/CreatePlaylistModal.vue'

const router = useRouter()
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

// 초기 데이터 로드
onMounted(() => {
  playlistStore.fetchPlaylists()
})
</script>