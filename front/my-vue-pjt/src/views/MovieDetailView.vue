<template>
    <div v-if="movieStore.movieDetail">  <!-- v-if 추가 -->
        <img 
            :src="`${movieStore.movieDetail.poster_url}`" 
            :alt="movieStore.movieDetail.title"
        >       
        <h4>{{ movieStore.movieDetail.title }}</h4>
        <p>장르: {{ movieStore.movieDetail.genre }}</p>
        <p>감독: {{ movieStore.movieDetail.director[0].name }}</p>
        <p>개봉년도 : {{ movieStore.movieDetail.open_year }}</p>
        <p>줄거리 : {{ movieStore.movieDetail.plot }}</p>
        <button @click="handleLike" class="like-button">
            <!-- 하트 이모지 변경 -->
            <span :class="{ 'text-red': isLiked }">
                <i v-if="isLiked"class="fa-solid fa-heart" style="color: #e10600;"></i>
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
.like-button {
    padding: 8px 16px;
    border: 1px solid #ddd;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.3s;
}

.like-button:hover {
    background-color: #f5f5f5;
}

.text-red {
    color: red;
}

button span {
    margin-right: 4px;
    font-size: 1.2em;
}
</style>