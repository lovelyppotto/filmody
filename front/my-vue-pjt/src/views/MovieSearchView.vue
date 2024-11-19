// views/MovieSearch.vue
<template>
    <div class="search-container">
        <SearchInput 
            v-model="searchQuery"
            :is-loading="movieStore.isLoading"
        />
        <SearchResults 
            :results="movieStore.searchResults"
            @select="movieStore.selectMovie"
        />

        <div v-if="movieStore.selectedMovie" class="selected-movie">
            <h2>선택된 영화</h2>
            <div class="movie-detail">
                <h3>{{ movieStore.selectedMovie.title }}</h3>
                <p>감독: {{ movieStore.selectedMovie.director }}</p>
                <p>개봉년도: {{ movieStore.selectedMovie.releaseYear }}</p>
                <button 
                    @click="createPlaylist" 
                    :disabled="playlistStore.isLoading"
                    class="create-playlist-btn"
                >
                    {{ playlistStore.isLoading ? '플레이리스트 생성 중...' : 'OST 플레이리스트 생성' }}
                </button>
            </div>  
        </div>

        <!-- 저장된 플레이리스트 목록 -->
        <div v-if="playlistStore.playlists.length > 0" class="playlist-list">
            <h3>내 플레이리스트</h3>
            <div v-for="playlist in playlistStore.playlists" :key="playlist.id" class="playlist-item">
                <p>{{ playlist.movie_title }}</p>
                <a :href="playlist.spotify_url" target="_blank" class="spotify-link">
                    스포티파이에서 열기
                </a>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useMovieStore, usePlaylistStore } from '@/stores/store'
import SearchInput from '@/components/SearchInput.vue'
import SearchResults from '@/components/SearchResults.vue'

const movieStore = useMovieStore()
const playlistStore = usePlaylistStore()

const searchQuery = ref('')

watch(searchQuery, (payload) => {
    if (payload.length >= 2) {
        movieStore.handleSearch(payload.value)
    }
}, { debounce: 300 })

const createPlaylist = () => {
    if (movieStore.selectedMovie) {
        playlistStore.createPlaylist(movieStore.selectedMovie)
    }
}

onMounted(() => {
    playlistStore.getUserPlaylists()
})
</script>