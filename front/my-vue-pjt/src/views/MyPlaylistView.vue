<template>
  <div class="container py-4 relative min-h-screen"> <!-- 부모에 min-h-screen으로 높이 확보 -->

    <!-- 헤더 섹션 -->
    <div class="mb-4">
      <h2 class="text-2xl font-bold"><i class="fa-solid fa-music" style="color: #5c42b3;"></i> 내 플레이리스트</h2>
      <p class="text-gray-600">등록한 플레이리스트를 확인하세요 :)</p>
    </div>

    <!-- 로딩 상태 표시 -->
    <div v-if="playlistStore.loading" class="text-center py-8">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 mx-auto"></div>
    </div>

    <!-- 에러 메시지 -->
    <div v-else-if="playlistStore.error" class="text-center py-8">
      <p class="text-red-500">{{ playlistStore.error }}</p>
      <button 
        @click="playlistStore.fetchMyPlaylist" 
        class="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
      >
        다시 시도
      </button>
    </div>

    <!-- 플레이리스트 목록 -->
    <div v-else-if="playlistStore.myPlaylists.length > 0" class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
      <div 
        v-for="playlist in playlistStore.myPlaylists" 
        :key="playlist.id"
        class="col"
      >
        <PlaylistCard
          :playlist="playlist"
          :use-base-url="true"
          @click="navigateToPlaylist(playlist.id)"
        />
      </div>
    </div>

    <!-- 데이터가 없을 때 이 부분은 화면 정중앙 위치 -->
    <div 
      v-else
      class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-center"
    >
      <p class="text-gray-500">생성한 플레이리스트가 없습니다.</p>
    </div>
  </div>
</template>


<script setup>
import PlaylistCard from '@/components/Playlist/PlaylistCard.vue'
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { usePlaylistStore } from '@/stores/playlist'

const playlistStore = usePlaylistStore()
const router = useRouter()

const navigateToPlaylist = (playlistId) => {
  router.push(`/playlist/${playlistId}`)
}

onMounted(() => {
  console.log('컴포넌트 마운트')
  playlistStore.fetchMyPlaylist()
})
</script>