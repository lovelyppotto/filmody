<!-- MovieListItem.vue -->
<template>
    <div class="col-12 col-md-6 col-lg-3 mb-4">  <!-- 그리드 시스템 수정 -->
        <div class="card h-100" @click="goToDetail(movie.id)">  <!-- 높이 일정하게 -->
            <img 
                :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`" 
                class="card-img-top"
                :alt="movie.title"
                style="object-fit: cover;"  
            >
            <div class="card-body">
                <h5 class="card-title">{{ movie.title }}</h5>
                <p class="card-text text-truncate">{{ movie.overview }}</p>  <!-- 긴 텍스트 자르기 -->
                <p class="card-text">
                    <small class="text-muted">
                        평점: {{ movie.vote_average }}
                    </small>
                </p>
            </div>
        </div>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

defineProps({
    movie: {
        type: Object,
        required: true
    }
}) 

const goToDetail = (movieId) => {
    router.push(`/movies/${movieId}`)
}
</script>

<style scoped>
.card {
    transition: transform 0.2s;
}

.card:hover {
    transform: scale(1.02);
}

.card-img-top {
    height: 400px;  /* 이미지 높이 고정 */
    object-fit: cover;
}

/* 긴 텍스트 처리 */
.card-text {
    display: -webkit-box;
    -webkit-line-clamp: 3;  /* 최대 3줄 */
    -webkit-box-orient: vertical;
    overflow: hidden;
}
</style>