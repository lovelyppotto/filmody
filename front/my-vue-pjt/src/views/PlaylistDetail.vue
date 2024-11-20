<template>
  <div>
    <!-- 로딩 상태 표시 -->
    <div v-if="loading">로딩 중...</div>

    <!-- 플레이리스트와 리뷰 표시 -->
    <div v-else>
      <!-- 플레이리스트 제목, 없으면 '플레이리스트를 찾을 수 없습니다' 표시 -->
      <h1 v-if="playlist">{{ playlist.title }}</h1>
      <h1 v-else>플레이리스트를 찾을 수 없습니다</h1>
      
      <!-- PlaylistReviewList에 Number로 변환된 playlistId 전달 -->
      <PlaylistReviewList :playlistId="Number(playlistId)"/>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { usePlaylistStore } from '@/stores/playlist';
import { useRoute } from 'vue-router';
import PlaylistReviewList from '@/components/PlaylistReviews/PlaylistReviewList.vue';

// 라우터에서 현재 플레이리스트 ID를 가져옴
const route = useRoute();
const playlistId = route.params.id;

// Pinia 스토어 및 상태 변수
const playlistStore = usePlaylistStore();
const playlist = ref(null);
const loading = ref(true);

// 컴포넌트가 마운트되었을 때 데이터 가져오기
onMounted(() => {
  // 플레이리스트 데이터만 가져오기
  playlistStore.fetchPlaylists().then((playlists) => {
    // 해당 플레이리스트 찾기
    playlist.value = playlists.find((p) => p.id === Number(playlistId));
    loading.value = false; // 로딩 상태 해제
  }).catch((error) => {
    console.error('플레이리스트 가져오기 실패:', error);
    loading.value = false;
  });
});
</script>