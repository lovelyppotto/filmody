<template>
  <div>
    <!-- 로딩 상태 표시 -->
    <div v-if="loading">로딩 중...</div>
    
    <!-- 플레이리스트와 리뷰 표시 -->
    <div v-else>
      <!-- 플레이리스트 제목 -->
      <h1 v-if="playlist">{{ playlist.title }}</h1>
      <h1 v-else>플레이리스트를 찾을 수 없습니다</h1>
      
      <!-- 플레이리스트 소유자일 경우에만 검색 버튼 표시 -->
      <div v-if="playlist?.user === authStore.userData?.id" class="text-end mb-3">
        <button class="btn btn-primary" @click="openSearchModal">
          <i class="fas fa-plus"></i> 플레이리스트 추가
        </button>
      </div>
 
      <!-- YouTube 검색 모달 -->
      <YoutubeSearchModal
        v-if="showSearchModal"
        :playlistId="Number(playlistId)"
        @close="closeSearchModal"
        @videoAdded="handleVideoAdded"
      />
      
      <PlaylistVideo 
        :playlist-id="playlistId" 
        :playlist="playlist"  
      />
      <router-view :playlist-id="playlistId"></router-view>
 
      <!-- PlaylistReviewList -->
      <PlaylistReviewList :playlistId="Number(playlistId)"/>
    </div>
  </div>
 </template>


<script setup>
import { onMounted, ref } from 'vue';
import { usePlaylistStore } from '@/stores/playlist';
import { useAuthStore } from '@/stores/auth';
import { useRoute } from 'vue-router';
import PlaylistReviewList from '@/components/PlaylistReviews/PlaylistReviewList.vue';
import YoutubeSearchModal from '@/components/YoutubeAPI/YoutubeSearchModal.vue';
import PlaylistVideo from '@/components/Playlist/PlaylistVideo.vue';

// 스토어 및 라우트 설정
const route = useRoute();
const playlistId = route.params.id;
const playlistStore = usePlaylistStore();
const authStore = useAuthStore();

// 상태 관리
const playlist = ref(null);
const loading = ref(true);
const showSearchModal = ref(false);

// 컴포넌트 마운트 시 데이터 가져오기
onMounted(async () => {
 try {
   loading.value = true;
   const playlists = await playlistStore.fetchPlaylists();
   playlist.value = playlists.find((p) => p.id === Number(playlistId));
 } catch (error) {
   console.error('플레이리스트 가져오기 실패:', error);
 } finally {
   loading.value = false;
 }
});

// 모달 관련 함수
const openSearchModal = () => {
 showSearchModal.value = true;
};

const closeSearchModal = () => {
 showSearchModal.value = false;
};

// 비디오 추가 후 처리
const handleVideoAdded = async () => {
 try {
   const playlists = await playlistStore.fetchPlaylists();
   playlist.value = playlists.find((p) => p.id === Number(playlistId));
 } catch (error) {
   console.error('플레이리스트 새로고침 실패:', error);
 }
};
</script>