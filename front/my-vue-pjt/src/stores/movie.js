import { ref, computed } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import router from "@/router";

export const useMovieStore = defineStore("movie", () => {

  // state
  const videos = ref([]);
  const recommendMovies = ref([])
  const movieDetail = ref([])
  const searchResults = ref([])
  const selectedMovie = ref(null)
  const isLoading = ref(false)


  const API_KEY = import.meta.env.VITE_APP_YOUTUBE_API_KEY;
  const TMDB_API_URL = 'https://api.themoviedb.org/3'
  const TMDB_API_KEY = import.meta.env.VITE_TMDB_KEY  // v3 API 키 사용
  const SPOTYFY_API_URL = import.meta.env.SPOTYFY_API_URL
  
  
  // getters
  const getVideos = computed(() => videos.value);
  const hasResult = computed(() => searchResults.value.length > 0)
  const currentMovie = computed(() => selectedMovie.value)


  // actions

  // 리뷰 검색
  const searchReview = (keyword) => {
    axios({
      url: "https://www.googleapis.com/youtube/v3/search",
      method: "GET",
      params: {
        part: "snippet",
        q: keyword,
        type: "video",
        key: API_KEY,
      },
    })
      .then((response) => {
        videos.value = response.data.items;
        console.log(videos.value);
        router.push({ name: "ReviewSearchView" });
      })
      .catch((err) => {
        console.log(err);
      });
  };
    
  const fetchTopRatedMovies = () => {
      axios({
          method: 'get',
          url: `${TMDB_API_URL}/movie/top_rated`,
          params: {
              api_key: TMDB_API_KEY,  // Bearer 토큰이 아닌 API 키 사용
              language: 'ko-KR',
              page: 1
          }
      })
      .then(response => {
          recommendMovies.value = response.data.results
          // console.log(recommendMovies.value)
      })
      .catch(error => {
          console.error('영화 데이터 로딩 실패:', error.response?.data || error)
      })
  }

  const fetchMovieDetail = (movieId) => {
      axios({
          method: 'get',
          url: `${TMDB_API_URL}/movie/${movieId}`,
          params: {
              api_key: TMDB_API_KEY,  
              language: 'ko-KR',
              page: 1
          }
      })
      .then(response => {
          movieDetail.value = response.data
          console.log(movieDetail)
      })
      .catch(error => {
          console.error('영화 세부정보 로딩 실패:', error.response?.data || error)
      })
  }

// 여기손보는중...........
// ㄱㄴ데....
// 플레이리스트... 스토어... 파일 필요할듯...


  // 검색 관련
//   const handleSearch = (payload) => {
//     if (payload.length < 2) {
//       searchResults.value = []
//       return
//     }

//     isLoading.value = true

//     axios({
//       url: 'api/movies/search',
//       method: 'GET',
//       params: {payload}
//     })
//       .then((response) => {
//         searchResults.value = response.data
//       })
//       .catch((error) => {
//         console.error('검색 중 오류 발생:', error)
//         searchResults.value = []
//       })
//       .finally(() => {
//         isLoading.value = false
//       })
//   }

//   const selectMovie = (movie) => {
//     selectedMovie.value = movie
//     searchResults.value = []
//   }


//   return {
//     videos,
//     getVideos,
//     movieDetail,
//     searchReview,
//     recommendMovies,
//     fetchTopRatedMovies,
//     fetchMovieDetail,
//     handleSearch,
//     selectMovie,
//   };
// });