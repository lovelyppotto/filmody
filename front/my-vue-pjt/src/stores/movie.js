// import { ref, computed } from "vue";
// import { defineStore } from "pinia";
// import axios from "axios";
// import router from "@/router";

// export const useMovieStore = defineStore("movie", () => {

//   // state
//   const videos = ref([]);
//   const recommendMovies = ref([])
//   const movieDetail = ref([])
//   const searchResults = ref([])
//   const selectedMovie = ref(null)
//   const isLoading = ref(false)


//   const API_KEY = import.meta.env.VITE_APP_YOUTUBE_API_KEY;
//   const TMDB_API_URL = 'https://api.themoviedb.org/3'
//   const TMDB_API_KEY = import.meta.env.VITE_TMDB_KEY  // v3 API 키 사용
//   const SPOTYFY_API_URL = import.meta.env.SPOTYFY_API_URL
  
  
//   // getters
//   const getVideos = computed(() => videos.value);
//   const hasResult = computed(() => searchResults.value.length > 0)
//   const currentMovie = computed(() => selectedMovie.value)


//   // actions

//   // 리뷰 검색
//   const searchReview = (keyword) => {
//     axios({
//       url: "https://www.googleapis.com/youtube/v3/search",
//       method: "GET",
//       params: {
//         part: "snippet",
//         q: keyword,
//         type: "video",
//         key: API_KEY,
//       },
//     })
//       .then((response) => {
//         videos.value = response.data.items;
//         console.log(videos.value);
//         router.push({ name: "ReviewSearchView" });
//       })
//       .catch((err) => {
//         console.log(err);
//       });
//   };
    
//   const fetchTopRatedMovies = () => {
//       axios({
//           method: 'get',
//           url: `${TMDB_API_URL}/movie/top_rated`,
//           params: {
//               api_key: TMDB_API_KEY,  // Bearer 토큰이 아닌 API 키 사용
//               language: 'ko-KR',
//               page: 1
//           }
//       })
//       .then(response => {
//           recommendMovies.value = response.data.results
//           // console.log(recommendMovies.value)
//       })
//       .catch(error => {
//           console.error('영화 데이터 로딩 실패:', error.response?.data || error)
//       })
//   }

//   const fetchMovieDetail = (movieId) => {
//       axios({
//           method: 'get',
//           url: `${TMDB_API_URL}/movie/${movieId}`,
//           params: {
//               api_key: TMDB_API_KEY,  
//               language: 'ko-KR',
//               page: 1
//           }
//       })
//       .then(response => {
//           movieDetail.value = response.data
//           console.log(movieDetail)
//       })
//       .catch(error => {
//           console.error('영화 세부정보 로딩 실패:', error.response?.data || error)
//       })
//   }

// //


//   // 검색기능
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
//     hasResult,
//     currentMovie,
//     searchReview,
//     recommendMovies,
//     fetchTopRatedMovies,
//     fetchMovieDetail,
//     handleSearch,
//     selectMovie,
//   }
// })


// export const usePlaylistStore = defineStore('playlist', () => {
//   const playlists = ref([])
//   const isLoading = ref(false)

//   const createPlaylist = (movie) => {
//     isLoading.value = true

//     // 백엔드에서 스포티파이 플레이리스트 생성 요청
//     axios({
//       url: '/api/playlists/create',
//       method: 'POST',
//       data: {
//         movie_id: movie.id,
//         movie_title: movie.title
//       }
//     })
//       .then((response) => {
//         playlists.value.push(response.data)
//       })
//       .catch((error) => {
//         console.error('플레이리스트 생성 중 오류:', error)
//       })
//       .finally(() => {
//         isLoading.value = false
//       })
//   }

//   const getUserPlaylists = () => {
//     isLoading.value = true

//     axios({
//       url: '/api/playlists/',
//       method: 'GET'
//     })
//       .then((response) => {
//         playlists.value = response.data
//       })
//       .catch((error) => {
//         console.error('플레이리스트 목록 조회 중 오류:', error)
//       })
//       .finally(() => {
//         isLoading.value = false
//       })
//   }

//   return {
//     playlists,
//     isLoading,
//     createPlaylist,
//     getUserPlaylists
//   }
// })

// stores/store.js
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useMovieStore = defineStore('movie', () => {
  const searchResults = ref([])
  const selectedMovie = ref(null)
  const isLoading = ref(false)

  const handleSearch = (query) => {
    if (query.length < 2) {
      searchResults.value = []
      return
    }

    isLoading.value = true
    
    // 테스트용 임시 데이터
    setTimeout(() => {
      searchResults.value = [
        {
          id: 1,
          title: '라라랜드',
          director: '데이미언 셔젤',
          releaseYear: 2016
        },
        {
          id: 2,
          title: '위플래쉬',
          director: '데이미언 셔젤',
          releaseYear: 2014
        },
        {
          id: 3,
          title: '인셉션',
          director: '크리스토퍼 놀란',
          releaseYear: 2010
        }
      ].filter(movie => 
        movie.title.toLowerCase().includes(query.toLowerCase()) ||
        movie.director.toLowerCase().includes(query.toLowerCase())
      )
      isLoading.value = false
    }, 500) // 실제 API 호출처럼 약간의 딜레이 추가
  }

  const selectMovie = (movie) => {
    selectedMovie.value = movie
    searchResults.value = []
  }

  return {
    searchResults,
    selectedMovie,
    isLoading,
    handleSearch,
    selectMovie
  }
})

export const usePlaylistStore = defineStore('playlist', () => {
  const playlists = ref([])
  const isLoading = ref(false)

  // 테스트용 임시 데이터
  let mockPlaylistId = 1

  const createPlaylist = (movie) => {
    isLoading.value = true

    // 임시 플레이리스트 생성 로직
    setTimeout(() => {
      const newPlaylist = {
        id: mockPlaylistId++,
        movie_id: movie.id,
        movie_title: movie.title,
        spotify_url: `https://open.spotify.com/playlist/mock${movie.id}`,
        created_at: new Date().toISOString()
      }

      playlists.value.push(newPlaylist)
      isLoading.value = false
    }, 1000)
  }

  const getUserPlaylists = () => {
    isLoading.value = true

    // 임시 데이터 로드
    setTimeout(() => {
      playlists.value = [
        {
          id: 1,
          movie_id: 1,
          movie_title: '라라랜드',
          spotify_url: 'https://open.spotify.com/playlist/mock1',
          created_at: '2024-03-19T10:00:00Z'
        }
      ]
      isLoading.value = false
    }, 500)
  }

  return {
    playlists,
    isLoading,
    createPlaylist,
    getUserPlaylists
  }
})