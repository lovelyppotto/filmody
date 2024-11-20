<template>
  <form @submit.prevent="submitReview">
    <textarea 
      v-model="content" 
      rows="3" 
      placeholder="리뷰를 입력하세요."
      required>
    </textarea>
    <button type="submit">작성</button>
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
  reviewStore.createReview(props.playlistId, content.value);
  content.value = ""; // 작성 후 초기화
};
</script>