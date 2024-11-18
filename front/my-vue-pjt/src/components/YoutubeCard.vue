<!-- YoutubeCard.vue -->
<template>
    <div class="container mt-3">
      <div class="card mb-3 hover-card" style="max-width: 800px; margin: 0 auto" @click="openModal">
        <div class="row g-0">
          <div class="col-md-4 img-container">
            <img :src="video.snippet.thumbnails.high.url" alt="" class="img-fluid rounded-start" />
          </div>
          <div class="col-md-8">
            <div class="card-body">
              <h5 class="card-title text-truncate">{{ video.snippet.title }}</h5>
              <p class="card-text description">{{ video.snippet.description }}</p>
              <p class="card-text">
                <small class="text-body-secondary">{{ video.snippet.publishTime }}</small>
              </p>
            </div>
          </div>
        </div>
      </div>
      <YoutubeReviewModal v-if="isModalOpen" :video="video" @close="closeModal" />
    </div>
   </template>
   
   <script setup>
   import { ref } from "vue";
   import YoutubeReviewModal from "./YoutubeReviewModal.vue";
   
   defineProps({
    video: Object,
   });
   
   const isModalOpen = ref(false);
   
   const openModal = (e) => {
    e?.preventDefault();
    isModalOpen.value = true;
   };
   
   const closeModal = (e) => {
    e?.preventDefault();
    isModalOpen.value = false;
   };
   </script>