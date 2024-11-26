<template>
    <div class="container py-4">
        <!-- 헤더 섹션 -->
        <div class="mb-4">
            <h2 class="text-2xl"><i class="fa-solid fa-clapperboard" style="color: #203250;"></i> 좋아요한 영화</h2>
            <p class="text-gray-600">마음에 드는 영화를 모아보세요 :)</p>
        </div>
 
        <!-- 에러 메시지 -->
        <div v-if="!authStore.token" class="text-center py-8">
            <p class="text-red-500">{{ movieStore.error }}</p>
            <button 
                @click="redirectToLogin" 
                class="mt-4 px-4 py-2 !bg-indigo-500 text-black rounded hover:!bg-indigo-600"
            >
                로그인
            </button>
        </div>
 
        <!-- 영화 목록 -->
        <div v-else class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
            <div 
                v-for="movie in movieStore.likedMovies" 
                :key="movie.id"
                class="col"
            >
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
            </div>
        </div>
 
        <!-- 데이터가 없을 때 -->
        <div v-if="!movieStore.loading && !movieStore.error && movieStore.likedMovies.length === 0" class="text-center py-8">
            <p class="text-gray-500">아직 좋아요한 영화가 없습니다.</p>
        </div>
    </div>
 </template>
 
 <script setup>
 import { useMovieStore } from '@/stores/movie';
 import { useRouter } from 'vue-router';
 import { onMounted } from 'vue';
 import { useAuthStore } from '@/stores/auth';
 
 const movieStore = useMovieStore();
 const authStore = useAuthStore();
 const router = useRouter();
 
 const goToDetail = (movieId) => {
    router.push(`/movies/${movieId}`);
 };
 
 onMounted(() => {
    movieStore.fetchLikedMovies();
 });

 const redirectToLogin = () => {
  router.push({ name: 'LogInView' })  
}
 </script>
 
 <style scoped>
 .movie-item-wrapper {
    padding: 0.75rem;
 }
 
 .card {
    transition: transform 0.2s;
    height: 100%;
    border-radius: 8px;
    overflow: hidden;
    cursor: pointer;
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
 
 /* 반응형 조정 */
 @media (max-width: 992px) {
    .row-cols-md-2 > * {
        flex: 0 0 50%;
        max-width: 50%;
    }
 }
 
 @media (max-width: 768px) {
    .row-cols-1 > * {
        flex: 0 0 100%;
        max-width: 100%;
    }
 }
 </style>