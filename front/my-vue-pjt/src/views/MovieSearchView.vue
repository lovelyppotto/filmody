// views/MovieSearch.vue
<template>
    <div class="search-container">
        <SearchBox 
            v-model="searchQuery"
            :is-loading="movieStore.isLoading"
        />
        <SearchResults />
    </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useMovieStore } from '@/stores/movie.js'
import SearchBox from '@/components/SearchBox.vue'
import SearchResults from '@/components/SearchResults.vue'

const movieStore = useMovieStore()
const searchQuery = ref('')

watch(searchQuery, (newQuery) => {
    if (newQuery) {
        movieStore.searchMovies(newQuery)
    } else {
        // 검색어가 비었을 때 검색 결과 초기화
        movieStore.clearSearchResults()  // store에 이 메서드 추가 필요
    }
})

// watch(keyword, (newKeyword) => {
//   movieStore.searchMovies(newKeyword)
// })
</script>