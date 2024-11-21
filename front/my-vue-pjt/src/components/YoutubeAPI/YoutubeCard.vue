<template>
  <div class="container mt-3">
    <div 
      class="card mb-3 hover-card" 
      style="max-width: 800px; margin: 0 auto" 
      @click="openModal"
    >
      <div class="row g-0">
        <div class="col-md-4">
          <img 
            :src="video.snippet.thumbnails.medium.url" 
            class="img-fluid rounded-start" 
            :alt="video.snippet.title"
          />
        </div>
        <div class="col-md-8">
          <div class="card-body">
            <h5 class="card-title">{{ decodeHtml(video.snippet.title) }}</h5>
            <p class="card-text description">{{ video.snippet.description }}</p>
            <p class="card-text">
              <small class="text-body-secondary">
                {{ formatDate(video.snippet.publishTime) }}
              </small>
            </p>
          </div>
        </div>
      </div>
    </div>
    <YoutubeReviewModal 
      v-if="isModalOpen" 
      :video="video" 
      :playlistId="playlistId"
      @close="closeModal"
      @videoSaved="$emit('videoSaved')"
    />
  </div>
</template>

<script setup>
import { ref } from "vue";
import YoutubeReviewModal from "@/components/YoutubeAPI/YoutubeReviewModal.vue";
import { useDecodeHtml } from '@/composables/useDecodeHtml';

// 디코딩 적용
const { decodeHtml } = useDecodeHtml();

const props = defineProps({
  video: {
    type: Object,
    required: true
  },
  playlistId: {
    type: Number,
    required: true
  }
});

defineEmits(['videoSaved']);

const isModalOpen = ref(false);

const openModal = () => {
  isModalOpen.value = true;
};

const closeModal = () => {
  isModalOpen.value = false;
};

const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleString();
};
</script>

<style scoped>
.hover-card {
  cursor: pointer;
  transition: all 0.3s ease;
}

.hover-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.description {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

img {
  object-fit: cover;
  height: 100%;
  min-height: 180px;
}

.card {
  border: 1px solid #dee2e6;
  background-color: white;
}

.card-title {
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.text-body-secondary {
  color: #6c757d;
}
</style>