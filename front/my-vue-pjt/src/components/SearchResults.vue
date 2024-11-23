<!-- SearchResults.vue -->
<template>
  <div class="container">
    <div v-if="isLoading" class="text-center py-4">
      검색 중...
    </div>
    
    <div v-else-if="searchResults && searchResults.length > 0" class="row g-4">
      <div v-for="movie in searchResults" :key="movie.id" class="col-12 col-md-6 col-lg-4">
        <div 
          class="card h-100 cursor-pointer" 
          @click="handleMovieClick(movie.id)"
        >
          <img 
            :src="movie.poster_url" 
            :alt="movie.title" 
            class="card-img-top"
          />
          <div class="card-body">
            <h5 class="card-title">{{ movie.title }}</h5>
            <p class="card-text">
              감독: {{ movie.director && movie.director.length 
                ? movie.director.map(d => d.name).join(', ') 
                : '정보 없음' }}
            </p>
            <p class="card-text">장르: {{ movie.genre }}</p>
            <p class="card-text">개봉: {{ movie.open_year }}</p>
            <p class="card-text">관람등급: {{ movie.rating }}</p>
          </div>
        </div>
      </div>
    </div>
      
    <div v-else class="text-center py-4">
      검색 결과가 없습니다.
    </div>
  </div>
</template>

<script setup>
import { storeToRefs } from 'pinia'
import { useMovieStore } from '@/stores/movie'
import { useRouter } from 'vue-router'
import { watch } from 'vue'

const router = useRouter()
const movieStore = useMovieStore()
const { searchResults, isLoading } = storeToRefs(movieStore)

const handleMovieClick = async (movieId) => {
  try {
    await movieStore.fetchMovieDetail(movieId)
    router.push(`/movies/${movieId}`)  // 영화 상세 페이지로 이동
  } catch (error) {
    console.error('영화 상세 정보 로딩 실패:', error)
  }
}

watch(searchResults, (newResults) => {
  console.log('Search Results:', newResults)
  const ids = newResults.map(movie => movie.id)
  console.log('IDs:', ids)
})
</script>
 
 <style scoped>
 .card {
  transition: transform 0.2s ease;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
 }
 
 .card:hover {
  transform: translateY(-5px);
 }
 
 .card-img-top {
  height: 500px;
  object-fit: cover;
 }
 
 .card-text {
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
 }
 </style>