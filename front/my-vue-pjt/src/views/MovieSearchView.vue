<!-- MovieSearch.vue -->
<template>
    <div class="search-container" :class="{ 'has-results': hasResults }">
      <div class="search-box-wrapper" :class="{ 'centered': !hasResults }">
        <SearchBox 
          v-model="searchQuery"
          :is-loading="movieStore.isLoading"
        />
      </div>
      <transition name="fade">
        <div v-if="hasResults" class="results-wrapper">
          <SearchResults />
        </div>
      </transition>
    </div>
  </template>
  
  <script setup>
  import { ref, watch, computed } from 'vue'
  import { useMovieStore } from '@/stores/movie.js'
  import SearchBox from '@/components/SearchBox.vue'
  import SearchResults from '@/components/SearchResults.vue'
  
  const movieStore = useMovieStore()
  const searchQuery = ref('')
  
  const hasResults = computed(() => {
    return movieStore.searchResults?.length > 0
  })
  
  watch(searchQuery, (newQuery) => {
    if (newQuery) {
      movieStore.searchMovies(newQuery)
    } else {
      movieStore.clearSearchResults()
    }
  })
  </script>
  
  <style scoped>
  .search-container {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
  }
  
  .search-box-wrapper {
    display: flex;
    align-items: flex-start;  /* 기본적으로 상단에 위치 */
    justify-content: center;
    padding: 20px;
    min-height: 100px;  /* 최소 높이 설정 */
    transform: translateY(0);
    transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  }
  
  .search-box-wrapper.centered {
    min-height: 100vh;
    align-items: center;
    transform: translateY(0);
  }
  
  .has-results .search-box-wrapper {
    flex: 0;
    position: sticky;
    top: 0;
    background: white;
    z-index: 10;
    padding: 1rem;
    transform: translateY(0);
  }
  
  .results-wrapper {
    flex: 1;
    padding: 20px;
    overflow-y: auto;
  }
  
  /* 페이드 트랜지션 */
  .fade-enter-active,
  .fade-leave-active {
    transition: opacity 0.5s ease;
  }
  
  .fade-enter-from,
  .fade-leave-to {
    opacity: 0;
  }
  
  /* 위치 이동 트랜지션 */
  .search-box-wrapper {
    will-change: transform, min-height;
  }
  </style>