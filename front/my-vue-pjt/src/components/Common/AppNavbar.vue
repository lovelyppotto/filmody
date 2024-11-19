<template>
    <nav class="navbar fixed-top navbar-expand-lg bg-body-tertiary">
        <div class="container-fluid">
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarTogglerDemo01" aria-controls="navbarTogglerDemo01" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarTogglerDemo01">
                <RouterLink class="navbar-brand" :to="{name:'HomeView'}">Filmody</RouterLink>
                <!-- <a class="navbar-brand" href="#">Filmody</a> -->
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                        <RouterLink 
                            class="nav-link" 
                            :class="{ active: $route.path === '/' }"
                            to="/"
                        >
                            Library
                        </RouterLink>
                    </li>
                    <li class="nav-item">
                        <RouterLink 
                            class="nav-link" 
                            :class="{ active: $route.path === '/' }"
                            to="/"
                        >
                            Playlist
                        </RouterLink>
                    </li>
                    <li class="nav-item">
                        <RouterLink 
                            class="nav-link" 
                            :class="{ active: $route.path === '/recommend' }"
                            to="/recommend"
                        >
                            Recommend
                        </RouterLink>
                    </li>
                </ul>
                <div class="d-flex align-items-center">
                    <form class="d-flex me-2" role="search">
                        <input class="form-control me-2" type="search" placeholder="제목을 입력하세요" aria-label="Search" v-model.trim="keyword" @keyup.enter="search" />
                        <button class="btn btn-outline-success" type="submit" @click.prevent="searchReview()">Search</button>
                    </form>
                    <form @submit.prevent="logOut" class="d-flex">
                        <button class="btn btn-outline-danger" type="submit" v-if="store.token">Logout</button>
                    </form>
                </div>
            </div>
        </div>
    </nav>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { useMovieStore } from "@/stores/movie";
import { ref } from "vue";

const store = useMovieStore();
const keyword = ref(null);

const searchReview = () => {
  if (keyword.value === "") {
    alert("검색어를 입력하세요");
  }
  store.searchReview(keyword.value);
  keyword.value = "";
};

const logOut = () => {
  store.logOut();
};
</script>