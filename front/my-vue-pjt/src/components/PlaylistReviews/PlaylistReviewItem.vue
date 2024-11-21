<template>
  <div class="review-item">
    <div class="review-header">
      <strong>{{ review.user }}</strong>
      <span class="timestamp">{{ formatDate(review.created_at) }}</span>
    </div>
    <p>{{ review.content }}</p>

    <div class="actions-wrapper">
      <i 
        :class="[
          'fa-thumbs-up', 
          'like-icon', 
          review.is_liked_by_user ? 'fa-solid' : 'fa-regular'
        ]"
        @click="toggleLike"
      ></i>
      <span class="like-count">{{ review.likes_count || 0 }}</span>
      <button class="delete-btn" @click="deleteReview">삭제</button>
    </div>
  </div>
</template>
 
 <script setup>
 import { useReviewStore } from "@/stores/review";
 
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
 
 const formatDate = (dateString) => {
  const date = new Date(dateString);
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');
 
  return `${year}. ${month}. ${day}  |  ${hours}:${minutes}`;
 };
 
 const toggleLike = () => {
  reviewStore.toggleLike(props.playlistId, props.review.id);
 };
 
 const deleteReview = () => {
  reviewStore.deleteReview(props.playlistId, props.review.id);
 };
 </script>
 
 <style scoped>
 .review-item {
  margin-bottom: 16px;
  padding: 15px;
  border-bottom: 1px solid #eee;
 }
 
 .review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
 }
 
 .timestamp {
  color: #666;
  font-size: 0.9em;
 }
 
 .actions-wrapper {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 8px;  /* 요소들 사이 간격 */
  padding-right: 10px;  /* 오른쪽 여백 */
  margin-top: 12px;
}

.like-icon {
  cursor: pointer;
  color: #666;
  transition: all 0.2s ease;
}

.like-icon:hover {
  transform: scale(1.1);
}

.like-icon.fa-solid {
  color: #0d6efd;
}

.like-count {
  color: #666;
  font-size: 0.9em;
  margin: 0 5px;  /* 좌우 여백 */
}

.delete-btn {
  padding: 5px 10px;
  border-radius: 4px;
  border: 1px solid #ddd;
  background: #f5f5f5;
  cursor: pointer;
  font-size: 0.9em;
}
</style>