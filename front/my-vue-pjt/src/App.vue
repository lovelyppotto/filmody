<template>
  <AppNavbar />
  <div class="content-wrapper">
    <RouterLink :to="{name: 'SignUpView'}">SignUpView</RouterLink> |
    <RouterLink :to="{name: 'LogInView'}">LogInView</RouterLink> |
    <RouterLink :to="{name: 'MovieSearchView'}">Search</RouterLink> |
    <div  v-if="store.token">
      <RouterLink :to="{path: '/profile/' + username}">ProfileView</RouterLink> |
    </div>
    <RouterView />
  </div>
</template>

<script setup>
import AppNavbar from "@/components/Common/AppNavbar.vue";
import { RouterView, RouterLink } from 'vue-router'
import { useMovieStore } from "./stores/movie";
import { onMounted } from "vue";
import axios from "axios";
const store = useMovieStore()

// 토큰이 있으면 로그인 상태 유지
onMounted(() => {
  const token = localStorage.getItem('token')
  if(token) {
    axios({
      method:'get',
      url:`${store.BASE_URL}/accounts/user/`,
      headers: {
        Authorization: `Token ${token}`
      }
    })
    .then(() => {
      store.token = token
    })
    .catch(() => {
      // 토큰이 만료됐거나 유효하지 않을 때
      localStorage.removeItem('token')
      store.token = null
    })
  }
})
</script>

<style scoped>
.content-wrapper {
  margin-top: 65px;
  /* 또는 */
  /* 필요한 경우 추가 스타일 */
  width: 100%;
  min-height: calc(100vh - 56px);
}
</style>
