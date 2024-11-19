<template>
<div v-if="results.length > 0" class="search-results">
    <div
        v-for="movie in results"
        :key="movie.id"
        class="movie-item"
        @click="emit('select', movie)"
    >
    <div class="movie-info">
        <h3>{{ movie.title }}</h3>
        <p>감독: {{ movie.director }}</p>
        <p>개봉년도: {{ movie.releaseYear }}</p>
    </div>
    </div>
</div>
</template>

<script setup>
defineProps({
    results: {
        type: Array,
        required: true
    }
})

const emit = defineEmits(['select'])
</script>

<style>
</style>