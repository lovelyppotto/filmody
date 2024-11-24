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
      <span class="timestamp">
        <span v-if="isEdited" class="edited-mark">(수정됨)</span>
        {{ formattedDate }}
      </span>
    </div>
    
    <div v-if="isEditing" class="edit-form">
      <textarea 
        v-model="editContent" 
        class="edit-textarea"
        placeholder="수정할 내용을 입력하세요."
      ></textarea>
      <div class="edit-buttons">
        <button @click="handleSave" class="save-btn">저장</button>
        <button @click="handleCancel" class="cancel-btn">취소</button>
      </div>
    </div>
    <!-- 일반 모드일 때 -->
    <p v-else>{{ review.content }}</p>

    <div class="actions-wrapper">
      <i 
        :class="[
          'fa-thumbs-up', 
          'like-icon', 
          review.is_liked ? 'fa-solid' : 'fa-regular'
        ]"
        @click="handleLikeClick"
      ></i>
      <span class="like-count">{{ review.likes_count || 0 }}</span>
      <button 
        v-if="review.is_owner" 
        class="edit-btn" 
        @click="startEdit"  
      >수정</button>
      <button 
        v-if="review.is_owner" 
        class="delete-btn" 
        @click="deleteReview"
      >삭제</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useReviewStore } from "@/stores/review";
import { useAuthStore } from "@/stores/auth";
import { useRouter } from "vue-router";

const router = useRouter();
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
const authStore = useAuthStore();
// 수정 관련 상태
const isEditing = ref(false);
const editContent = ref('');

// 삭제 버튼 표시 여부 계산
const canDelete = computed(() => {
  // console.log("Review data:", props.review);  // 전체 리뷰 데이터
  // console.log("Is owner:", props.review.is_owner);  // is_owner 값
  // console.log("User info:", props.review.user_info);  // 사용자 정보
  return props.review.is_owner;
});

// 수정 여부 확인을 위한 computed 속성 추가
const isEdited = computed(() => {
  if (!props.review.updated_at) return false;
  
  const createdDate = new Date(props.review.created_at).getTime();
  const updatedDate = new Date(props.review.updated_at).getTime();
  
  return updatedDate > createdDate;
});


const formattedDate = computed(() => {
  const date = new Date(props.review.created_at);
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');
  return `${year}. ${month}. ${day}  |  ${hours}:${minutes}`;
});

const handleLikeClick = async () => {
  if (props.review.is_owner) return;
  
  try {
    await reviewStore.toggleLike(props.playlistId, props.review.id);
  } catch (error) {
    console.error('Failed to toggle like:', error);
  }
};

const getImageUrl = (profileImage) => {
  const baseUrl = authStore.BASE_URL;
  
  if (!profileImage) {
    return `${baseUrl}/static/images/default.png`;
  }
  
  if (profileImage.startsWith('/static/')) {
    return `${baseUrl}${profileImage}`;
  }
  
  try {
    if (profileImage.startsWith('/media/')) {
      const encodedPath = profileImage.split('/').map(segment => 
        segment.includes('.') ? segment : encodeURIComponent(segment)
      ).join('/');
      return `${baseUrl}${encodedPath}`;
    }
    
    const encodedImage = encodeURIComponent(profileImage);
    return `${baseUrl}/media/${encodedImage}`;
  } catch (error) {
    console.error('Error creating image URL:', error);
    return `${baseUrl}/static/images/default.png`;
  }
};

const goToUserProfile = (userId) => {
  router.push(`/users/${userId}`);
};


// 수정 시작
const startEdit = () => {
  editContent.value = props.review.content;
  isEditing.value = true;
};

// 수정 취소
const handleCancel = () => {
  isEditing.value = false;
  editContent.value = '';
};

// 수정 저장
const handleSave = () => {
  if (!editContent.value.trim()) {
    alert('내용을 입력해주세요');
    return;
  }

  reviewStore.updateReview(props.playlistId, props.review.id, {
    content: editContent.value.trim()
  })
    .then(() => {
      isEditing.value = false;
      editContent.value = '';
    })
    .catch(error => {
      console.error('리뷰 수정 실패:', error);
    });
};

const deleteReview = async () => {
  try {
    await reviewStore.deleteReview(props.playlistId, props.review.id);
  } catch (error) {
    console.error('Failed to delete review:', error);
  }
};

const handleImageError = (event) => {
  event.target.src = `${authStore.BASE_URL}/static/images/default.png`;
};

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

.edit-form {
  margin: 10px 0;
}

.edit-textarea {
  width: 100%;
  min-height: 80px;
  padding: 8px;
  margin-bottom: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  resize: none;
}

.edit-buttons {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}

.save-btn, .cancel-btn {
  padding: 5px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9em;
}

.save-btn {
  background-color: #4CAF50;
  color: white;
  border: none;
}

.cancel-btn {
  background-color: #f5f5f5;
  border: 1px solid #ddd;
}

.edit-btn {
  padding: 5px 10px;
  border-radius: 4px;
  border: 1px solid #ddd;
  background: #f5f5f5;
  cursor: pointer;
  font-size: 0.9em;
  margin-right: 8px;
}

.edited-mark {
  color: #666;
  font-size: 0.9em;
  margin-right: 5px;
}

</style>