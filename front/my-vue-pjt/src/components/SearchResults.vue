<!-- SearchResults.vue -->
<template>
    <div class="search-results">
      <div v-if="isLoading" class="loading">검색 중...</div>
      
      <div v-else-if="searchResults && searchResults.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 p-4">
        <div v-for="movie in searchResults" :key="movie.id" class="card">
          <img 
            :src="movie.poster_url" 
            :alt="movie.title" 
            class="w-full h-64 object-cover mb-4"
          />
          <h3 class="text-xl font-bold mb-2">{{ movie.title }}</h3>
          <p class="text-sm text-gray-600 mb-2">
            감독: {{ movie.director && movie.director.length 
              ? movie.director.map(d => d.name).join(', ') 
              : '정보 없음' }}
          </p>
          <p class="text-sm text-gray-600">장르: {{ movie.genre }}</p>
          <p class="text-sm text-gray-600">개봉: {{ movie.open_year }}</p>
          <p class="text-sm text-gray-600">관람등급: {{ movie.rating }}</p>
        </div>
      </div>
        
      <div v-else class="no-results">
        검색 결과가 없습니다.
      </div>
    </div>
</template>
  
  <script setup>
    import { storeToRefs } from 'pinia'
    import { useMovieStore } from '@/stores/movie'
    import { onMounted, watch } from 'vue'  // watch 추가

    const movieStore = useMovieStore()
    const { searchResults, isLoading } = storeToRefs(movieStore)

    // 데이터 구조 확인
    watch(searchResults, (newResults) => {
  console.log('Search Results:', newResults)
  const ids = newResults.map(movie => movie.id)
  console.log('IDs:', ids)
})



</script>
  
  <style scoped>
  .card {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 1rem;
    background: white;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }
  
  .loading, .no-results {
    text-align: center;
    padding: 2rem;
    color: #666;
  }
  </style>