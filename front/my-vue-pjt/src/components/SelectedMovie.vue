<template>
<div v-if="movie" class="selected-movie">
    <div class="movie-detail">
    <h3>{{ movie.title }}</h3>
    <p>감독: {{ movie.director }}</p>
    <p>개봉년도: {{ movie.openYear }}</p>
    <p>출연진: {{ movie.actor }}</p>
    <p>줄거리: {{ movie.plot }}</p>
    <button @click="emit('searchPlaylist')" class="search-playlist-btn">
        플레이리스트 검색
    </button>
    </div>
</div>
</template>

<script setup>
defineProps({
movie: {
    type: Object,
    required: true
}
})

const emit = defineEmits(['searchPlaylist'])
</script>

<style>
</style>