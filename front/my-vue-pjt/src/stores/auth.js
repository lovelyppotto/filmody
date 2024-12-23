import { ref, computed } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import router from "@/router";

export const useAuthStore = defineStore("auth", () => {
  const BASE_URL = 'http://127.0.0.1:8000';
  const token = ref(null);
  const currentUser = ref(null);
  const userData = ref(null);
  const userProfile = ref(null);
  const userPlaylists = ref([]);
  const userLikedPlaylists = ref([]);
  const userLikedMovies = ref([]);
  const isAuthenticated = computed(() => !!token.value);
  const userId = computed(() => currentUser.value?.id);

  // 회원가입
  const signUp = function (payload) {
    const { username, password1, password2, email, nickname } = payload;

    if (password1 !== password2) {
      alert('비밀번호가 일치하지 않습니다.');
      return;
    }

    axios({
      method: 'post',
      url: `${BASE_URL}/accounts/signup/`,
      data: { username, password1, password2, email, nickname }
    })
      .then((res) => {
        // 회원가입 성공 후 로그인
        const password = password1;
        logIn({ username, password });
      })
      .catch((err) => {
        console.log(err.response?.data);
      });
  };

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
    currentUser.value = userResponse.data;
    userData.value = userResponse.data;  // show_reviews를 포함한 전체 사용자 데이터 저장
    console.log('User data loaded:', userData.value); // 데이터 확인용
    router.push({ name: 'home' });
  } catch (err) {
    console.log(err);
  }
};
  // 로그아웃
  const logOut = function () {
    axios({
      method: 'post',
      url: `${BASE_URL}/accounts/logout/`,
    })
      .then(() => {
        token.value = null;

        // router.push('/');

        currentUser.value = null;  
        userData.value = null;     
        userProfile.value = null;  
        userPlaylists.value = [];  
        userLikedPlaylists.value = [];
        userLikedMovies.value = [];
        router.push({ name: 'home' });
      
      })
      .catch((err) => {
        console.log(err);
      });
  };

  // 유저 프로필 상세페이지
  const fetchUserProfile = async (userId) => {
    try {
      const response = await axios.get(`${BASE_URL}/accounts/users/${userId}/`, {
        headers: { Authorization: `Token ${token.value}` }
      });
      userProfile.value = response.data.user_info;
      userPlaylists.value = response.data.playlists;
      userLikedPlaylists.value = response.data.liked_playlists;
      userLikedMovies.value = response.data.liked_movies;
    } catch (error) {
      console.error('프로필 로드 실패 : ', error);
    }
  };
  
  // 현재 로그인한 사용자 정보
const fetchCurrentUser = async () => {
  if (!token.value) {
    console.log('No token available');
    return null;
  }
  try {
    console.log('Fetching current user with token:', token.value);
    const res = await axios.get(`${BASE_URL}/accounts/user/`, {
      headers: { Authorization: `Token ${token.value}` }
    });
    console.log('Current user data:', res.data);
    currentUser.value = res.data;
    userData.value = res.data;  // show_reviews를 포함한 전체 사용자 데이터 저장
    return res.data;
  } catch (err) {
    console.error('Error fetching current user:', err);
    return null;
  }
};

  // 팔로우, 언팔로우 토글
  const toggleFollow = async (userId) => {
    try {
      const response = await axios({
        method: 'post',
        url: `${BASE_URL}/accounts/users/${userId}/follow/`,
        headers: { Authorization: `Token ${token.value}` }
      });

      await fetchUserProfile(userId);
      return response.data;
    } catch (error) {
      console.error('팔로우 토글 실패:', error);
    }
  };

  // 팔로워 목록 가져오기
  const fetchFollowers = async (userId) => {
    try {
      const response = await axios({
        method: 'get',
        url: `${BASE_URL}/accounts/users/${userId}/followers/`,
        headers: { Authorization: `Token ${token.value}` }
      });
      return response.data;
    } catch (error) {
      console.error(error);
    }
  };

  // 팔로잉 목록 가져오기
  const fetchFollowing = async (userId) => {
    try {
      const response = await axios({
        method: 'get',
        url: `${BASE_URL}/accounts/users/${userId}/following/`,
        headers: { Authorization: `Token ${token.value}` }
      });
      return response.data;
    } catch (error) {
      console.error(error);
    }
  };

  return {
    token,
    userData,
    logIn,
    logOut,
    BASE_URL,
    signUp,
    fetchCurrentUser,
    userProfile,
    userPlaylists,
    userLikedPlaylists,
    userLikedMovies,
    fetchUserProfile,
    toggleFollow,
    fetchFollowers,
    fetchFollowing,
    currentUser, 
    isAuthenticated, 
    userId
  };
}, { persist: true });