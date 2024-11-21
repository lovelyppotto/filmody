<template>
    <div>
        <LibraryMovieListItem 
            v-for="movie in store.likedMovies"
            :key="movie.id"
            :movie="movie"
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

</style>