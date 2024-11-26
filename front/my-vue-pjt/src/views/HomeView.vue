<template>
    <div class="home-container">
      <!-- Header Section -->
      <header class="header">
        <div class="header-background" :style="{ backgroundImage: `url(${cinemaImage})` }"></div>
        <div class="header-blur"></div>
        <div class="header-content">
          <h1 class="text-fade-in font-bold">Filmody,</h1>
          <h1 class="playlist-text">영화와 플레이리스트를 연결하다</h1>
          <button @click="redirectToPlaylist" 
                  class="filmody-btn hover-effect"
                  :class="{ 'button-pulse': showPulse }">
            Start to Filmody
          </button>
        </div>
      </header>
  
      <!-- Main Content Section -->
      <section class="main-section" ref="mainSection" :class="{ 'appear': isMainVisible }">
        <div class="main-content">
            <div class="accordion-gallery">
            <div v-for="(image, index) in images" 
                :key="index"
                class="accordion-item"
                :class="{ 'expanded': hoveredIndex === index }"
                @mouseenter="hoveredIndex = index"
                @mouseleave="hoveredIndex = null">
                <img :src="image.src" :alt="image.alt" class="accordion-image" />
            </div>
            </div>
            
            <div class="content-section ms-0" 
                :class="{ 'content-active': isContentActive }"
                @mouseenter="isContentActive = true"
                @mouseleave="isContentActive = false">
            <div class="text-content">
                <h2 class="animate-text mb-3 text-ibm font-bold">Make Playlist!</h2>
                <p class="animate-text-delay-1 ">좋아하는 영화의 OST가 있나요?</p>
                <p class="animate-text-delay-2 mb-0">나만의 플레이리스트를 쉽게 만들어 보세요!</p>
            </div>
            </div>
        </div>
        </section>
  
      <!-- Share Section -->
    <section class="share-section-container" ref="shareSection" :class="{ 'appear': isShareVisible }">
    <div class="bottom-section">
        <div class="share-section" @click="handleShareClick">
            <h3 class="share-text mb-3 text-ibm font-bold">Share Playlist!</h3>
            <p class="share-description">만든 플레이리스트를 공유하세요,</p>
            <p class="mb-0">그리고 소통하세요!</p>
        </div>
        <div class="preview-section">
        <div class="gradient-overlay"></div>
        <video 
            class="preview-video" 
            autoplay 
            loop 
            muted 
            playsinline
            :class="{ 'video-loaded': isVideoLoaded }"
            @loadeddata="handleVideoLoaded"
        >
            <source :src="videoPath" type="video/mp4">
            Your browser does not support the video tag.
        </video>
        </div>
    </div>
    </section>

      <!-- Community Section -->
      <section class="community-section" ref="communitySection" :class="{ 'appear': isCommunityVisible }">
    <div class="community-content">
      <div class="community-text">
        <h2 class="animate-text text-3xl font-bold mb-4">Find fun at Filmody!</h2>
        <p class="animate-text-delay-1 text-lg text-gray-600">감상할 영화를 찾고,</p>
        <p class="animate-text-delay-2 text-lg text-gray-600">나만의 음악 취향까지 Filmody에서 공유해보세요</p>
      </div>
      <div class="community-features">
        <div v-for="(feature, index) in features" 
             :key="index"
             class="feature-card"
             :style="{ animationDelay: `${index * 0.2}s` }"
             :class="{ 'card-appear': isCommunityVisible }">
          <div class="feature-icon">
            <i :class="feature.icon"></i>
          </div>
          <h3 class="text-xl font-semibold">{{ feature.title }}</h3>
          <p>{{ feature.description }}</p>
        </div>
      </div>
    </div>
  </section>
  
      <footer class="footer">
        <p class="mb-0">© 2024 Filmody</p>
      </footer>
    </div>
</template>
  
<script setup>
import { ref, onMounted, computed } from 'vue'
import cinemaImage from '@/assets/cinema.jpg?url' 
import router from '@/router';

