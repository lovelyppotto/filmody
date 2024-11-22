<!-- components/YoutubeSearchModal.vue -->
<template>
  <div class="modal show d-block" tabindex="-1" style="background-color: rgba(0, 0, 0, 0.5)" @click.self="$emit('close')">
    <div class="modal-dialog modal-lg modal-dialog-scrollable">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h5 class="modal-title">YouTube 영상 검색</h5>
          <button type="button" class="btn-close" @click="$emit('close')" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <!-- 검색창 -->
          <div class="search-container mb-4">
            <div class="input-group">
              <input 
                type="text" 
                class="form-control" 
                v-model="searchQuery"
                placeholder="추가하고 싶은 영상을 검색하세요"
                @keyup.enter="handleSearch"
              >
              <button 
                class="btn btn-primary" 
                @click="handleSearch"
                :disabled="isLoading"
              >
                <span v-if="isLoading" class="spinner-border spinner-border-sm me-1"></span>
                검색
              </button>
            </div>
          </div>

          <!-- 검색 결과 -->
          <div v-if="movieStore.videos.length > 0" class="search-results">
            <div v-for="video in movieStore.videos" :key="video.id.videoId" class="mb-3">
              <YoutubeCard 
                :video="video"
                :playlistId="playlistId"
                @videoSaved="handleVideoSaved"
              />
            </div>
          </div>
          <div v-else-if="!isLoading && searchPerformed" class="text-center py-4">
            검색 결과가 없습니다.
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useMovieStore } from '@/stores/movie';
import YoutubeCard from '@/components/YoutubeAPI/YoutubeCard.vue';


const props = defineProps({
  playlistId: {
    type: Number,
    required: true
  }
});

const emit = defineEmits(['close', 'videoAdded']);
const movieStore = useMovieStore();
const searchQuery = ref('');
const isLoading = ref(false);
const searchPerformed = ref(false);

const handleSearch = async () => {
if (!searchQuery.value.trim()) return;

isLoading.value = true;
searchPerformed.value = true;

try {
  await movieStore.searchReview(searchQuery.value);
} catch (error) {
  console.error('검색 실패:', error);
} finally {
  isLoading.value = false;
}
};

const handleVideoSaved = () => {
  emit('videoAdded');
};
</script>

<style scoped>
.modal-dialog {
  max-width: 800px;
}

.search-container {
  position: sticky;
  top: 0;
  background-color: white;
  padding: 1rem 0;
  z-index: 1;
}

.search-results {
  max-height: calc(100vh - 250px);
  overflow-y: auto;
}
</style>