<template>
  <div class="reviews-container">
    <!-- 리뷰 작성 폼은 항상 표시 -->
    <PlaylistReviewForm :playlistId="playlistId" />

    <!-- 리뷰 목록 컨테이너 -->
    <div class="reviews-section" :class="{ 'is-hidden': userShowReviews && !showHiddenReviews }">
      <div v-if="reviewStore.loading" class="loading">로딩 중...</div>
      <div v-else-if="reviewStore.reviews && reviewStore.reviews.length > 0" class="review-list">
        <PlaylistReviewItem
          v-for="review in reviewStore.reviews"
          :key="review.id"
          :review="review"
          :playlistId="playlistId"
        />
      </div>
      <p v-else>등록된 리뷰가 없습니다.</p>

      <!-- 가림 오버레이 -->
      <div v-if="userShowReviews && !showHiddenReviews" class="reviews-overlay">
        <div class="hidden-reviews-notice">
          <p class="text-center mt-4 py-1">리뷰를 가렸습니다!</p>
          <div class="text-center mt-2">
            <a 
              href="#" 
              @click.prevent="showHiddenReviews = true" 
              class="show-reviews-btn"
            >
              리뷰 확인하기
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useReviewStore } from "@/stores/review"
import { useAuthStore } from '@/stores/auth'
import PlaylistReviewForm from "./PlaylistReviewForm.vue"
import PlaylistReviewItem from "./PlaylistReviewItem.vue"
import { onMounted, watch, ref, computed } from "vue"

const props = defineProps({
  playlistId: {
    type: Number,
    required: true
  }
})

const authStore = useAuthStore()
const reviewStore = useReviewStore()
const showHiddenReviews = ref(false)

// show_reviews 상태 확인
const userShowReviews = computed(() => {
  console.log('userData:', authStore.userData)  // userData 전체 출력
  console.log('show_reviews value:', authStore.userData?.show_reviews)  // show_reviews 값 확인
  return authStore.userData?.show_reviews ?? true
})

const fetchReviews = () => {
  if (props.playlistId) {
    reviewStore.fetchReviews(props.playlistId)
      .catch(error => {
        console.error('리뷰 불러오기 실패:', error)
      })
  }
}

onMounted(() => {
  fetchReviews()
})

watch(() => props.playlistId, (newId) => {
  if (newId) {
    fetchReviews()
  }
})
</script>

<style scoped>
.reviews-container {
  position: relative;
  width: 100%;
}

.reviews-section {
  position: relative;
  transition: all 0.3s ease;
}

.reviews-section.is-hidden {
  max-height: 200px; /* 보여줄 높이 조절 */
  overflow: hidden;
}

.reviews-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 100%;
  background: linear-gradient(
    to bottom,
    rgba(255, 255, 255, 0.9) 0%,
    rgba(255, 255, 255, 0.98) 30%,
    rgba(255, 255, 255, 1) 100%
  );
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  align-items: center;
  padding-bottom: 20px;
}

/* .hidden-reviews-notice {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 8px;
  padding: 1rem;
  text-align: center;
  width: 90%;
  max-width: 400px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
} */

.show-reviews-btn {
  display: inline-block;
  padding: 0.5rem 1rem;
  color: #3b82f6;
  text-decoration: none;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.show-reviews-btn:hover {
  color: #2563eb;
  text-decoration: underline;
}

/* 흐림 효과가 자연스럽게 보이도록 약간의 여백 추가 */
.review-list {
  padding-bottom: 2rem;
}
</style>