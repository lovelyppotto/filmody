<template>
  <nav class="navbar fixed-top navbar-expand-lg">
    <div class="container-fluid px-4">
      <!-- Logo -->
      <RouterLink class="navbar-brand" :to="{ name: 'home' }" @click="handleMenuClick">Filmody</RouterLink>

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
      
      <!-- Collapsible Content -->
      <div 
        class="collapse navbar-collapse"
        :class="{ 'show': isMobileMenuOpen }"
        id="navbarContent"
      >
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
                style="background: none !important; background-color: transparent !important;"
                :class="{ 'show': isDropdownOpen }"
                @click="closeDropdown"
              >
                <li>
                  <RouterLink class="dropdown-item" :to="{ name: 'my-playlists' }" @click="handleMenuClick">My Playlist</RouterLink>                </li>
                <li>
                  <RouterLink class="dropdown-item" :to="{ name: 'liked-playlists' }" @click="handleMenuClick">Liked Playlist</RouterLink>
                </li>
                <li>
                  <RouterLink class="dropdown-item" :to=" {name:'LikedMovies'}" @click="handleMenuClick">Liked Movies</RouterLink>
                </li>
              </ul>
            </li>
            <li class="nav-item">
              <RouterLink
                class="nav-link"
                :class="{ active: $route.path === '/playlist' }"
                @click="handleMenuClick"
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
                @click="handleMenuClick"
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
            @click="handleMenuClick"
          >
            <i class="fa-solid fa-magnifying-glass" style="color: #374c72;"></i>
          </RouterLink>
          
          <template v-if="!store.token">
            <RouterLink :to="{ name: 'signup' }" class="router-link mx-3" @click="handleMenuClick">
              SignUp
            </RouterLink>
            <RouterLink to="/login" class="router-link mx-3" @click="handleMenuClick">
              Login
            </RouterLink>
          </template>
          <template v-else>
            <RouterLink :to="'/users/' + id" class="router-link mx-3" @click="handleMenuClick">
              Profile
            </RouterLink>
            <RouterLink to="/" class="router-link mx-3" @click="logOut">
              Logout
            </RouterLink>
          </template>
        </div>
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
  
  // 모바일 메뉴와 드롭다운을 모두 닫는 함수
  const closeMobileMenu = () => {
    isMobileMenuOpen.value = false;
    isDropdownOpen.value = false;
  };

  const logOut = () => {
    store.logOut();
    closeMobileMenu(); // 로그아웃 시 메뉴 닫기
  };
    
  const toggleDropdown = (event) => {
    event.preventDefault();
    event.stopPropagation();
    isDropdownOpen.value = !isDropdownOpen.value;
  };

  const handleMenuClick = () => {
    isDropdownOpen.value = false;
    isMobileMenuOpen.value = false;
  };

  const closeDropdown = () => {
    isDropdownOpen.value = false;
  };

  const toggleMobileMenu = () => {
    isMobileMenuOpen.value = !isMobileMenuOpen.value;
  };
  
  // 외부 클릭 이벤트 핸들러 수정
  const handleClickOutside = (event) => {
    const dropdownElement = document.querySelector('.dropdown-menu');
    const dropdownToggle = document.querySelector('.dropdown-toggle');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    const navbarToggler = document.querySelector('.navbar-toggler');
    
    // 드롭다운 메뉴 닫기
    if (
      dropdownElement &&
      !dropdownElement.contains(event.target) && 
      dropdownToggle &&
      !dropdownToggle.contains(event.target)
    ) {
      isDropdownOpen.value = false;
    }
  
    // 모바일 메뉴 닫기
    if (
      navbarCollapse &&
      !navbarCollapse.contains(event.target) &&
      !navbarToggler.contains(event.target) &&
      isMobileMenuOpen.value
    ) {
      isMobileMenuOpen.value = false;
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
    document.addEventListener('click', handleClickOutside);
  });
  
  onUnmounted(() => {
    window.removeEventListener('resize', handleResize);
    document.removeEventListener('click', handleClickOutside);
  });
  </script>
  
  <style scoped>
  .navbar {
  background: linear-gradient(to bottom, 
      rgba(255, 255, 255, 1) 0%,
      rgba(255, 255, 255, 0.7) 30%,
      rgba(255, 255, 255, 0.4) 70%,
      rgba(255, 255, 255, 0.0) 100%
    );
  transition: all 0.3s ease;
  padding: 0.5rem 1rem;
  border-bottom: none; /* 경계선 제거 */
  box-shadow: none; /* 그림자 제거 */
}

