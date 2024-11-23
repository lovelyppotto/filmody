import { defineStore } from "pinia";
import axios from "axios";
import { ref } from 'vue';
import { useAuthStore } from './auth';

export const useReviewStore = defineStore('review', () => {
  const reviews = ref([]);
  const loading = ref(false);
  const error = ref(null);
  const authStore = useAuthStore();

  // axios 요청에 인증 헤더와 baseURL을 추가하는 함수
  const authRequest = (method, url, data = null) => {
    const config = {
      method,
      url: `${authStore.BASE_URL}${url}`,
      headers: {
        'Authorization': `Token ${authStore.token}`,
        'Content-Type': 'application/json',
      }
    };

    if (data) {
      config.data = data;
    }

    return axios(config);
  };

  const fetchReviews = (playlistId) => {
    if (!playlistId) return Promise.resolve();
    
    loading.value = true;
    return authRequest('get', `/api/playlist/${playlistId}/review-list/`)
      .then(response => {
        reviews.value = Array.isArray(response.data) ? response.data : [];
        return response.data;
      })
      .catch(err => {
        console.error(`리뷰 가져오기 실패:`, err);
        error.value = err.response?.data || "리뷰를 불러오지 못했습니다.";
        reviews.value = [];
        return Promise.reject(err);
      })
      .finally(() => {
        loading.value = false;
      });
  };

  const createReview = (playlistId, content) => {
    if (!authStore.token) {
      error.value = "로그인이 필요합니다.";
      return Promise.reject(new Error("로그인이 필요합니다."));
    }

    loading.value = true;
    return authRequest('post', `/api/playlist/${playlistId}/reviews/`, { content })
      .then(response => {
        reviews.value = [response.data, ...reviews.value];
        return response.data;
      })
      .catch(err => {
        error.value = err.response?.data || "리뷰 작성에 실패했습니다.";
        return Promise.reject(err);
      })
      .finally(() => {
        loading.value = false;
      });
  };

  const toggleLike = async (playlistId, reviewId) => {
    try {
      const response = await authRequest('post', `/api/playlist/${playlistId}/review/${reviewId}/toggle-like/`);
      
      // 전체 목록을 다시 불러오는 대신 해당 리뷰만 업데이트
      const updatedReview = response.data;
      reviews.value = reviews.value.map(review => 
        review.id === reviewId 
          ? { ...review, is_liked: updatedReview.is_liked, likes_count: updatedReview.likes_count }
          : review
      );
      
      return response.data;
    } catch (err) {
      console.error('좋아요 토글 실패:', err);
      throw err;
    }
  };

  

  
  const deleteReview = (playlistId, reviewId) => {
    if (!authStore.token) {
      error.value = "로그인이 필요합니다.";
      return Promise.reject(new Error("로그인이 필요합니다."));
    }

    return authRequest('delete', `/api/playlist/${playlistId}/reviews/`, { review_id: reviewId })
      .then(() => {
        reviews.value = reviews.value.filter(review => review.id !== reviewId);
        return true;
      })
      .catch(err => {
        error.value = err.response?.data || "리뷰 삭제에 실패했습니다.";
        return Promise.reject(err);
      });
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