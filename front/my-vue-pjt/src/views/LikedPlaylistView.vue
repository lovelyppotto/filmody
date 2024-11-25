<template>
  <div class="container py-4">

    <!-- 헤더 섹션 -->
    <div class="mb-4">
      <h2 class="text-2xl"><i class="fa-solid fa-heart" style="color: #ed1d1d; font-weight: 900;"></i> 좋아요한 플레이리스트</h2>
      <p class="text-gray-600">마음에 드는 플레이리스트를 모아보세요 :)</p>
    </div>

    <!-- 로딩 상태 표시 -->
    <div v-if="playlistStore.loading" class="text-center py-8">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 mx-auto"></div>
    </div>

    <!-- 에러 메시지 -->
    <div v-else-if="playlistStore.error" class="text-center py-8">
      <p class="text-red-500">{{ playlistStore.error }}</p>
      <button 
        @click="redirectToLogin" 
        class="mt-4 px-4 py-2 !bg-indigo-500 text-black rounded hover:!bg-indigo-600"
      >
        로그인
      </button>
    </div>

    <!-- 플레이리스트 목록 -->
    <div v-else class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
  <div 
    v-for="playlist in playlistStore.likedPlaylists" 
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

    <!-- 데이터가 없을 때 -->
    <div v-if="!playlistStore.loading && !playlistStore.error && playlistStore.likedPlaylists.length === 0" class="text-center py-8">
      <p class="text-gray-500">아직 좋아요한 플레이리스트가 없습니다.</p>
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

const redirectToLogin = () => {
  router.push({ name: 'LogInView' })  // 로그인 라우트 이름을 사용
}

onMounted(() => {
  console.log('컴포넌트 마운트')
  playlistStore.fetchLikedPlaylists()
})
</script>
