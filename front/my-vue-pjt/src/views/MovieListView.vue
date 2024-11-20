<template>
  <div class="container mt-5">
    <div class="row">
      <MovieListItem v-for="movie in store.recommendMovies" :key="movie.id" :movie="movie" />
    </div>
  </div>
</template>

<script setup>
import { onMounted } from "vue";
import { useMovieStore } from "@/stores/movie.js";
import MovieListItem from "@/components/RecommendMovieListItem.vue";

const store = useMovieStore();

onMounted(() => {
  store.fetchTopRatedMovies();
});
</script>
