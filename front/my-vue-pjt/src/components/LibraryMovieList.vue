<template>
    <div class="row g-4 mx-3">
        <template v-if="hasLikedMovies">
            {{ hasLikedMovies }}
            <LibraryMovieListItem 
                v-for="movie in store.likedMovies"
                :key="movie.id"
                :movie="movie"
                class="col-12 col-md-6 col-lg-4"
            />
        </template>
        <template v-else>
            <div class="col-12 text-center">
                <p>아직 좋아요한 영화가 없습니다.</p>
            </div>
        </template>
    </div>
</template>
<script setup>
import LibraryMovieListItem from '@/components/LibraryMovieListItem.vue';
import { useMovieStore } from '@/stores/movie';
import { onMounted } from 'vue';
const store = useMovieStore()
const hasLikedMovies = computed(() => store.likedMovies.length > 0)

onMounted(() => {
    store.fetchLikedMovies()
})

</script>

<style scoped>
/* 카드 간격 */
.row.g-4 {
  gap: 1.5rem; /* 카드 간격 */
}
</style>