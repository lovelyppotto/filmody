<template>
  <div>
    <div v-if="loading">로딩 중...</div>
    
    <div v-else>
      <h1 v-if="playlist">{{ playlist.title }}</h1>
      <p v-if="playlist">{{ playlist.user_nickname }}</p>
      <h1 v-else>플레이리스트를 찾을 수 없습니다</h1>

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

      <div v-if="playlist?.user === authStore.userData?.id" class="text-end mb-3">
        <button class="btn btn-danger me-2" @click="openDeleteModal">
          <i class="fas fa-minus"></i> 플레이리스트 삭제
        </button>
        <button class="btn btn-primary me-2" @click="openSearchModal">
          <i class="fas fa-plus"></i> 플레이리스트 추가
        </button>
      </div>

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

      <!-- 리뷰 작성 폼 -->
      <PlaylistReviewForm :playlistId="props.playlistId" />
      <div class="review-list-wrapper">
        <PlaylistReviewList 
          :playlistId="Number(playlistId)"
        />
      </div>
    </div>

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
import { onMounted, ref, computed } from 'vue'
import { usePlaylistStore } from '@/stores/playlist'
import { useAuthStore } from '@/stores/auth'
import { useRoute, useRouter } from 'vue-router'
import PlaylistReviewList from '@/components/PlaylistReviews/PlaylistReviewList.vue'
import YoutubeSearchModal from '@/components/YoutubeAPI/YoutubeSearchModal.vue'
import PlaylistVideo from '@/components/Playlist/PlaylistVideo.vue'

const route = useRoute()
const router = useRouter()
const playlistId = route.params.id
const playlistStore = usePlaylistStore()
const authStore = useAuthStore()

const playlist = ref(null)
const loading = ref(true)
const showSearchModal = ref(false)
const showDeleteModal = ref(false)
const showHiddenReviews = ref(false)


const props = defineProps({
  playlistId: {
    type: Number,
    required: true
  }
});

const userShowReviews = computed(() => {
  // 현재 로그인한 유저가 플레이리스트 작성자인지 확인
  const isPlaylistOwner = playlist.value?.user === authStore.userData?.id

  if (isPlaylistOwner) {
    // 작성자라면 항상 리뷰 표시
    return true
  }

  // 작성자가 아니라면 show_reviews 설정값 사용
  return authStore.userData?.show_reviews ?? true
})

// 리뷰 표시 여부를 결정하는 새로운 computed 속성
const isReviewVisible = computed(() => {
  return !userShowReviews.value || showHiddenReviews.value
})

const canLike = computed(() => {
  if (!authStore.userData || !playlist.value) return false
  
  const isOwner = playlist.value.user === authStore.userData.id || 
                  playlist.value.user === authStore.userData.pk
                  
  return !isOwner
})

onMounted(() => {
  loading.value = true
  
  playlistStore.fetchPlaylists()
    .then(playlists => {
      playlist.value = playlists.find(p => p.id === Number(playlistId))
    })
    .catch(error => {
      console.error('플레이리스트 가져오기 실패:', error)
    })
    .finally(() => {
      loading.value = false
    })
})

const openSearchModal = () => {
  showSearchModal.value = true
}

const closeSearchModal = () => {
  showSearchModal.value = false
}

const openDeleteModal = () => {
  showDeleteModal.value = true
}

const closeDeleteModal = () => {
  showDeleteModal.value = false
}

const confirmDeletePlaylist = () => {
  playlistStore.deletePlaylist(Number(playlistId))
    .then(() => {
      alert('플레이리스트가 삭제되었습니다.')
      closeDeleteModal()
      router.push({ name: 'PlaylistView' })
    })
    .catch(error => {
      console.error('플레이리스트 삭제 실패:', error)
      alert('삭제 실패: 다시 시도해주세요.')
    })
}

const handleLike = () => {
  if (!authStore.token) {
    alert('로그인이 필요합니다.')
    return
  }
  
  if (!playlist.value?.id) {
    console.error('플레이리스트 ID가 없습니다.')
    return
  }

  if (playlist.value.user === authStore.userData.id || 
      playlist.value.user === authStore.userData.pk) {
    console.log('자신의 플레이리스트는 좋아요할 수 없습니다.')
    return
  }

  playlistStore.toggleLike(playlist.value.id)
    .then(response => {
      playlist.value = {
        ...playlist.value,
        is_liked: response.liked,
        likes_count: response.likes_count
      }
    })
    .catch(error => {
      console.error('좋아요 처리 중 오류 발생:', error)
    })
}
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
  align-items: baseline;
  gap: 0.5rem;
}

.like-icon {
  font-size: 1.8rem;
  line-height: 1;
}

.like-count {
  margin: 0px 20px 0px 10px;
  min-width: 2rem;
  font-size: 1.5rem;
  line-height: 1;
}

.fa-heart {
  transition: all 0.2s ease;
}

.hoverable:hover {
  color: #dc3545;
}

.text-danger {
  color: #dc3545 !important;
}

.disabled .fa-heart {
  cursor: not-allowed;
}

.review-list-wrapper {
  margin-bottom: 100px;
}
</style>