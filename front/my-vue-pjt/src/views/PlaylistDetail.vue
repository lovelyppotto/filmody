<template>
  <div>
    <!-- 로딩 상태 표시 -->
    <div v-if="loading">로딩 중...</div>
    
    <!-- 플레이리스트와 리뷰 표시 -->
    <div v-else>
      <!-- 플레이리스트 제목 -->
      <h1 v-if="playlist">{{ playlist.title }}</h1>
      <p v-if="playlist">{{ playlist.user_nickname }}</p>
      <h1 v-else>플레이리스트를 찾을 수 없습니다</h1>
      
      <!-- 플레이리스트 소유자일 경우에만 검색 버튼 표시 -->
      <div v-if="playlist?.user === authStore.userData?.id" class="text-end mb-3">
        <button class="btn btn-danger me-2" @click="openDeleteModal">
          <i class="fas fa-minus"></i> 플레이리스트 삭제
        </button>
        <button class="btn btn-primary me-2" @click="openSearchModal">
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

    <!-- 삭제 확인 모달 -->
    <div v-if="showDeleteModal" class="modal-backdrop">
      <div class="modal-content">
        <p>해당 플레이리스트를 완전히 삭제하시겠습니까?</p>
        <div class="text-end">
          <button class="btn btn-secondary me-2" @click="closeDeleteModal">취소</button>
          <button class="btn btn-danger" @click="confirmDeletePlaylist">삭제</button>
        </div>
      </div>
    </div>
  </div>
 </template>


<script setup>
import { onMounted, ref } from 'vue';
import { usePlaylistStore } from '@/stores/playlist';
import { useAuthStore } from '@/stores/auth';
import { useRoute, useRouter } from 'vue-router';
import PlaylistReviewList from '@/components/PlaylistReviews/PlaylistReviewList.vue';
import YoutubeSearchModal from '@/components/YoutubeAPI/YoutubeSearchModal.vue';
import PlaylistVideo from '@/components/Playlist/PlaylistVideo.vue';

// 스토어 및 라우트 설정
const route = useRoute();
const router = useRouter()
const playlistId = route.params.id;
const playlistStore = usePlaylistStore();
const authStore = useAuthStore();

// 상태 관리
const playlist = ref(null);
const loading = ref(true);
const showSearchModal = ref(false);
const showDeleteModal = ref(false); // 삭제 모달 상태

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

// 삭제 관련 함수
const openDeleteModal = () => {
  showDeleteModal.value = true;
};
const closeDeleteModal = () => {
  showDeleteModal.value = false;
};

const confirmDeletePlaylist = async () => {
  try {
    await playlistStore.deletePlaylist(Number(playlistId)); // 삭제 요청
    alert('플레이리스트가 삭제되었습니다.');
    closeDeleteModal();
    // 이후 페이지 이동 처리
    router.push({ name: 'PlaylistView' })
  } catch (error) {
    console.error('플레이리스트 삭제 실패:', error);
    alert('삭제 실패: 다시 시도해주세요.');
  }
};
</script>


<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  width: 90%;
  max-width: 400px;
  text-align: center;
}

.text-end {
  margin-top: 15px;
}
</style>