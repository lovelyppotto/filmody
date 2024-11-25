<template>
  <form @submit.prevent="submitReview">
    <div class="review-form">
      <label for="formGroupExampleInput2" class="form-label fs-3">Playlist Review</label>
      <textarea 
        type="text" 
        class="form-control" 
        rows="3" 
        v-model="content"  
        id="formGroupExampleInput2" 
        placeholder="감상평을 남겨보세요 :)"
        @focus="handleFocus"
      >
      </textarea>
    </div>
    <div class="text-end me-2">
      <button 
        type="submit" 
        class="btn btn-primary"
        :disabled="!content.trim()"
      >
        작성
      </button>
    </div>
  </form>

  <!-- 로그인 필요 모달 -->
  <div v-if="showLoginModal" class="modal-backdrop">
    <div class="modal-content">
      <p>로그인이 필요한 서비스입니다.</p>
      <div class="text-end">
        <button class="btn btn-secondary me-2" @click="closeLoginModal">취소</button>
        <button class="btn btn-custom" @click="goToLogin">로그인</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useReviewStore } from "@/stores/review";
import { useAuthStore } from "@/stores/auth";
import { useRouter } from 'vue-router';

const props = defineProps({
  playlistId: {
    type: Number,
    required: true
  }
});

const router = useRouter();
const authStore = useAuthStore();
const reviewStore = useReviewStore();
const content = ref("");
const showLoginModal = ref(false);

const handleFocus = (event) => {
  if (!authStore.token) {
    event.target.blur(); // textarea에서 포커스 제거
    showLoginModal.value = true;
  }
};

const closeLoginModal = () => {
  showLoginModal.value = false;
};

const goToLogin = () => {
  closeLoginModal();
  router.push('/login'); // 로그인 페이지로 이동
};

const submitReview = () => {
  if (content.value.trim()) {
    reviewStore.createReview(props.playlistId, content.value)
      .then(newReview => {
        console.log('리뷰 작성 성공:', newReview);
        content.value = "";
      })
      .catch(error => {
        console.error('리뷰 작성 실패:', error);
      });
  }
};
</script>

<style scoped>
.review-form {
  margin: 30px 20px 10px 20px
}

textarea {
  resize: none;
}

.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(151, 148, 148, 0.646);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1050;
}

.modal-content {
  text-align: center;
  background: white;
  padding: 30px;
  border-radius: 8px;
  width: 90%;
  max-width: 400px;
}
.btn-custom{
  background-color: #213565;
  color: white;
}
.btn-custom:hover{
  background-color: #213565d7;
  color: white;
}

.text-end {
  margin-top: 15px;
}
</style>