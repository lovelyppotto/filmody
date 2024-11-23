<template>
  <div class="review-item">
    <div class="review-header">
      <div class="image-nickname" @click="goToUserProfile(review.user_info.id)">
        <img 
        :src="getImageUrl(review.user_info.profile_image)" 
        alt="프로필 사진"
        class="profile-image"
        @error="handleImageError"
        >
        <strong>{{ review.user_info.nickname }}</strong>
      </div>
      <span class="timestamp">{{ formatDate(review.created_at) }}</span>
    </div>
    <p>{{ review.content }}</p>

    <div class="actions-wrapper">
    <i 
      :class="[
        'fa-thumbs-up', 
        'like-icon', 
        review.is_liked ? 'fa-solid' : 'fa-regular'
      ]"
      @click="reviewStore.toggleLike(playlistId, review.id)"
    ></i>
    <span class="like-count">{{ review.likes_count || 0 }}</span>
    <button class="delete-btn" @click="deleteReview">삭제</button>
  </div>
  </div>
</template>


<script setup>
import { ref } from "vue";
import { useReviewStore } from "@/stores/review";
import { useAuthStore } from "@/stores/auth";
import { useRouter } from "vue-router";
const router = useRouter()
const showModal = ref(false);

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
const authStore = useAuthStore()

const formatDate = (dateString) => {
  const date = new Date(dateString);
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');

  return `${year}. ${month}. ${day}  |  ${hours}:${minutes}`;
};

// const isAlertOpen = ref(false);

const handleLikeClick = () => {
  if (props.review.is_owner) return; // 자신의 리뷰면 여기서 끝
  reviewStore.toggleLike(props.playlistId, props.review.id);
};

const closeModal = () => {
  showModal.value = false;
};

const deleteReview = () => {
  reviewStore.deleteReview(props.playlistId, props.review.id);
};

const getImageUrl = (profileImage) => {
  console.log('Original profile image:', profileImage);
  const baseUrl = authStore.BASE_URL

  // 프로필 이미지가 없는 경우
  if (!profileImage) {
    return `${baseUrl}/static/images/default.png`;
  }
  
  // static 폴더(기본 이미지)인 경우
  if (profileImage.startsWith('/static/')) {
    return `${baseUrl}${profileImage}`;
  }
  
  // media 폴더(업로드된 이미지)인 경우
  try {
    if (profileImage.startsWith('/media/')) {
      // URL 인코딩 처리
      const encodedPath = profileImage.split('/').map(segment => 
        segment.includes('.') ? 
          segment : // 파일명은 이미 인코딩되어 있으므로 건너뛰기
          encodeURIComponent(segment)
      ).join('/');
      
      return `${baseUrl}${encodedPath}`;
    }
    
    // media로 시작하지 않는 경우
    const encodedImage = encodeURIComponent(profileImage);
    return `${baseUrl}/media/${encodedImage}`;
    } catch (error) {
      console.error('Error creating image URL:', error);
      return '/static/images/default.png';
    }
};

const goToUserProfile = (user_id) => {
  router.push(`/users/${user_id}`)
}
</script>

 <style scoped>
 .review-item {
  margin-bottom: 16px;
  padding: 15px;
  border-bottom: 1px solid #eee;
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

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.image-nickname {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;  /* 클릭 가능함을 표시 */
  transition: opacity 0.2s ease;  /* 부드러운 호버 효과 */
}

.image-nickname:hover {
  opacity: 0.8;  /* 호버 시 약간 투명해지는 효과 */
}

.profile-image {
  width: 40px;        
  height: 40px;
  border-radius: 50%;  
  object-fit: cover;   
  flex-shrink: 0;      
}

</style>