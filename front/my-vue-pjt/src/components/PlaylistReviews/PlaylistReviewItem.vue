<template>
  <div class="review-item">
    <div class="review-header">
      <strong>{{ review.user }}</strong>
      <span>{{ review.created_at }}</span>
    </div>
    <p>{{ review.content }}</p>

    <!-- 액션 버튼 -->
    <div class="actions">
      <button @click="toggleLike">
        {{ review.likesCount }} 👍 {{ review.isLikedByUser ? "좋아요 취소" : "좋아요" }}
      </button>
      <button @click="deleteReview">삭제</button>
    </div>
  </div>
</template>

<script setup>
import { useReviewStore } from "@/stores/review";

// id 제대로 전달하지 않으면 오류나므로 주의
const props = defineProps({
  review: {
    type: Object,
    required: true
  },
  playlistId: {
    type: Number,
    required: true
  }
});

const reviewStore = useReviewStore();

const toggleLike = () => {
  reviewStore.toggleLike(props.playlistId, props.review.id);
};

const deleteReview = () => {
  reviewStore.deleteReview(props.playlistId, props.review.id);
};
</script>