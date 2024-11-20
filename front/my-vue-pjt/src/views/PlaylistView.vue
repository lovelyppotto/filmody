<!-- views/PlaylistListView.vue -->
<template>
    <div class="container mx-auto p-4">
      <!-- 헤더 영역 -->
      <div class="mb-6 flex justify-between items-center">
        <h1 class="text-2xl font-bold">내 플레이리스트</h1>
        <button 
          @click="showCreateModal = true"
          class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
        >
          새 플레이리스트
        </button>
      </div>
  
      <!-- 로딩 상태 -->
      <div v-if="playlistStore.loading" class="text-center py-8">
        <p>로딩중...</p>
      </div>
  
      <!-- 에러 메시지 -->
      <div v-if="playlistStore.error" class="bg-red-100 text-red-700 p-4 rounded-lg mb-4">
        {{ playlistStore.error }}
      </div>
  
      <!-- 플레이리스트 그리드 -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        <PlaylistCard
          v-for="playlist in playlistStore.playlists"
          :key="playlist.id"
          :playlist="playlist"
          @click="navigateToDetail(playlist.id)"
        />
      </div>
  
      <!-- 새 플레이리스트 생성 모달 -->
      <div v-if="showCreateModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
        <div class="bg-white p-6 rounded-lg w-full max-w-md">
          <h2 class="text-xl font-bold mb-4">새 플레이리스트 만들기</h2>
          <form @submit.prevent="createNewPlaylist">
            <div class="mb-4">
              <label class="block mb-2">제목</label>
              <input 
                v-model="newPlaylist.title"
                type="text"
                class="w-full border rounded-lg px-3 py-2"
                required
              >
            </div>
            <div class="mb-4">
              <label class="block mb-2">설명</label>
              <textarea
                v-model="newPlaylist.description"
                class="w-full border rounded-lg px-3 py-2"
                rows="3"
              ></textarea>
            </div>
            <div class="flex justify-end gap-2">
              <button 
                type="button"
                @click="showCreateModal = false"
                class="px-4 py-2 border rounded-lg"
              >
                취소
              </button>
              <button 
                type="submit"
                class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
              >
                만들기
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useRouter } from 'vue-router'
  import { usePlaylistStore } from '@/stores/playlist'
  import PlayListCard from '@/components/PlayListCard.vue';
  
  const router = useRouter()
  const playlistStore = usePlaylistStore()
  const showCreateModal = ref(false)
  const newPlaylist = ref({
    title: '',
    description: ''
  })
  
  // 컴포넌트 마운트시 플레이리스트 목록 가져오기
  onMounted(() => {
    playlistStore.fetchPlaylists()
      .then(() => {
        console.log('플레이리스트 로드 완료')
      })
      .catch((error) => {
        console.error('플레이리스트 로드 실패:', error)
      })
  })
  
  // 새 플레이리스트 생성
  const createNewPlaylist = () => {
    playlistStore.createPlaylist(newPlaylist.value)
      .then(() => {
        showCreateModal.value = false
        newPlaylist.value = { title: '', description: '' }
      })
      .catch((error) => {
        console.error('플레이리스트 생성 실패:', error)
      })
  }
  
  // 상세 페이지로 이동
  const navigateToDetail = (playlistId) => {
    router.push(`/playlist/${playlistId}`)
  }
  </script>
  