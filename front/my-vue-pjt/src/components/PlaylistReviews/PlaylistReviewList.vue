<template>
  <div class="reviews-container">
    <h2>리뷰</h2>

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

const fetchReviews = async () => {
  if (props.playlistId) {
    await reviewStore.fetchReviews(props.playlistId);
  }
};

onMounted(() => {
  fetchReviews();
});

// playlistId가 변경될 때마다 리뷰를 새로 불러옴
watch(() => props.playlistId, () => {
  fetchReviews();
});
</script>
  
  <style scoped>
  .reviews-container {
    padding: 16px;
  }
  .review-list {
    margin-top: 16px;
  }
  .loading {
    text-align: center;
    margin-top: 16px;
  }
  </style>