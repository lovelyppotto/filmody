import { ref, computed } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import router from "@/router";

export const useAuthStore = defineStore("auth", () => {
  const BASE_URL = 'http://127.0.0.1:8000'
  const token = ref(null)

    // 회원가입
    const signUp = function (payload) {
      const { username, password1, password2, email, nickname } = payload
      console.log(payload)
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
          console.log(err.response.data)
        })
    }

    // 로그인
    const logIn = function (payload) {
      const { username, password } = payload;
      axios({
        method: 'post',
        url: `${BASE_URL}/accounts/login/`,
        data: { username, password }
      })
      .then((res) => {
        token.value = res.data.key;
        console.log("로그인 후 받은 토큰:", token.value); // 토큰 확인
        router.push({ name: 'home' });
      })
      .catch((err) => {
        console.log(err);
      });
    };

    // 로그아웃
    const logOut = function () {
      axios({
        method:'post',
        url:`${BASE_URL}/accounts/logout/`,
      })
      .then((res) => {
        token.value=null
        router.push({name : 'HomeView'})
      })
      .catch((err) => {
        console.log(err);
      })
    }
    return {
      token,
      logIn,
      logOut,
      BASE_URL,
      signUp,
    };
  }, { persist: true });