import { ref, computed } from "vue";
import { debounce } from "lodash"
import { defineStore } from "pinia";
import axios from "axios";
// import router from "@/router";
import { useAuthStore } from "@/stores/auth";

export const useMovieStore = defineStore("movie", () => {
  const authStore = useAuthStore(); 
  const BASE_URL = 'http://127.0.0.1:8000'
  const videos = ref([]);
  
  // 박스 오피스 영화들
  const recommendMovies = ref([]);
  
  // 내가 좋아요 한 영화들
  const likedMovies = ref([]);

  // 검색결과
  const searchResults = ref([]);
  const movieDetail = ref([]);

  const isLoading = ref(false);
  const searchQuery = ref('');

  const getVideos = computed(() => videos.value);
  const API_KEY = import.meta.env.VITE_APP_YOUTUBE_API_KEY;
  // const TMDB_API_URL = 'https://api.themoviedb.org/3'
  // const TMDB_API_KEY = import.meta.env.VITE_TMDB_KEY  // v3 API 키 사용

  // YouTube API 검색
  const searchReview = (keyword) => {
    isLoading.value = true;
    return axios({
      url: "https://www.googleapis.com/youtube/v3/search",
      method: "GET",
      params: {
        part: "snippet",
        q: keyword,
        type: "video",
        maxResults: 10,
        key: API_KEY,
      },
    })
      .then((response) => {
        videos.value = response.data.items;
        return videos.value;
      })
      .catch((err) => {
        console.error('YouTube 검색 실패:', err);
        throw err;
      })
      .finally(() => {
        isLoading.value = false;
      });
  };

  // 플레이리스트에 비디오 추가
  const addVideoToPlaylist = (playlistId, videoData) => {
    const formattedVideoData = {
      video_id: videoData.id.videoId,
      title: videoData.snippet.title,
      description: videoData.snippet.description,
      thumbnail_url: videoData.snippet.thumbnails.default.url,
    };

    return axios({
      method: 'post',
      url: `${authStore.BASE_URL}/api/playlist/${playlistId}/videos/`,
      data: formattedVideoData,
      headers: {
        'Authorization': `Token ${authStore.token}`,
        'Content-Type': 'application/json',
      }
    });
  };


  // 영화 및 감독 검색 기능
  const searchMovies = debounce((keyword) => {
    if (!keyword.trim()) {
      searchResults.value = [] // 검색어가 비어 있으면 초기화
      return
    }

    isLoading.value = true
    axios.get(`${BASE_URL}/api/movies/search/`, {
      params: { search: keyword }
    })
    .then((response) => {
      searchResults.value = response.data
    })
      .catch((error) => {
        console.error('검색 중 오류 발생:', error)
        searchResults.value = []
      })
      .finally(() => {
        isLoading.value = false
      })
  }, 500)


  function clearSearchResults() {
    searchResults.value = []
  }

  // 박스오피스 영화 가져오기
  const fetchRecommendMovies = () => {
    axios({
      method:'get',
      url:`${BASE_URL}/api/movies/recommend/`,
    })
    .then((response) => {
      // console.log(response.data)
      recommendMovies.value = response.data
    })
    .catch((error) => {
      console.error('추천 영화 데이터 로딩 실패:', error)
    })
  }

  // 박스오피스 영화 클릭했을 때
  const fetchMovieDetail = async (movie_id) => {
    try {
      const token = authStore.token
      const response = await axios({
        method:'get',
        url:`${BASE_URL}/api/movies/${movie_id}`,
        headers: token ? {
          Authorization: `Token ${token}`
      } : {}
      })
        movieDetail.value = response.data
        return response.data
    } catch (error) {
      console.error('영화 상세 데이터 로딩 실패:', error)
    }
  }

    // 내가 좋아요한 영화 목록 불러오기
    const fetchLikedMovies = () => {
      axios({
        method:'get',
        url:`${BASE_URL}/api/movies/liked-movies/`,
        headers: {
          Authorization: `Token ${authStore.token}`,
        }
      })
      .then((response) => {
        console.log(response.data)
        likedMovies.value = response.data
      })
      .catch((error) => {
        console.error(error);
      })
    }

    
  return{
    BASE_URL,
    searchResults,
    isLoading,
    searchQuery,
    videos,
    getVideos,
    movieDetail,
    searchReview,
    recommendMovies,
    searchMovies,
    clearSearchResults,
    fetchRecommendMovies,
    fetchMovieDetail,
    fetchLikedMovies,
    likedMovies
  }
}, { persist: true });