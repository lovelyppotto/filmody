<template>
    <div v-if="movieStore.movieDetail" class="movie-detail-container">
        <!-- 포스터 이미지 -->
        <img 
            class="movie-poster"
            :src="`${movieStore.movieDetail.poster_url}`" 
            :alt="movieStore.movieDetail.title" 
            @error="handleImageError"
        >
        
        <!-- 영화 정보 -->
        <div class="movie-info">
            <h4 class="movie-title">{{ movieStore.movieDetail.title }}</h4>
            <p><strong>장르:</strong> {{ movieStore.movieDetail.genre }}</p>
            <p><strong>감독:</strong> {{ movieStore.movieDetail.director[0].name }}</p>
            <p><strong>개봉년도:</strong> {{ movieStore.movieDetail.open_year }}</p>
            <p class="movie-plot"><strong>줄거리:</strong> {{ movieStore.movieDetail.plot }}</p>
        </div>

        <!-- 좋아요 버튼 -->
        <button @click="handleLike" class="like-button">
            <span :class="{ 'text-red': isLiked }">
                <i v-if="isLiked" class="fa-solid fa-heart"></i>
                <i v-else class="fa-regular fa-heart"></i>
            </span>
            좋아요 {{ likeCount }}
        </button>
    </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useMovieStore } from '@/stores/movie'
import { useAuthStore } from '@/stores/auth'
import { useRoute, useRouter } from 'vue-router';

import axios from 'axios'
const movieStore = useMovieStore()
const authStore = useAuthStore()
const route = useRoute()
const router = useRouter()

const isLiked = ref(false)
const likeCount = ref(0)

onMounted(async ()=>{
    const movieId = route.params.id
    await movieStore.fetchMovieDetail(movieId)
    updateLikeStatus()
})

// 초기 좋아요 상태와 카운트 설정
const updateLikeStatus = () => {
    if(movieStore.movieDetail){
        isLiked.value = movieStore.movieDetail.is_liked
        likeCount.value = movieStore.movieDetail.like_count
    }
}

// movieDetail이 변경될 때 마다 updateLikeStatus 함수를 부름
watch(() => movieStore.movieDetail, updateLikeStatus)


const handleLike = async () => {
    if (!authStore.token) {
        alert('로그인이 필요한 서비스입니다.')
        router.push({name:'LogInView'})
        return
    }

    try {
        const response = await axios({
            method: 'post',
            url: `${movieStore.BASE_URL}/api/movies/${movieStore.movieDetail.id}/like/`,
            headers: {
                Authorization: `Token ${authStore.token}`
            }
        })
        
        isLiked.value = response.data.liked
        likeCount.value = response.data.like_count
        
    } catch (error) {
        console.error('좋아요 실패:', error)
        if (error.response?.status === 401) {
            alert('로그인이 필요한 서비스입니다.')
        }
    }
}
</script>

<style scoped>
/* 전체 컨테이너 스타일 */
.movie-detail-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* 포스터 이미지 스타일 */
.movie-poster {
    display: block;
    width: 100%;
    max-height: 400px;
    object-fit: contain;
    margin-bottom: 20px;
    border-radius: 8px;
    background-color: #f0f0f0; /* 이미지 없는 경우 여백 색상 */
}

/* 영화 정보 스타일 */
.movie-info {
    margin-bottom: 20px;
}

.movie-title {
    font-size: 1.5em;
    font-weight: bold;
    margin-bottom: 10px;
    color: #333;
}

.movie-plot {
    margin-top: 10px;
    line-height: 1.6;
    color: #555;
}

/* 좋아요 버튼 스타일 */
.like-button {
    display: flex;
    align-items: center;
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    background-color: #f5f5f5;
    font-size: 1em;
    cursor: pointer;
    transition: background-color 0.3s, transform 0.2s;
}

.like-button:hover {
    background-color: #e9ecef;
    transform: translateY(-2px);
}

.text-red {
    color: #e10600;
    font-size: 1.2em;
}

button span {
    margin-right: 8px;
    display: inline-flex;
    align-items: center;
}
</style>