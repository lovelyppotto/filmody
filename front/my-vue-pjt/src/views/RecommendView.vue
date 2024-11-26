<template>
    <div class="container py-4 relative min-h-screen">
        <!-- 헤더 섹션 -->
        <div class="d-flex justify-content-between align-items-center mb-4">
            <div>
                <h2 class="text-2xl"><i class="fa-solid fa-film" style="color: #253c65; font-weight: 900;"></i> 추천 영화</h2>
                <p class="text-gray-600 font-subtitle">박스오피스 기준 영화를 추천해드립니다 :)</p>
            </div>
        </div>
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