const mainImage = ref('https://blog.kakaocdn.net/dn/bmIwxA/btrVE1Ql6YL/kfImMiXEd19Kch9ziopPj0/img.jpg')
const isContentActive = ref(false)
const showPulse = ref(false)
const showShareIndicator = ref(false)

// 비디오 관련 상태
const videoPath = ref('/lp.mp4') // public 폴더에 있는 비디오 경로
const isVideoLoaded = ref(false)

// 스크롤 애니메이션 관련 상태
const mainSection = ref(null)
const shareSection = ref(null)
const communitySection = ref(null)
const isMainVisible = ref(false)
const isShareVisible = ref(false)
const isCommunityVisible = ref(false)
const hoveredIndex = ref(null)

const headerStyle = {
  backgroundImage: `url(${cinemaImage})`,
  backgroundSize: 'cover',
  backgroundPosition: 'center'
}

const images = [
  {
    src: 'https://muko.kr/files/attach/images/2024/10/15/8ecf41e1702aee730124da952c0c4186.jpeg',
    alt: 'Movie Poster 1'
  },
  {
    src: 'https://img.sbs.co.kr/newsnet/etv/upload/2024/07/25/30000939794_1280.jpg',
    alt: 'Movie Poster 2'
  },
  {
    src: 'https://cinelab.co.kr/upload/1672747058961_common%20(9).jpg',
    alt: 'Movie Poster 3'
  }
]

const redirectToPlaylist = () => {
  router.push({ name: 'PlaylistView' })  // 로그인 라우트 이름을 사용
}

const handleVideoLoaded = () => {
  isVideoLoaded.value = true
}

// Feature cards data
const features = [
  {
    title: 'Discover',
    description: '새로운 플레이리스트의 발견',
    icon: 'fas fa-compass'  // 탐색/발견 아이콘
  },
  {
    title: 'Share',
    description: '나만의 특별한 플레이리스트 공유',
    icon: 'fas fa-share-alt'  // 공유 아이콘
  },
  {
    title: 'Connect',
    description: '음악 취향이 비슷한 친구 만들기',
    icon: 'fas fa-users'  // 커뮤니티 아이콘
  }
]

onMounted(() => {
  // Button pulse animation
  setInterval(() => {
    showPulse.value = true
    setTimeout(() => {
      showPulse.value = false
    }, 2000)
  }, 5000)

  // Intersection Observer setup
  const options = {
    threshold: 0.3  // 30% of the element is visible
  }

  const observerCallback = (entries, observer) => {
    entries.forEach(entry => {
      if (entry.target === mainSection.value) {
        isMainVisible.value = entry.isIntersecting
      } else if (entry.target === shareSection.value) {
        isShareVisible.value = entry.isIntersecting
      } else if (entry.target === communitySection.value) {
        isCommunityVisible.value = entry.isIntersecting
      }
    })
  }

  const observer = new IntersectionObserver(observerCallback, options)

  // Observe each section
  if (mainSection.value) observer.observe(mainSection.value)
  if (shareSection.value) observer.observe(shareSection.value)
  if (communitySection.value) observer.observe(communitySection.value)
})

const handleImageHover = () => {
  // Add any hover effects or animations
}

const handleShareClick = () => {
  showShareIndicator.value = true
  setTimeout(() => {
    showShareIndicator.value = false
  }, 2000)
}

const navigateToFilmoly = () => {
  // Add navigation logic here
  console.log('Navigating to Filmoly...')
}
</script>
  
<style scoped>

.home-container {
  width: 100%;
  min-height: 100vh;
  background-color: white;
}

.header {
  position: relative;
  padding: 24px;
  border-bottom: 1px solid #eee;
  overflow: hidden;
  min-height: 600px; /* 이미 수정됨 */
}

.header-content {
  position: relative;
  max-width: 1200px;
  height: 600px; /* 여기를 헤더 높이와 동일하게 수정 */
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  z-index: 3;
}

