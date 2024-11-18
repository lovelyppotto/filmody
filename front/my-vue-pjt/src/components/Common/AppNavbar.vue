<template>
    <nav class="navbar fixed-top navbar-expand-lg bg-body-tertiary">
        <div class="container-fluid">
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarTogglerDemo01" aria-controls="navbarTogglerDemo01" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarTogglerDemo01">
                <a class="navbar-brand" href="#">Movie Site</a>
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                        <RouterLink 
                            class="nav-link" 
                            :class="{ active: $route.path === '/' }"
                            to="/"
                        >
                            Home
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
        <form class="d-flex" role="search">
          <input class="form-control me-2" type="search" placeholder="제목을 입력하세요" aria-label="Search" v-model.trim="keyword" @keyup.enter="search" />
          <button class="btn btn-outline-success" type="submit" @click.prevent="searchReview()">Search</button>
        </form>
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
</script>
