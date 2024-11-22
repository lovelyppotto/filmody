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

      <!-- 플레이리스트 소유자가 아닐 경우 좋아요 버튼 표시(로그인한 유저만) -->
      <div class="text-end mb-3">
    <button 
      @click="handleLike" 
      class="like-button"
      :class="{ 
        'disabled': !canLike,
        'owner': playlist?.user === authStore.userData?.id || 
                playlist?.user === authStore.userData?.pk 
      }"
    >
      <div class="like-container">
        <i 
          class="fa-heart fa-2x like-icon"
          :class="{
            'fa-solid': playlist?.is_liked,
            'fa-regular': !playlist?.is_liked,
            'text-danger': playlist?.is_liked,
            'hoverable': canLike
          }"
        ></i>
        <span class="like-count">{{ playlist?.likes_count || 0 }}</span>
      </div>
    </button>
  </div>

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
import { onMounted, ref, computed } from 'vue';
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

// 플레이리스트 상태
const currentPlaylist = computed(() => playlistStore.currentPlaylist)

onMounted(async () => {
  try {
    console.log('Route params:', route.params);
    const playlistId = route.params.playlistId; // URL 파라미터 이름 확인 필요
    if (playlistId) {
      console.log('플레이리스트 ID:', playlistId);
      const data = await playlistStore.fetchPlaylist(playlistId);
      playlist.value = data;
      console.log('로드된 플레이리스트:', playlist.value);
    }
  } catch (error) {
    console.error('플레이리스트 로딩 실패:', error);
  }
});

const props = defineProps({
  playlist: {
    type: Object,
    required: true
  }
})

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

const canLike = computed(() => {
  console.log('현재 유저:', authStore.userData);
  console.log('플레이리스트:', playlist.value);
  
  if (!authStore.userData || !playlist.value) return false;
  
  // 현재 유저가 플레이리스트 작성자인 경우 false 반환
  const isOwner = playlist.value.user === authStore.userData.id || 
                  playlist.value.user === authStore.userData.pk;
                  
  console.log('Is owner:', isOwner);
  return !isOwner; // 작성자가 아닌 경우에만 true 반환
});

const handleLike = async () => {
  try {
    if (!authStore.token) {
      alert('로그인이 필요합니다.');
      return;
    }
    
    if (!playlist.value?.id) {
      console.error('플레이리스트 ID가 없습니다.');
      return;
    }

    // 작성자 체크 한번 더
    if (playlist.value.user === authStore.userData.id || 
        playlist.value.user === authStore.userData.pk) {
      console.log('자신의 플레이리스트는 좋아요할 수 없습니다.');
      return;
    }

    const response = await playlistStore.toggleLike(playlist.value.id);
    playlist.value = {
      ...playlist.value,
      is_liked: response.liked,
      likes_count: response.likes_count
    };
  } catch (error) {
    console.error('좋아요 처리 중 오류 발생:', error);
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

fa-heart {
  cursor: pointer;
}

.like-button {
  background: none;
  border: none;
  padding: 0;
  cursor: pointer;
  transition: all 0.2s ease;
}

.like-button:not(.disabled):hover .fa-heart {
  transform: scale(1.1);
  opacity: 0.8;
}

.like-button.disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

.like-container {
  display: flex;
  align-items: baseline; /* baseline으로 변경 */
  gap: 0.5rem; /* 간격 조정 */
}

.like-icon {
  font-size: 1.8rem; /* 아이콘 크기 조정 */
  line-height: 1; /* 라인 높이 조정 */
}

.like-count {
  margin: 0px 20px 0px 10px;
  min-width: 2rem;
  font-size: 1.5rem; /* 숫자 크기 조정 */
  line-height: 1; /* 라인 높이 조정 */
}


.fa-heart {
  transition: all 0.2s ease;
}

.hoverable:hover {
  color: #dc3545;  /* Bootstrap의 danger 색상 */
}

.text-danger {
  color: #dc3545 !important;
}

.disabled .fa-heart {
  cursor: not-allowed;
}
</style>