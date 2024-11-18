<template>
    <div v-if="store.movieDetail">  <!-- v-if 추가 -->
        <img 
            :src="`https://image.tmdb.org/t/p/w500${store.movieDetail.poster_path}`" 
            :alt="store.movieDetail.title"
        >       
        <h4>{{ store.movieDetail.title }}</h4>
        <p>장르: {{ genreList }}</p>
        <p>{{ store.movieDetail.tagline }}</p>
        <p>{{ store.movieDetail.overview }}</p>

    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useMovieStore } from '@/stores/movie'
import { useRoute } from 'vue-router';

const store = useMovieStore()
const route = useRoute()

const genreList = computed(() => {
    if (!store.movieDetail.genres) return ''
    return store.movieDetail.genres.map(genre => genre.name).join(', ')
})

onMounted(()=>{
    const movieId = route.params.id
    store.fetchMovieDetail(movieId)
})
</script>

<style scoped>

</style>