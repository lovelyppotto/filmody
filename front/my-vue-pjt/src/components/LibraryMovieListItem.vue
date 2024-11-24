<template>
    <div class="movie-item-wrapper">
        <div class="card h-100" @click="goToDetail(movie.id)" v-if="movie">
            <img 
                :src="`${movie.poster_url}`" 
                class="card-img-top"
                :alt="movie.title"
            >
            <div class="card-body">
                <h5 class="card-title">{{ movie.title }}</h5>
                <p class="card-text">장르 : {{ movie.genre }}</p>
                <p class="card-text">
                    <small class="text-muted">
                        등급: {{ movie.rating }}
                    </small>
                </p>
            </div>
        </div>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
const router = useRouter()
defineProps({
    movie:Object
})
const goToDetail = (movieId) => {
    router.push(`/movies/${movieId}`)
}
</script>

<style scoped>
.movie-item-wrapper {
    padding: 0.75rem;  /* 각 아이템에 패딩 추가 */
}

.card {
    transition: transform 0.2s;
    height: 100%;
    border-radius: 8px;
    overflow: hidden;
}

.card:hover {
    transform: scale(1.02);
}

.card-img-top {
    height: 400px;
    object-fit: cover;
    width: 100%;
}

.card-body {
    padding: 1rem;
}

.card-title {
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}

.card-text {
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
    margin-bottom: 0.5rem;
}

.text-muted {
    color: #6c757d;
}
</style>