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
      <div v-if="isOwner" class="text-end mb-3">
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
      
      <!-- PlaylistReviewList -->
      <PlaylistReviewList :playlistId="Number(playlistId)"/>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue';
import { usePlaylistStore } from '@/stores/playlist';
import { useAuthStore } from '@/stores/auth';
import { useRoute } from 'vue-router';
import PlaylistReviewList from '@/components/PlaylistReviews/PlaylistReviewList.vue';
import YoutubeSearchModal from '@/components/YoutubeAPI/YoutubeSearchModal.vue';

const route = useRoute();
const playlistId = route.params.id;
const playlistStore = usePlaylistStore();
const authStore = useAuthStore();
const playlist = ref(null);
const loading = ref(true);
const showSearchModal = ref(false);

// 플레이리스트 소유자 여부 확인
const isOwner = computed(() => {
  return playlist.value?.user === authStore.currentUser;
});

// 컴포넌트 마운트 시 데이터 가져오기
onMounted(() => {
  playlistStore.fetchPlaylists().then((playlists) => {
    playlist.value = playlists.find((p) => p.id === Number(playlistId));
    loading.value = false;
  }).catch((error) => {
    console.error('플레이리스트 가져오기 실패:', error);
    loading.value = false;
  });
});

const openSearchModal = () => {
  showSearchModal.value = true;
};

const closeSearchModal = () => {
  showSearchModal.value = false;
};

const handleVideoAdded = () => {
  // 필요한 경우 플레이리스트 새로고침
  playlistStore.fetchPlaylists().then((playlists) => {
    playlist.value = playlists.find((p) => p.id === Number(playlistId));
  });
};
</script>