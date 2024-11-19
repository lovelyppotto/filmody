<template>
    <div class="search-container">
        <SearchInput 
            v-model="searchQuery"
            :is-loading="isLoading"
        />
        <SearchResults 
            :results="SearchResults"
            @select="selecteMovie"
        />

        <div v-if="selectedMovie" class="selected-movie">
            <h2>선택된 영화</h2>
            <div class="movie-detail">
                <h3>{{ selectedMovie.title }}</h3>
                <p>감독: {{ selectedMovie.director }}</p>
                <p>개봉년도: {{ selectedMovie.releaseYear }}</p>
                <button @click="searchPlaylist" class="search-playlist-btn">
                플레이리스트 검색
                </button>
            </div>  
        </div>
    </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import SearchInput from '@/components/SearchInput.vue'
import SearchResults from '@/components/SearchResults.vue'
import axios from 'axios'

const searchQuery = ref('')
const searchResults = ref([])
const selectedMovie = ref(null)
const isLoading = ref(false)

watch(searchQuery, async (newQuery) => {
  if (newQuery.length < 2) {
    searchResults.value = []
    return
  }
  
  try {
    isLoading.value = true
    const response = await axios.get('/api/movies/search', {
      params: { query: newQuery }
    })
    searchResults.value = response.data
  } catch (error) {
    console.error('검색 중 오류 발생:', error)
  } finally {
    isLoading.value = false
  }
}, { debounce: 300 })

const selectMovie = (movie) => {
  selectedMovie.value = movie
  searchResults.value = []
  searchQuery.value = ''
}

const searchPlaylist = async () => {
  if (!selectedMovie.value) return
  try {
    // 여기에 플레이리스트 검색 로직 추가
    console.log(`${selectedMovie.value.title} 관련 플레이리스트 검색 중...`)
  } catch (error) {
    console.error('플레이리스트 검색 중 오류:', error)
  }
}

</script>

<style scoped>

</style>