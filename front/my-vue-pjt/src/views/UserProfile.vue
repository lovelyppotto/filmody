<template>
    <div class="profile-page" v-if="authStore.userProfile">
      <!-- {{ authStore.userLikedPlaylists }} | -->
      <!-- {{ authStore.userLikedMovies }} | -->
      <!-- 상단 프로필 -->
      <div class="profile-header">
        <div class="avatar">
          <img :src=profileImageUrl alt="프로필 사진" />
        </div>
        <div class="info">
          <h2>{{ authStore.userProfile.nickname }}</h2>
          <p>팔로워 <strong>7</strong> | 팔로잉 <strong>6</strong></p>
          <button class="follow-btn">팔로우</button>
        </div>
      </div>
  

    <!-- 보관함 -->
    <div class="collection-section">
      <h3>보관함</h3>
      <div class="categories">
        <div
          class="category"
          :class="{ active: selectedCategory === 'playlist' }"
          @click="selectCategory('playlist')"
        >
          Created Playlist
        </div>
        <div
          class="category"
          :class="{ active: selectedCategory === 'likedPlaylist' }"
          @click="selectCategory('likedPlaylist')"
        >
          Liked Playlist
        </div>
        <div
          class="category"
          :class="{ active: selectedCategory === 'likedMovies' }"
          @click="selectCategory('likedMovies')"
        >
          Liked Movies
        </div>
      </div>
    </div>

    <!-- 선택된 카테고리의 콘텐츠 -->
    <div class="content-section">
      <h3>{{ selectedTitle }}</h3>
        <!-- 내 플레이리스트 -->
        <div v-if="selectedCategory === 'playlist'" class="playlist-grid">
          <div v-if="authStore.userPlaylists.length === 0" class="no-content">
            <p>아직 생성한 플레이리스트가 없습니다.</p>
          </div>
          <PlaylistCard 
            v-else
            v-for="playlist in authStore.userPlaylists" 
            :key="playlist.id"
            :playlist="playlist"
            :use-base-url="true"
            @click="navigateToPlaylist(playlist.id)"
          />
          </div>

        <!-- 좋아요한 플레이리스트 -->
        <div v-if="selectedCategory === 'likedPlaylist'" class="playlist-grid">
          <div v-if="authStore.userLikedPlaylists.length === 0" class="no-content">
            <p>아직 좋아요한 플레이리스트가 없습니다.</p>
          </div>
          <PlaylistCard 
            v-else
            v-for="playlist in authStore.userLikedPlaylists" 
            :key="playlist.id"
            :playlist="playlist"
            :use-base-url="true"
            @click="navigateToPlaylist(playlist.id)"
          />
        </div>

        <!-- 좋아요한 영화 -->
        <div v-if="selectedCategory === 'likedMovies'" class="playlist-grid">
          <div v-if="authStore.userLikedMovies.length === 0" class="no-content">
            <p>아직 좋아요한 영화가 없습니다.</p>
          </div>
          <div 
            v-else
            v-for="movie in authStore.userLikedMovies" 
            :key="movie.id"
            class="card h-100 hover:shadow-lg transition-all cursor-pointer"
            @click="navigateToMovie(movie.id)"
          >
            <div class="position-relative">
              <img 
                v-if="movie.poster_url"
                :src="movie.poster_url"
                :alt="movie.title"
                class="card-img-top"
                @error="handleImageError"
              />
              <div v-else class="no-image-placeholder">
                <span>No Image</span>
              </div>
            </div>
            
            <div class="card-body">
              <h5 class="card-title mb-1 text-truncate">{{ movie.title }}</h5>
              <p class="card-text">
                <small class="text-muted">{{ movie.open_year }}</small>
              </p>
            </div>
          </div>
        </div>
    </div>
  </div>
  </template>
  
  <script setup>
  import { ref, computed, onMounted } from 'vue';
  import { useAuthStore } from '@/stores/auth';
  import { useRoute, useRouter} from 'vue-router';
  import PlaylistCard from '@/components/Playlist/PlaylistCard.vue';

  const route = useRoute();
  const router = useRouter();
  const authStore = useAuthStore();
  const selectedCategory = ref('playlist');

  onMounted(() => {
  const userId = route.params.id;
  authStore.fetchUserProfile(userId);
  });

  const profileImageUrl = computed(() => 
      `${authStore.BASE_URL}${authStore.userProfile.profile_image}`
    );

  
  // 카테고리 변경 함수
  const selectCategory = (category) => {
  selectedCategory.value = category;
  };

  // 해당 플레이리스트로 이동
  const navigateToPlaylist = (playlistId) => {
    router.push(`/playlist/${playlistId}`);
  };
  
  // 해당 영화 상세페이지로 이동
  const navigateToMovie = (movieId) => {
    router.push(`/movies/${movieId}`);
  };
  </script>
  
  <style scoped>
  /* 전체 페이지 스타일 */
  .profile-page {
    font-family: 'Arial', sans-serif;
    background-color: #f8f8f8;
    padding: 30px;
    max-width: 800px;
    margin: 0 auto;
  }
  
  /* 프로필 헤더 스타일 */
  .profile-header {
    display: flex;
    align-items: center;
    background-color: #fff;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    margin-bottom: 30px;
  }
  
  .avatar img {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    margin-right: 20px;
  }
  
  .info {
    flex: 1;
  }
  
  .info h2 {
    margin: 0;
    font-size: 24px;
    color: #333;
  }
  
  .info p {
    margin: 5px 0;
    color: #777;
  }
  
  .follow-btn {
    background-color: #000;
    color: #fff;
    border: none;
    padding: 10px 20px;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .follow-btn:hover {
    background-color: #333;
  }
  
  /* 보관함 스타일 */
  .collection-section {
    background-color: #fff;
    margin-top: 25px;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    margin-bottom: 30px;
  }
  
  .collection-section h3 {
    margin: 0 0 20px;
    font-size: 20px;
    color: #333;
  }
  
  .categories {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 15px;
  }
  
  .category {
    background-color: #f0f0f0;
    padding: 20px;
    text-align: center;
    border-radius: 8px;
    font-size: 16px;
    font-weight: bold;
    color: #555;
    cursor: pointer;
  }
  
  .card {
  border: 1px solid rgba(0,0,0,.125);
  border-radius: 0.5rem;
  background-color: white;
  margin: 0;
  height: 100%; /* 높이 균일화 */
}

.card:hover {
  transform: translateY(-2px);
}

.card-body {
  padding: 1rem;
}

.card-title {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.text-muted {
  color: #6c757d;
}

.category.active {
  background-color: #000;
  color: white;
}

/* 플레이리스트 그리드 */
.playlist-grid {
  display: grid;
  gap: 30px; /* 카드 간격 */
}

/* 이미지 스타일 */
.card-img-top {
  display: block;
  width: 100%;
  max-height: 400px;
  object-fit: contain;
  margin-bottom: 20px;
  border-radius: 8px;
  background-color: #f0f0f0; /* 이미지 없는 경우 여백 색상 */
}
</style>