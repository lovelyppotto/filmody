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
        placeholder="감상평을 남겨보세요 :)" >
      </textarea>
    </div>
    <div class="text-end me-2"> <!-- 버튼을 감싸는 div 추가 -->
      <button 
        type="submit" 
        class="btn btn-primary"
        :disabled="!content.trim()" > <!-- content가 비어있거나 공백만 있으면 disabled -->
        작성
      </button>
    </div>
  </form>
 </template>
 
 <script setup>
 import { ref } from "vue";
 import { useReviewStore } from "@/stores/review";
 
 const props = defineProps({
  playlistId: {
    type: Number,
    required: true
  }
 });
 
 const reviewStore = useReviewStore();
 const content = ref("");
 
 const submitReview = () => {
  if (content.value.trim()) {  // 내용이 있을 때만 제출
    reviewStore.createReview(props.playlistId, content.value)
      .then(newReview => {
        console.log('리뷰 작성 성공:', newReview);
        content.value = ""; // 작성 후 초기화
      })
      .catch(error => {
        console.error('리뷰 작성 실패:', error);
      });
  }
 };
 </script>
 <style>
  .review-form{
    margin: 30px 20px 10px 20px
  }

  textarea {
    resize: none;
  }
</style>