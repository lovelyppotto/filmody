<template>
    <div v-if="store.movieDetail">  <!-- v-if 추가 -->
        <img 
            :src="`${store.movieDetail.poster_url}`" 
            :alt="store.movieDetail.title"
        >       
        <h4>{{ store.movieDetail.title }}</h4>
        <p>장르: {{ store.movieDetail.genre }}</p>
        <p>감독: {{ store.movieDetail.director }}</p>
        <p>개봉년도 : {{ store.movieDetail.open_year }}</p>
        <p>줄거리 : {{ store.movieDetail.plot }}</p>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useMovieStore } from '@/stores/movie'
import { useRoute } from 'vue-router';

const store = useMovieStore()
const route = useRoute()

onMounted(()=>{
    const movieId = route.params.id
    store.fetchMovieDetail(movieId)
})
</script>

<style scoped>

</style>