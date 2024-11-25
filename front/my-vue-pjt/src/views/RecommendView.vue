<template>
    <div class="movie-container">
        <h1 class="title">🎬 추천 영화</h1>
        <div class="recommend-list-wrapper">
            <RecommendMovieList />
        </div>
    </div>
</template>

<script setup>
import RecommendMovieList from '@/components/RecommendMovieList.vue';
</script>

<style scoped>
.movie-container {
    padding: 20px;
}

.title {
    margin: 20px 90px 10px;
    font-weight: 600;
    line-height: 1.5;
    font-size: 1.8rem;
    color: #333;
}

.recommend-list-wrapper {
    margin-top: 4%; /* 원하는 만큼 여백 추가 */
}
</style>
