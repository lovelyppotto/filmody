<template>
    <nav class="navbar fixed-top navbar-expand-lg">
      <div class="container-fluid px-4">
        <!-- Logo -->
        <RouterLink class="navbar-brand" :to="{ name: 'home' }">Filmody</RouterLink>
  
        <!-- Mobile Toggle Button -->
        <button
          class="navbar-toggler"
          type="button"
          @click="toggleMobileMenu"
          aria-controls="navbarContent"
          :aria-expanded="isMobileMenuOpen"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
  
        <!-- Center Menu -->
        <div class="nav-center">
          <ul class="navbar-nav">
            <li class="nav-item dropdown">
              <a
                class="nav-link dropdown-toggle"
                href="#"
                role="button"
                @click="toggleDropdown"
                :aria-expanded="isDropdownOpen.toString()"
              >
                Library
              </a>
              <ul 
                class="dropdown-menu" 
                :class="{ 'show': isDropdownOpen }"
                @click="closeDropdown"
              >
                <li>
                  <RouterLink class="dropdown-item" :to="{ name: 'my-playlists' }">My Playlist</RouterLink>
                </li>
                <li>
                  <RouterLink class="dropdown-item" :to="{ name: 'liked-playlists' }">Liked Playlist</RouterLink>
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
  
        <!-- Right Menu -->
        <div class="nav-right">
          <RouterLink
            class="search-btn mx-3"
            :class="{ active: $route.path === '/MovieSearchView' }"
            to="/movies/search"
          >
            <i class="fa-solid fa-magnifying-glass" style="color: #374c72;"></i>
          </RouterLink>
          
          <template v-if="!store.token">
            <RouterLink :to="{ name: 'signup' }" class="router-link mx-3">
              SignUp
            </RouterLink>
            <RouterLink to="/login" class="router-link mx-3">
              Login
            </RouterLink>
          </template>
          <template v-else>
            <RouterLink :to="{ path: '/profile/' + username }" class="router-link mx-3">
              Profile
            </RouterLink>
            <RouterLink @click="logOut" to="/" class="router-link mx-3">
              Logout
            </RouterLink>
          </template>
        </div>
      </div>
    </nav>
  </template>
  
  <script setup>
   import { ref, onMounted, onUnmounted } from 'vue';
import { useAuthStore } from '@/stores/auth';

const store = useAuthStore();
const isDropdownOpen = ref(false);
const isMobileMenuOpen = ref(false);

const logOut = () => {
  store.logOut();
};

const toggleDropdown = (event) => {
  event.preventDefault();
  event.stopPropagation(); // 이벤트 전파 방지
  isDropdownOpen.value = !isDropdownOpen.value;
};

const closeDropdown = () => {
  isDropdownOpen.value = false;
};

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value;
};

const handleClickOutside = (event) => {
  const dropdownElement = document.querySelector('.dropdown-menu');
  const dropdownToggle = document.querySelector('.dropdown-toggle');
  
  if (
    dropdownElement &&
    !dropdownElement.contains(event.target) && 
    dropdownToggle &&
    !dropdownToggle.contains(event.target)
  ) {
    isDropdownOpen.value = false;
  }
};

const handleResize = () => {
  if (window.innerWidth > 992) {
    isMobileMenuOpen.value = false;
    isDropdownOpen.value = false;
  }
};

onMounted(() => {
  window.addEventListener('resize', handleResize);
  document.addEventListener('click', handleClickOutside); // 외부 클릭 이벤트 리스너 추가
});

onUnmounted(() => {
  window.removeEventListener('resize', handleResize);
  document.removeEventListener('click', handleClickOutside); // 리스너 제거
});

  </script>
  
  <style scoped>
  .navbar {
  background: rgba(255, 255, 255, 0.9); /* 약간 투명한 배경 */
  background: linear-gradient(to bottom, rgba(255, 255, 255, 0.9) 0%, rgba(255, 255, 255, 0) 100%); /* 끝부분만 투명 */
  transition: all 0.3s ease;
  padding: 0.5rem 1rem;
  border-bottom: none; /* 경계선 제거 */
  box-shadow: none; /* 그림자 제거 */
}

/* 반응형 스타일 (모바일 뷰) */
@media (max-width: 992px) {
  .navbar {
    background: rgba(255, 255, 255, 1); /* 모바일에서는 조금 더 불투명한 배경 */
    background: linear-gradient(to bottom, rgba(255, 255, 255, 1) 0%, rgba(255, 255, 255, 0.5) 90%); /* 끝부분만 투명 효과 */
    box-shadow: none; /* 하단 경계선 및 그림자 제거 */
  }

  .navbar-collapse {
    background: rgba(255, 255, 255, 1); /* 메뉴 펼쳐졌을 때도 불투명한 배경 */
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 약간의 그림자로 분리감 */
    padding: 1rem;
    border-radius: 8px; /* 메뉴 모서리 둥글게 */
  }
}

  
  .navbar-brand {
    font-weight: bold;
    font-size: 1.5rem;
    color: #374c72;
  }
  
  .container-fluid {
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: relative;
  }
  
  .nav-center {
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1;
  }
  
  .nav-item {
    margin: 0 50px;
  }
  
  .nav-link {
    color: #374c72;
    font-weight: 500;
    transition: color 0.3s ease;
  }
  
  .nav-link:hover,
  .nav-link.active {
    color: #6e8ab5;
  }
  
  .nav-right {
    display: flex;
    align-items: center;
    margin-left: auto;
    z-index: 1;
  }
  
  .router-link {
    text-decoration: none;
    color: #374c72;
    transition: color 0.3s ease;
  }
  
  .router-link:hover {
    color: #6e8ab5;
  }
  
  .dropdown-menu {
    border: 1px solid #e6e3e3;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    min-width: 150px;
  }
  
  .dropdown-item {
    padding: 0.75rem 1.5rem;
    color: #374c72;
    transition: all 0.2s ease;
  }
  
  .dropdown-item:hover {
    background-color: #f8f9fa;
    color: #374c72;
  }
  
  /* 반응형 스타일 */
  @media (max-width: 992px) {
    .nav-center {
      position: static;
      transform: none;
      width: 100%;
      margin: 1rem 0;
      order: 1;
    }
  
    .navbar-nav {
      width: 100%;
      text-align: center;
    }
  
    .nav-item {
      margin: 0.5rem 0;
    }
  
    .nav-right {
      display: flex;
      justify-content: center;
      width: 100%;
      margin-top: 1rem;
      order: 2;
    }
  
    .dropdown-menu {
      position: static !important;
      width: 100%;
      text-align: center;
      box-shadow: none;
      margin-top: 0;
    }
  
    .navbar-collapse {
      position: absolute;
      top: 100%;
      left: 0;
      right: 0;
      background-color: white;
      padding: 1rem;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
  
    .container-fluid {
      flex-wrap: wrap;
    }
  }
  
  .navbar-toggler {
    border: none;
    padding: 0.5rem;
    margin-left: auto;
  }
  
  .navbar-toggler:focus {
    box-shadow: none;
  }
  </style>