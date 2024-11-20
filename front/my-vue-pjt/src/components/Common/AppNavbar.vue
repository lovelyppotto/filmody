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
                    <form @submit.prevent="logOut" class="d-flex">
                        <button class="btn btn-outline-danger" type="submit" v-if="store.token">Logout</button>
                    </form>
                </div>
            </div>
        </div>
    </nav>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth';
import { RouterLink } from 'vue-router'

const store = useAuthStore();


const logOut = () => {
  store.logOut();
};
</script>