<template>
    <nav class="navbar fixed-top navbar-expand-lg" style="background: rgba(255, 255, 255, 0.8); background: linear-gradient(to bottom, rgba(255, 255, 255, 1) 0%, rgba(255, 255, 255, 0) 100%);">
        <div class="container-fluid">
            <!-- 로고 -->
            <RouterLink class="navbar-brand" :to="{ name: 'home' }">Filmody</RouterLink>
    
            <!-- 중앙 정렬할 부분 -->
                <div class="nav-center">
                    <ul class="navbar-nav d-flex">
                        <li class="nav-item dropdown" @click="toggleDropdown">
                            <a 
                                class="nav-link dropdown-toggle" 
                                href="#" 
                                role="button" 
                                :aria-expanded="isDropdownOpen.toString()"
                            >
                                Library
                            </a>
                            <ul class="dropdown-menu" :class="{ show: isDropdownOpen }">
                                <li>
                                    <RouterLink class="dropdown-item" to="/library/books">My Playlist</RouterLink>
                                </li>
                                <li>
                                    <RouterLink class="dropdown-item" to="/library/movies">Liked Movies</RouterLink>
                                </li>
                            </ul>
                            </li>

                        <li class="nav-item">
                            <RouterLink 
                                class="nav-link" 
                                :class="{ active: $route.path === '/playlist' }"
                                to="/playlist"
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
                </div>
    
            <!-- 오른쪽 버튼 그룹 -->
            <div class="nav-right d-flex align-items-center">
                <RouterLink
                    class="search-btn mx-3"
                    :class="{ active: $route.path === '/MovieSearchView' }"
                    to="/movies/search"
                >
                    <i class="fa-solid fa-magnifying-glass" style="color: #374c72;"></i>
                </RouterLink>
                
                <RouterLink 
                    v-if="!store.token"
                    :to="{ name: 'signup' }"
                    class="router-link mx-3"
                >
                    SignUp
                </RouterLink> 
    
                <RouterLink 
                    v-if="!store.token"
                    to="/login"
                    class="router-link mx-3"
                >
                    Login
                </RouterLink>
    
                <RouterLink 
                    v-if="store.token"
                    :to="{ path: '/profile/' + username }"
                    class="router-link mx-3"
                >
                    Profile
                </RouterLink>
                <RouterLink
                    v-if="store.token"
                    @click="logOut"
                    to="/"
                    class="router-link mx-3"
                >
                    Logout
                </RouterLink>
            </div>
        </div>
    </nav>
    </template>
    
    <script setup>
    import { ref, onMounted } from 'vue';
    import { useAuthStore } from '@/stores/auth';
    
    const store = useAuthStore();
    const isDropdownOpen = ref(false);

    // 로그아웃 함수
    const logOut = () => {
        store.logOut();
    };
    
    // 드롭다운 상태핸들러
    const toggleDropdown = () => {
    isDropdownOpen.value = !isDropdownOpen.value;
    };

    // Bootstrap 드롭다운 초기화
    onMounted(() => {
      const dropdownElements = document.querySelectorAll('.dropdown-toggle');
      dropdownElements.forEach((el) => {
        new bootstrap.Dropdown(el);
      });
    });
    </script>
    
    <style>
    /* 공통 스타일 */
    .router-link {
        text-decoration: none; /* 밑줄 제거 */
        color: inherit; /* 기본 텍스트 색상으로 설정 */
    }
    
    /* 전체 레이아웃을 위한 Flexbox 설정 */
    .container-fluid {
        display: flex;
        align-items: center;
        justify-content: space-between; /* 로고와 오른쪽 버튼을 양쪽으로 정렬 */
        position: relative; /* nav-center를 중앙 배치하기 위해 설정 */
    }
    
    /* nav-center 중앙 배치 */
    .nav-center {
        position: absolute;
        left: 50%; /* 부모 기준으로 수평 중앙 */
        transform: translateX(-50%); /* 정확히 중앙 정렬 */
        display: flex;
        justify-content: center; /* 자식 요소 가로 중앙 정렬 */
        align-items: center; /* 자식 요소 세로 중앙 정렬 */
    }
    
    /* 각 nav-item 간 간격 */
    .nav-item {
        margin: 0 50px; /* 각 항목 사이의 간격 */
    }
    
    /* 로고와 오른쪽 요소의 스타일 */
    .navbar-brand {
        font-weight: bold;
        font-size: 1.5rem;
    }
    
    .nav-right {
        display: flex;
        align-items: center;
    }

    /* 드롭다운 메뉴 스타일 */
    .dropdown-menu {
        display: none; /* Bootstrap가 JS로 토글 */
        background-color: white;
        top: 100%; /* 부모의 아래에 표시 */
        border-radius: 4px;
        border: 1px solid #e6e3e3;
        min-width: 150px;
        z-index: 1000;
    }

    /* 드롭다운 항목 간격 및 스타일 */
    .dropdown-item {
        padding: 10px 15px;
        color: #000;
        text-decoration: none;
    }

    .dropdown.show .dropdown-menu {
        display: block; /* 활성화된 드롭다운 */
        }

    .dropdown-item:hover {
        background-color: #f8f9fa;
        color: #007bff;
    }
    </style>
    
