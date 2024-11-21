<template>
  <div>
    <h1>LogIn Page</h1>
    <form @submit.prevent="logIn">
      <label for="username">아이디 : </label>
      <input type="text" id="username" v-model.trim="username"><br>

      <label for="password">비밀번호 : </label>
      <input type="password" id="password" v-model.trim="password"><br>

      <input type="submit" value="logIn">
    </form>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth';
import { ref } from 'vue'
import { useRouter } from 'vue-router';

const router = useRouter()

const username = ref(null)
const password = ref(null)

const store = useAuthStore()

const logIn = function () {
  const payload = {
    username: username.value,
    password: password.value
  };
  
  // 로그인 요청
  store.logIn(payload).then(() => {
    // 로그인 성공 후 HomeView로 이동
    router.push({ name: 'home' });
  }).catch((error) => {
    console.error('로그인 실패:', error);
    // 실패시 처리 로직 추가 가능
  });
};

</script>

<style scoped>

</style>