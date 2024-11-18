<!-- YoutubeReviewModal.vue -->
<template>
    <div class="modal show d-block" tabindex="-1" style="background-color: rgba(0, 0, 0, 0.5)" @click.self="$emit('close')">
      <div class="modal-dialog modal-lg">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h5 class="modal-title">{{ video.snippet.title }}</h5>
            <button type="button" class="btn-close" @click.stop.prevent="$emit('close')" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div class="ratio ratio-16x9">
              <iframe
                :src="`https://www.youtube.com/embed/${video.id.videoId}`"
                title="YouTube video player"
                frameborder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowfullscreen
              ></iframe>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click.stop.prevent="$emit('close')">닫기</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  defineProps({
    video: Object,
  });
  
  defineEmits(['close']);
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
  </style>