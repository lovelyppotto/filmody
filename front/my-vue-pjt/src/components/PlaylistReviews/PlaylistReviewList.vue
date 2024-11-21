<template>
  <div class="reviews-container">
    <!-- 리뷰 작성 폼 -->
    <PlaylistReviewForm :playlistId="props.playlistId" />

    <!-- 리뷰 목록 -->
    <div v-if="reviewStore.loading" class="loading">로딩 중...</div>
    <div v-else-if="reviewStore.reviews && reviewStore.reviews.length > 0" class="review-list">
      <PlaylistReviewItem
        v-for="review in reviewStore.reviews"
        :key="review.id"
        :review="review"
        :playlistId="props.playlistId"
      />
    </div>
    <p v-else>등록된 리뷰가 없습니다.</p>
  </div>
</template>

<script setup>
import { useReviewStore } from "@/stores/review";
import PlaylistReviewForm from "./PlaylistReviewForm.vue";
import PlaylistReviewItem from "./PlaylistReviewItem.vue";
import { onMounted, watch } from "vue";

const props = defineProps({
  playlistId: {
    type: Number,
    required: true
  }
});

const reviewStore = useReviewStore();

// Promise 체이닝으로 변경
const fetchReviews = () => {
  if (props.playlistId) {
    reviewStore.fetchReviews(props.playlistId)
      .catch(error => {
        console.error('리뷰 불러오기 실패:', error);
      });
  }
};

onMounted(() => {
  fetchReviews();
});

// watch 효과 수정
watch(() => props.playlistId, (newId) => {
  if (newId) {
    fetchReviews();
  }
});
</script>