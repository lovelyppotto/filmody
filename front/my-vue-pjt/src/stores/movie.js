import { ref, computed } from "vue";
import { debounce } from "lodash"
import { defineStore } from "pinia";
import axios from "axios";
import router from "@/router";

export const useMovieStore = defineStore("movie", () => {
  const BASE_URL = 'http://127.0.0.1:8000'
  const token = ref(null)
  const videos = ref([]);

  // 검색결과
  const searchResults = ref([])
  const recommendMovies = ref([])
  const movieDetail = ref([])

  const isLoading = ref(false)
  const searchQuery = ref('')

  const getVideos = computed(() => videos.value);
  const API_KEY = import.meta.env.VITE_APP_YOUTUBE_API_KEY;
  // const TMDB_API_URL = 'https://api.themoviedb.org/3'
  // const TMDB_API_KEY = import.meta.env.VITE_TMDB_KEY  // v3 API 키 사용

    // 회원가입
    const signUp = function (payload) {
      const { username, password1, password2, email, nickname } = payload
      // 비밀번호, 비밀번호 확인이 일치하는지
      if (password1 != password2){
        alert('비밀번호가 일치하지 않습니다.')
        return
      }

      axios({
        method: 'post',
        url: `${BASE_URL}/accounts/signup/`,
        data: {
          username, password1, password2, email, nickname
        }
      })
        .then((res) => {
          // console.log(res)
          // console.log('회원가입 성공')
          const password = password1
          logIn({ username, password })
        })
        .catch((err) => {
          console.log(er.response.data)
        })
    }
    // 로그인
    const logIn = function (payload) {
      // const username = payload.username
      // const password1 = payload.password
      const { username, password } = payload
      axios({
        method: 'post',
        url: `${BASE_URL}/accounts/login/`,
        data: {
          username, password
        }
      })
        .then((res) => {
          token.value = res.data.key
          router.push({ name: 'HomeView' })
          // console.log(res.data)
          console.log('로그인 성공')
        })
        .catch((err) => {
          console.log(err)
        })
    }

    // 로그아웃
    const logOut = function () {
      axios({
        method:'post',
        url:`${BASE_URL}/accounts/logout/`,
      })
      .then((res) => {
        console.log(res.data);
        token.value=null
        router.push({name : 'HomeView'})
      })
      .catch((err) => {
        console.log(err);
      })
    }


  // 유튜브 검색
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
      })
  }

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
      console.log('API 응답 데이터:', response.data) // 데이터 구조 확인
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

  return{
    token,
    logIn,
    logOut,
    BASE_URL,
    searchResults,
    isLoading,
    searchQuery,
    signUp,
    videos,
    getVideos,
    movieDetail,
    searchReview,
    recommendMovies,
    searchMovies,
    clearSearchResults,

  }
}, { persist: true });