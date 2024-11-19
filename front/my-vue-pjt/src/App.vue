<template>
  <AppNavbar />
  <div class="content-wrapper">
    <RouterLink :to="{name: 'SignUpView'}">SignUpView</RouterLink> |
    <RouterLink :to="{name: 'LogInView'}">LogInView</RouterLink> 
    <RouterView />
  </div>
</template>

<script setup>
import AppNavbar from "@/components/Common/AppNavbar.vue";
import { RouterView, RouterLink } from 'vue-router'
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
