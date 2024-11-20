<!-- views/PlaylistDetailView.vue -->
<template>
    <div class="container mx-auto p-4">
      <div v-if="playlistStore.loading" class="text-center py-8">
        로딩중...
      </div>
  
      <div v-else-if="playlistStore.error" class="bg-red-100 text-red-700 p-4 rounded-lg mb-4">
        {{ playlistStore.error }}
      </div>
  
      <template v-else-if="playlistStore.currentPlaylist">
        <!-- 플레이리스트 정보 헤더 -->
        <div class="bg-white rounded-lg shadow p-6 mb-6">
          <div class="flex justify-between items-start mb-4">
            <div>
              <h1 class="text-2xl font-bold mb-2">{{ playlistStore.currentPlaylist.title }}</h1>
              <p class="text-gray-600">{{ playlistStore.currentPlaylist.description }}</p>
            </div>
            <button 
              v-if="isOwner"
              @click="showAddVideoModal = true"
              class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
            >
              영상 추가
            </button>
          </div>
          <div class="text-sm text-gray-500">
            {{ playlistStore.currentPlaylist.videos?.length || 0 }}개의 영상
          </div>
        </div>
  
        <!-- 현재 재생중인 영상 영역 -->
        <div v-if="currentVideoId" class="mb-6">
          <div class="aspect-video">
            <!-- YouTube iFrame Player -->
            <div ref="playerContainer" class="w-full h-full"></div>
          </div>
        </div>
  
        <!-- 영상 목록 -->
        <div class="space-y-4">
          <VideoCard
            v-for="video in sortedVideos"
            :key="video.id"
            :video="video"
            :is-editable="isOwner"
            @play="playVideo(video)"
            @remove="removeVideo(video.id)"
          />
        </div>
      </template>
  
      <!-- 영상 추가 모달 -->
      <div v-if="showAddVideoModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
        <div class="bg-white p-6 rounded-lg w-full max-w-md">
          <h2 class="text-xl font-bold mb-4">영상 추가</h2>
          <!-- 이전에 만든 영상 추가 폼 내용 -->
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, onMounted } from 'vue'
  import { useRoute } from 'vue-router'
  import { usePlaylistStore } from '@/stores/playlist'
  import { useYoutubeData } from '@/composables/useYoutubeData'
  import VideoCard from '@/components/VideoCard.vue'
  
  const route = useRoute()
  const playlistStore = usePlaylistStore()
  const { loading: youtubeLoading, error: youtubeError, fetchVideoInfo } = useYoutubeData()
  
  const showAddVideoModal = ref(false)
  const playerContainer = ref(null)
  const currentVideoId = ref(null)
  const player = ref(null)
  
//   const isOwner = computed(() => {
//     return playlistStore.currentPlaylist?.user.id === /* 현재 로그인한 사용자 ID */
//   })
  
  const sortedVideos = computed(() => {
    return playlistStore.currentPlaylist?.videos?.sort((a, b) => a.order_num - b.order_num) || []
  })
  
  onMounted(() => {
    const playlistId = route.params.id
    playlistStore.fetchPlaylistById(playlistId)
  })
  
  // YouTube Player 초기화
  const initPlayer = () => {
    if (window.YT) {
      player.value = new window.YT.Player(playerContainer.value, {
        height: '100%',
        width: '100%',
        playerVars: {
          autoplay: 1,
          modestbranding: 1,
        }
      })
    }
  }
  
  const playVideo = (video) => {
    currentVideoId.value = video.video_id
    if (!player.value) {
      initPlayer()
    } else {
      player.value.loadVideoById(video.video_id)
    }
  }
  
  // ... 이전의 영상 추가/삭제 관련 메서드들
  </script>
