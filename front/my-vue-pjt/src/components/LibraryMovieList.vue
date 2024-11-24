<template>
    <div class="row g-4 mx-3">
        <LibraryMovieListItem 
            v-for="movie in store.likedMovies"
            :key="movie.id"
            :movie="movie"
            class="col-12 col-md-6 col-lg-4"
        />
    </div>
</template>

<script setup>
import LibraryMovieListItem from '@/components/LibraryMovieListItem.vue';
import { useMovieStore } from '@/stores/movie';
import { onMounted } from 'vue';
const store = useMovieStore()
onMounted(() => {
    store.fetchLikedMovies()
})

</script>

<style scoped>
/* 카드 간격 */
.row.g-4 {
  gap: 1.5rem; /* 카드 간격 */
}
</style>