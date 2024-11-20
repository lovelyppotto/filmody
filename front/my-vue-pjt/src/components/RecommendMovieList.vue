<!-- RecommendView.vue -->
<template>
    <div class="container mt-5">
      <div id="movieCarousel" class="carousel slide" data-bs-ride="carousel">
        <!-- 인디케이터 -->
        <div class="carousel-indicators">
          <button 
            v-for="(_, index) in Math.ceil(store.recommendMovies.length / 4)" 
            :key="index"
            type="button" 
            data-bs-target="#movieCarousel" 
            :data-bs-slide-to="index" 
            :class="{ active: index === 0 }"
            aria-current="true">
          </button>
        </div>
  
        <!-- 캐러셀 내용 -->
        <div class="carousel-inner">
          <div 
            v-for="(chunk, index) in movieChunks" 
            :key="index" 
            class="carousel-item"
            :class="{ active: index === 0 }"
          >
            <div class="row">
              <RecommendMovieListItem 
                v-for="movie in chunk"
                :key="movie.id"
                :movie="movie"
              />
            </div>
          </div>
        </div>
  
        <!-- 이전/다음 버튼 -->
        <button class="carousel-control-prev rounded-circle" type="button" data-bs-target="#movieCarousel" data-bs-slide="prev">
            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Previous</span>
        </button>
        <button class="carousel-control-next rounded-circle" type="button" data-bs-target="#movieCarousel" data-bs-slide="next">
            <span class="carousel-control-next-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Next</span>
        </button>
      </div>
    </div>
  </template>
  
  <script setup>
  import { onMounted, computed } from 'vue'
  import { useMovieStore } from '@/stores/movie.js'
  import RecommendMovieListItem from '@/components/RecommendMovieListItem.vue';
  
  const store = useMovieStore()
  
  // 4개씩 영화 묶기
  const movieChunks = computed(() => {
    const chunks = []
    for (let i = 0; i < store.recommendMovies.length; i += 4) {
      chunks.push(store.recommendMovies.slice(i, i + 4))
    }
    return chunks
  })
  
  onMounted(() => {
    store.fetchRecommendMovies()
  })
  </script>
  
  <style scoped>
  .carousel {
    padding-bottom: 50px;  /* 인디케이터를 위한 여백 */
  }
  
  .carousel-control-prev,
.carousel-control-next {
  width: 40px;  /* 버튼 크기 조절 */
  height: 40px;
  border-radius: 50%;  /* 동그랗게 */
  background-color: rgba(0, 0, 0, 0.5);  /* 배경색 */
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
}

.carousel-control-prev {
  left: -20px;  /* 위치 조정 */
}

.carousel-control-next {
  right: -20px;  /* 위치 조정 */
}

.carousel-control-prev:hover,
.carousel-control-next:hover {
  background-color: rgba(0, 0, 0, 0.7);  /* 호버 시 더 진한 배경 */
}

/* 화살표 아이콘 크기 조정 */
.carousel-control-prev-icon,
.carousel-control-next-icon {
  width: 20px;
  height: 20px;
}
  </style>