<template>
  <div>
    <YoutubeCard v-for="video in videos" :video="video" :key="video.id.videoId" />
  </div>
</template>

<script setup>
import YoutubeCard from "@/components/YoutubeAPI/YoutubeCard.vue";
import { useMovieStore } from "@/stores/movie";
import { computed } from "vue";

const store = useMovieStore();
const videos = computed(() => store.videos);
</script>

<style scoped></style>
