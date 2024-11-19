import { ref, computed } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import router from "@/router";

export const useMovieStore = defineStore("movie", () => {
  const BASE_URL = 'http://127.0.0.1:8000'
  const token = ref(null)
  const videos = ref([]);
  const recommendMovies = ref([])
  const movieDetail = ref([])
  const getVideos = computed(() => videos.value);
  const API_KEY = import.meta.env.VITE_APP_YOUTUBE_API_KEY;
  const TMDB_API_URL = 'https://api.themoviedb.org/3'
  const TMDB_API_KEY = import.meta.env.VITE_TMDB_KEY  // v3 API 키 사용

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
  return{
    token,
    logIn,
    logOut,
    BASE_URL,
    signUp,
    videos,
    getVideos,
    movieDetail,
    searchReview,
    recommendMovies,
  }
}, { persist: true });