/* 반응형 스타일 (모바일 뷰) */


  
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
    color: #1d49b7;
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
    background-color: rgba(255, 255, 255, 0.472);
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    min-width: 150px;
  }
  
  .dropdown-item {
    padding: 0.75rem 1.5rem;
    color: #578df0;
    transition: all 0.2s ease;
  }
  
  .dropdown-item:hover {
    background-color: #f8f9fa;
    color: #374c72;
  }

  .navbar-collapse {
    flex-grow: 1;
    display: flex;
  }

  .navbar .nav-item .dropdown-menu,
.navbar .nav-item .dropdown-menu.show {
  /* background: none !important; */
  background-color: transparent !important;
  background-image: linear-gradient(to bottom,
    rgba(255, 255, 255, 0.98) 0%,
    rgba(255, 255, 255, 0.95) 40%,
    rgba(255, 255, 255, 0.90) 70%,
    rgba(255, 255, 255, 0.85) 100%
  ) !important;
  border: none !important;
  box-shadow: none !important;
  backdrop-filter: blur(8px);
}

/* 드롭다운 아이템 스타일도 추가 */
.navbar .nav-item .dropdown-menu .dropdown-item {
  background: transparent !important;
}

.navbar .nav-item .dropdown-menu .dropdown-item:hover,
.navbar .nav-item .dropdown-menu .dropdown-item:focus {
  background: rgba(255, 255, 255, 0.314) !important;
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
      margin: 2rem 0 2rem 0; /* 위 1rem, 아래 2rem으로 여백 설정 */
    }
  
    .dropdown-menu {
      position: static !important;
      width: 100%;
      text-align: center;
      box-shadow: none;
      margin-top: 0;
    }
  
  
    .container-fluid {
      flex-wrap: wrap;
    }

    .navbar-collapse {
    display: none;
    width: 100%;
  }

  .navbar-collapse.show {
    display: flex;
    flex-direction: column;
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    /* background: linear-gradient(to bottom, 
      rgba(255, 255, 255, 1) 0%,
      rgba(255, 255, 255, 0.9) 30%,
      rgba(255, 255, 255, 0.7) 70%,
      rgba(255, 255, 255, 0.3) 100%
    ); */
    padding: 1rem;
    backdrop-filter: blur(8px);  /* 배경 블러 효과 */
    box-shadow: 0 8px 12px -6px rgba(0, 0, 0, 0.1);  /* 부드러운 그림자 */
    border-bottom-left-radius: 20px;  /* 하단 모서리 둥글게 */
    border-bottom-right-radius: 20px;
  }

  /* 메뉴 항목들의 배경도 투명하게 처리 */
  .nav-center, .nav-right {
    background: transparent;
  }

  /* 드롭다운 메뉴의 배경도 반투명하게 */
  .navbar .nav-item .dropdown-menu,
  .navbar .nav-item .dropdown-menu.show {
    background-color: rgba(255, 255, 255, 0.934);
    border: none !important;
    box-shadow: none !important;
    backdrop-filter: blur(8px);
  }

  /* dropdown 아이템들의 스타일 */
  .navbar .nav-item .dropdown-menu .dropdown-item {
    background: transparent !important;
  }

  .navbar .nav-item .dropdown-menu .dropdown-item:hover,
  .navbar .nav-item .dropdown-menu .dropdown-item:focus {
    background: rgba(255, 255, 255, 0.3) !important;
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