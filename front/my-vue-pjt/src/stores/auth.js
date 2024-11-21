import { ref, computed } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import router from "@/router";

export const useAuthStore = defineStore("auth", () => {
  const BASE_URL = 'http://127.0.0.1:8000'
  const token = ref(null)
  const currentUser = ref(null)
  const userData = ref(null)

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
    const logIn = async function (payload) {
      try {
        const { username, password } = payload;
        const response = await axios.post(`${BASE_URL}/accounts/login/`, { username, password });
        token.value = response.data.key;
        
        // 사용자 정보 가져오기
        const userResponse = await axios.get(`${BASE_URL}/accounts/user/`, {
          headers: { Authorization: `Token ${token.value}` }
        });
        userData.value = userResponse.data;
        
        router.push({ name: 'home' });
      } catch (err) {
        console.log(err);
      }
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

    // 현재 로그인한 사용자 정보
    const fetchCurrentUser = async () => {
      if (!token.value) return null
      try {
        const res = await axios.get(`${BASE_URL}/accounts/user/`, {
          headers: { Authorization: `Token ${token.value}` }
        })
        currentUser.value = res.data
        return res.data
      } catch (err) {
        console.error(err)
        return null
      }
    }

    return {
      token,
      userData,
      logIn,
      logOut,
      BASE_URL,
      signUp,
      fetchCurrentUser,
    };
  }, { persist: true });