<template>
    <div class="container">
        <div class="content-container">
            <div class="header-section">
                <h2 class="title">좋아요한 영화</h2>
                <p class="subtitle">마음에 드는 영화를 모아보세요 :)</p>
            </div>
            <div class="row">
                <LibraryMovieListItem 
                    v-for="movie in store.likedMovies"
                    :key="movie.id"
                    :movie="movie"
                    class="col-12 col-md-6 col-lg-4"  
                />
            </div>
        </div>
    </div>
</template>

<script setup>
import LibraryMovieListItem from '@/components/LibraryMovieListItem.vue';
import { useMovieStore } from '@/stores/movie';
import { onMounted } from 'vue';

const store = useMovieStore()
onMounted(() => {
    store.fetchLikedMovies()
})
</script>

<style scoped>
.container {
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem 0;
}

.content-container {
    padding: 0 1rem;
}

.header-section {
    margin-bottom: 2rem;
    padding: 0 0.5rem;
}

.title {
    font-size: 1.5em;
    font-weight: bold;
    margin-bottom: 0.5rem;
}

.subtitle {
    font-size: 1.1em;
    color: #4A4A4A;
    margin: 0;
}

.row {
    display: flex;
    flex-wrap: wrap;
    margin: -0.75rem;
}

/* 반응형 조정 */
@media (max-width: 992px) {
    /* 태블릿: 2개씩 */
    .col-md-6 {
        flex: 0 0 50%;
        max-width: 50%;
    }
}

@media (max-width: 768px) {
    /* 모바일: 1개씩 */
    .col-12 {
        flex: 0 0 100%;
        max-width: 100%;
    }
    
    .container {
        padding: 1rem 0;
    }

    .content-container {
        padding: 0 0.5rem;
    }
}
</style>