.header-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-size: cover;
  background-position: center;
  z-index: 1;
}

.header-blur {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  backdrop-filter: blur(4px);
  background: rgba(255, 255, 255, 0.2);
  z-index: 2;
}


.text-fade-in,
.playlist-text {
  color: #ffffff;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  margin: 0;
  font-family: var(--font-nunito);
}

.playlist-text {
  font-size: 1.5em;
  margin: 8px 0 16px 0;
  font-family: var(--font-ibm);
}

.filmody-btn {
  padding: 8px 24px;
  border: 1px solid #ddd;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.9);
  transition: all 0.3s ease;
  cursor: pointer;
  margin-top: 24px;
}

.hover-effect:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.button-pulse {
  animation: pulse 2s infinite;
}

.main-section {
  background-color: #f5f5f5;
  padding: 40px 0;
}

.main-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 32px;
  padding: 32px;
  max-width: 1200px;
  margin: 0 auto;
}

.main-image {
  width: 100%;
  height: 400px;
  object-fit: cover;
  border-radius: 12px;
  transition: transform 0.3s ease;
}

.hover-zoom:hover .main-image {
  transform: scale(1.02);
}

.content-section {
  padding: 24px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  transition: all 0.3s ease;
}

.content-active {
  transform: translateX(10px);
}

.animate-text {
  opacity: 0;
  animation: slideIn 0.5s ease-out forwards;
}

.animate-text-delay-1 {
  opacity: 0;
  animation: slideIn 0.5s ease-out 0.2s forwards;
}

.animate-text-delay-2 {
  opacity: 0;
  animation: slideIn 0.5s ease-out 0.4s forwards;
}

.share-section-container {
  background-color: #ffffff;
}

.bottom-section {
  display: grid;
  grid-template-columns: 0.8fr 1.2fr;
  max-width: none; /* max-width 제거 */
  margin: 0; /* margin 제거 */
  height: 500px;
  position: relative; /* position 추가 */
}

/* share-section 수정 */
.share-section {
  padding: 24px 0 24px 24px;
  cursor: pointer;
  position: relative;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  justify-content: center;
  max-width: 1200px; /* 최대 너비 설정 */
  margin: 0 auto; /* 중앙 정렬 */
  padding-right: 48px; /* 오른쪽 여백 추가 */
}



.preview-section {
  position: absolute; /* 절대 위치로 변경 */
  right: 0; /* 오른쪽에 붙임 */
  width: 50%; /* 너비 설정 */
  height: 100%;
  overflow: hidden;
  background-color: #000;
}


.share-text {
  font-size: 2em;
  margin-bottom: 16px;
}

.preview-image {
  width: 100%;
  height: 300px;
  object-fit: cover;
  border-radius: 12px;
}

.community-section {
  background-color: #f8f9fa;  /* 좀 더 밝은 배경색 */
  padding: 80px 0;  /* 여백 증가 */
}

.community-text {
  text-align: center;
  margin-bottom: 60px;  /* 여백 증가 */
}

.community-features {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 32px;  /* 간격 증가 */
  margin-top: 40px;
}

.community-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 32px;
}

.feature-card {
  background-color: white;
  padding: 32px;  /* 패딩 증가 */
  border-radius: 16px;  /* 모서리 더 둥글게 */
  text-align: center;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
}

.feature-card h3 {
  color: #1f2937;  /* 더 진한 제목 색상 */
  margin-bottom: 12px;
  font-weight: 600;
}

.feature-card p {
  color: #4b5563;  /* 더 진한 텍스트 색상 */
  line-height: 1.6;
}

.feature-icon {
  width: 64px;
  height: 64px;
  background-color: #f0f7ff;  /* 밝은 파란색 배경 */
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
}

.feature-icon i {
  font-size: 24px;
  color: #3b82f6;  /* 파란색 아이콘 */
}

.footer {
  padding: 24px;
  text-align: center;
  background-color: #333;
  color: white;
}

