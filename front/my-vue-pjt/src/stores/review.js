import { defineStore } from "pinia";
import axios from "axios";
import { ref } from 'vue';

export const useReviewStore = defineStore('review', () => {
  const reviews = ref([]);
  const loading = ref(false);
  const error = ref(null);

  const fetchReviews = async (playlistId) => {
    if (!playlistId) return;
    
    loading.value = true;
    try {
      const response = await axios.get(`/api/playlist/${playlistId}/reviews/`);
      reviews.value = Array.isArray(response.data) ? response.data : [];
      return response.data;
    } catch (err) {
      console.error(`리뷰 가져오기 실패:`, err);
      error.value = err.response?.data || "리뷰를 불러오지 못했습니다.";
      reviews.value = [];
    } finally {
      loading.value = false;
    }
  };

  const createReview = async (playlistId, content) => {
    try {
      const response = await axios.post(`/api/playlist/${playlistId}/reviews/`, { content });
      reviews.value = [response.data, ...reviews.value];
      return response.data;
    } catch (err) {
      error.value = err.response?.data || "리뷰 작성에 실패했습니다.";
      throw err;
    }
  };

  const toggleLike = async (playlistId, reviewId) => {
    try {
      const response = await axios.post(`/api/playlist/${playlistId}/reviews/${reviewId}/like/`);
      const index = reviews.value.findIndex(review => review.id === reviewId);
      if (index !== -1) {
        reviews.value[index] = {
          ...reviews.value[index],
          likesCount: response.data.likes_count,
          isLikedByUser: response.data.is_liked_by_user
        };
      }
      return response.data;
    } catch (err) {
      error.value = err.response?.data || "좋아요 토글에 실패했습니다.";
      throw err;
    }
  };

  const deleteReview = async (playlistId, reviewId) => {
    try {
      await axios.delete(`/api/playlist/${playlistId}/reviews/${reviewId}/`);
      reviews.value = reviews.value.filter(review => review.id !== reviewId);
    } catch (err) {
      error.value = err.response?.data || "리뷰 삭제에 실패했습니다.";
      throw err;
    }
  };

  return {
    reviews,
    loading,
    error,
    fetchReviews,
    createReview,
    deleteReview,
    toggleLike
  };
});