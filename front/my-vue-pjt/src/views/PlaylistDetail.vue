<template>
<div class="container">
    <div class="content-container">
      <!-- 로딩 상태 -->
      <div v-if="loading" class="header-section">
        <h2 class="title">로딩 중...</h2>
      </div>

      <!-- 플레이리스트가 있는 경우 -->
      <div v-else-if="playlist" class="header-section">
        <h2 class="title"><i class="fa-solid fa-hashtag" style="color: #2a3079;"></i> {{ playlist.title }}</h2>
        <p class="subtitle">upload by {{ playlist.user_nickname }}</p>
      </div>

      <!-- 플레이리스트가 없는 경우 -->
      <div v-else class="header-section">
        <h2 class="title">플레이리스트를 찾을 수 없습니다</h2>
        <p class="subtitle">다른 플레이리스트를 찾아보세요 :)</p>
      </div>

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

      <div 
        v-if="isOwner" 
        class="text-end mb-3"
      >
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
      v-if="isReviewVisible"
      :playlistId="Number(playlistId)"
    />
    <div v-else-if="hasReviews" class="text-end mb-3">
      <a 
        href="#" 
        @click.prevent="showHiddenReviews = true"
        class="review-toggle-link"
      >
        리뷰 보기
      </a>
    </div>
    </div>
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
})

// 1. 플레이리스트 작성자인지 확인
const isPlaylistOwner = computed(() => {
  if (!authStore.userData || !playlist.value) return false
  return playlist.value.user === authStore.userData.id || 
         playlist.value.user === authStore.userData.pk
})

// 2. 리뷰 존재 여부 확인
const hasReviews = computed(() => {
  // 리뷰 배열이 있고 길이가 0보다 크면 true
  return (playlist.value?.reviews?.length || 0) > 0
})

// 3. 리뷰 표시 여부를 결정하는 최종 computed
const isReviewVisible = computed(() => {
  // 리뷰가 없거나 플레이리스트 소유자면 무조건 표시
  if (!hasReviews.value || isPlaylistOwner.value) {
    return true
  }
  
  // 로그인한 사용자는 설정값이나 showHiddenReviews에 따라 표시
  if (authStore.token) {
    return authStore.userData?.show_reviews || showHiddenReviews.value
  }
  
  // 비로그인 사용자는 showHiddenReviews가 true일 때만 표시
  return showHiddenReviews.value
})


// 3. 사용자의 리뷰 표시 설정
const userShowReviews = computed(() => {
  // 로그인하지 않은 경우 false 반환
  if (!authStore.token) return false
  
  // 플레이리스트 작성자인 경우 항상 true 반환
  if (isPlaylistOwner.value) return true
  
  // 그 외의 경우 사용자 설정값 사용
  return authStore.userData?.show_reviews ?? false
})


const canLike = computed(() => {
  if (!authStore.userData || !playlist.value) return false
  return !isPlaylistOwner.value
})

const isOwner = computed(() => {
  return isPlaylistOwner.value && authStore.token
})

onMounted(() => {
  loading.value = true
  
  playlistStore.fetchPlaylists()
    .then(playlists => {
      playlist.value = playlists.find(p => p.id === Number(playlistId))
      // console.log('playlist data:', playlist.value) // 데이터 확인용
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
.container {
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem 0;
}

.content-container {
    padding: 0 1rem;
}

.header-section {
    margin-bottom: 2rem;
    padding: 0 0.5rem;
}

.title {
    font-size: 1.5em;
    font-weight: bold;
    margin-bottom: 0.5rem;
}

.subtitle {
    color: #666;
    font-size: 1rem;
    margin-right: 10px;
}

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

.review-toggle-link {
  color: #666;
  text-decoration: none;
  cursor: pointer;
}

.review-toggle-link:hover {
  text-decoration: underline;
  color: #2a3079;
}
</style>