/* 스크롤 애니메이션 관련 스타일 추가 */
.main-section,
.share-section-container,
.community-section {
  opacity: 0;
  transform: translateY(30px);
  transition: all 1s ease-out;
}

.appear {
  opacity: 1;
  transform: translateY(0);
}

.feature-card {
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.5s ease-out;
}

.card-appear {
  opacity: 1;
  transform: translateY(0);
}

/* 섹션별 트랜지션 딜레이 */
.main-section {
  transition-delay: 0.2s;
}

.share-section-container {
  transition-delay: 0.3s;
}

.community-section {
  transition-delay: 0.4s;
}

/* 기존 스타일에 추가 */
.feature-card {
  animation: none; /* 기존 애니메이션 제거 */
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.5s ease-out, transform 0.3s ease;
}

.feature-card.card-appear {
  opacity: 1;
  transform: translateY(0);
}

.feature-card:hover {
  transform: translateY(-5px);
}


/* 영상 그라데이션 효과 */
.gradient-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 60%; /* 그라데이션 영역을 좀 더 넓게 */
  height: 100%;
  background: linear-gradient(to right, 
    rgba(255, 255, 255, 1) 0%,
    rgba(255, 255, 255, 0.9) 20%,
    rgba(255, 255, 255, 0.7) 40%,
    rgba(255, 255, 255, 0.4) 60%,
    rgba(255, 255, 255, 0) 100%
  );
  z-index: 2;
  pointer-events: none;
}


.preview-video {
  width: 100%;
  height: 100%; /* 컨테이너 높이에 맞춤 */
  object-fit: cover;
  opacity: 0;
  transition: opacity 0.5s ease;
}


.video-loaded {
  opacity: 1;
}

.accordion-gallery {
  display: flex;
  width: 700px;
  height: 600px;
  gap: 8px;
  position: relative;
  overflow: hidden;
}

.accordion-item {
  position: relative;
  flex: 1;
  overflow: hidden;
  transition: flex 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  min-width: 50px;
  cursor: pointer;
}

.accordion-item.expanded {
  flex: 4;
}

.accordion-image {
  height: 100%;
  width: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.accordion-item:hover .accordion-image {
  transform: scale(1.05);
}

/* 메인 콘텐츠 영역 조정 */
.main-content {
  gap: 48px;
  padding: 32px;
  align-items: center;
}


/* 모바일 대응 */
@media (max-width: 768px) {
  .main-section,
  .share-section-container,
  .community-section {
    transform: translateY(20px);
  }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
}

@media (max-width: 768px) {
    .header-content {
    height: 300px; /* 모바일에서는 높이 줄임 */
    padding: 20px;
  }
  
  .playlist-text {
    font-size: 1.2em;
  }
  .header::before {
    filter: blur(5px);  /* 모바일에서는 블러 효과 줄이기 */
  }

  .main-content,
  .bottom-section,
  .community-features {
    grid-template-columns: 1fr;
  }
  
  .content-section {
    text-align: center;
  }

  .main-image,
  .preview-image {
    height: 250px;
  }
  
  .feature-card {
    margin-bottom: 16px;
  }

  
  .bottom-section {
    grid-template-columns: 1fr;
    height: auto;
  }
  
  .preview-section {
    position: relative;
    width: 100%;
    height: 300px;
  }

  .share-section {
    padding: 24px;
    max-width: 100%;
  }
  
  .gradient-overlay {
    width: 100%;
    background: linear-gradient(to right,
      rgba(255, 255, 255, 1) 0%,
      rgba(255, 255, 255, 0.8) 40%,
      rgba(255, 255, 255, 0.4) 70%,
      rgba(255, 255, 255, 0) 100%
    );
  }
  .accordion-gallery {
    height: 300px;
  }

  .accordion-item {
    min-width: 40px;
  }

  .community-features {
    grid-template-columns: 1fr;
    gap: 24px;
    padding: 0 20px;
  }

  .feature-card {
    padding: 24px;
  }
}

</style>

