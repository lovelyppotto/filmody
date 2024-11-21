<template>
  <div class="modal show d-block" tabindex="-1" style="background-color: rgba(0, 0, 0, 0.5)" @click.self="$emit('close')">
    <div class="modal-dialog modal-lg">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h5 class="modal-title">{{ video.snippet.title }}</h5>
          <button type="button" class="btn-close" @click="$emit('close')" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <!-- YouTube 영상 플레이어 -->
          <div class="ratio ratio-16x9 mb-3">
            <iframe
              :src="`https://www.youtube.com/embed/${video.id.videoId}`"
              title="YouTube video player"
              frameborder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowfullscreen
            ></iframe>
          </div>
          <!-- 영상 정보 -->
          <div class="video-info mb-3">
            <p class="description">{{ video.snippet.description }}</p>
            <small class="text-muted">게시일: {{ formatDate(video.snippet.publishTime) }}</small>
          </div>
        </div>
        <div class="modal-footer">
          <div class="d-flex justify-content-between w-100">
            <div>
              <button 
                class="btn btn-primary" 
                @click="addToPlaylist"
                :disabled="isLoading"
              >
                <span v-if="isLoading" class="spinner-border spinner-border-sm me-1" role="status"></span>
                {{ isLoading ? '추가 중...' : '플레이리스트에 추가' }}
              </button>
            </div>
            <button type="button" class="btn btn-secondary" @click="$emit('close')">닫기</button>
          </div>
        </div>
        <!-- 성공/실패 알림 -->
        <div 
          v-if="notification.show" 
          :class="`alert alert-${notification.type} alert-dismissible fade show position-absolute bottom-0 start-50 translate-middle-x mb-3`"
          role="alert"
        >
          {{ notification.message }}
          <button type="button" class="btn-close" @click="notification.show = false"></button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useMovieStore } from '@/stores/movie';

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

const emit = defineEmits(['close', 'videoSaved']);
const movieStore = useMovieStore();
const isLoading = ref(false);
const notification = ref({
  show: false,
  type: 'success',
  message: ''
});

const formatDate = (dateString) => {
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date);
};

const showNotification = (type, message) => {
  notification.value = {
    show: true,
    type,
    message
  };
  setTimeout(() => {
    notification.value.show = false;
  }, 3000);
};

const addToPlaylist = async () => {
  isLoading.value = true;
  try {
    await movieStore.addVideoToPlaylist(props.playlistId, props.video);
    showNotification('success', '플레이리스트에 추가되었습니다!');
    emit('videoSaved');
    setTimeout(() => {
      emit('close');
    }, 1500);
  } catch (error) {
    showNotification('danger', '추가 실패: ' + (error.response?.data?.error || '알 수 없는 오류가 발생했습니다.'));
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1050;
  overflow-y: auto;
}

.modal-dialog {
  margin: 2rem auto;
}

.description {
  white-space: pre-line;
  max-height: 150px;
  overflow-y: auto;
}

.alert {
  z-index: 1060;
}
</style>