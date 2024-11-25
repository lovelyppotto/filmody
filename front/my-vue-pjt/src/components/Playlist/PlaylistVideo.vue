<template>
  <div class="playlist-videos">
    <!-- 로딩 상태 -->
    <div v-if="isLoading" class="text-center p-5">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <!-- 플레이리스트가 비어있을 때 -->
    <div v-else-if="!videos.length" class="text-center p-5">
      <h3 class="mb-3">플레이리스트가 비어있습니다</h3>
      <p class="text-muted">재생할 영상을 추가해주세요</p>
    </div>

    <!-- 플레이리스트에 영상이 있을 때 -->
    <template v-else>
      <div class="playlist-container">
        <!-- 메인 비디오 영역 -->
        <div class="main-video-section">
          <div id="videoCarousel" class="carousel slide" data-bs-interval="false">
            <div class="carousel-inner">
              <div 
                v-for="(video, index) in videos" 
                :key="video.video_id"
                :class="['carousel-item', { active: index === 0 }]"
              >
                <div class="main-video-card">
                  <div class="ratio ratio-16x9 position-relative">
                    <div :id="`youtube-player-${index}`"></div>
                    <div v-if="showPlayMessage && activeIndex === index" 
                      class="play-message">
                      {{ countdown }}초 후 재생됩니다...
                    </div>
                  </div>
                  <div class="video-info mt-3">
                    <h5 class="video-title mb-2">{{ decodeHtml(video.title) }}</h5>
                    <div class="d-flex justify-content-between align-items-center">
                      <small class="text-muted">{{ formatDate(video.published_at) }}</small>
                      <button 
                        v-if="playlist?.user === authStore.userData?.id"
                        class="btn btn-outline-danger btn-sm"
                        @click.stop="removeVideo(video)"
                        :disabled="isRemoving"
                      >
                        <span v-if="isRemoving" class="spinner-border spinner-border-sm me-1"></span>
                        삭제
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 횡스크롤 재생목록 -->
        <div class="playlist-scroll-section mt-4">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <h6 class="m-0"><i class="fa-solid fa-list me-1" style="color: #223a62;"></i>  재생목록 · {{ videos.length }}개 동영상</h6>
          </div>
          
          <div class="playlist-scroll" ref="playlistScroll">
            <div 
              v-for="(video, index) in videos" 
              :key="video.video_id"
              class="playlist-thumbnail"
              :class="{ 'active': index === activeIndex }"
              @click="goToSlide(index)"
            >
              <div class="thumbnail-container">
                <img 
                  :src="video.thumbnail_url" 
                  :alt="video.title"
                  class="thumbnail-img"
                >
                <!-- <span class="duration">{{ formatDuration(video.duration) }}</span> -->
                <div v-if="index === activeIndex" class="now-playing">
                  <span class="playing-indicator"></span>
                  재생 중
                </div>
              </div>
              <div class="thumbnail-title">{{ decodeHtml(video.title) }}</div>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { usePlaylistStore } from '@/stores/playlist';
import { useAuthStore } from '@/stores/auth';
import { Carousel } from 'bootstrap';
import { useDecodeHtml } from '@/composables/useDecodeHtml';

const { decodeHtml } = useDecodeHtml();
const authStore = useAuthStore();
const playlistStore = usePlaylistStore();

// 상태 관리
const videos = ref([]);
const isLoading = ref(true);
const isRemoving = ref(false);
const activeIndex = ref(0);
const showPlayMessage = ref(false);
const countdown = ref(5);
let countdownTimer = null;
let carousel = null;
const players = ref({});
const isAutoPlay = ref(false);

const props = defineProps({
  playlistId: {
    type: [String, Number],
    required: true
  },
  playlist: {
    type: Object,
    required: true
  }
});

// YouTube API 로드
const loadYouTubeAPI = () => {
  return new Promise((resolve) => {
    if (window.YT && window.YT.Player) {
      resolve(window.YT);
      return;
    }

    const tag = document.createElement('script');
    tag.src = 'https://www.youtube.com/iframe_api';
    const firstScriptTag = document.getElementsByTagName('script')[0];
    firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

    window.onYouTubeIframeAPIReady = () => {
      resolve(window.YT);
    };
  });
};

// 재생 딜레이 처리
const startPlaybackDelay = (player, isAutoplay = false) => {
  if (isAutoplay) {
    return Promise.resolve();
  }

  return new Promise((resolve) => {
    showPlayMessage.value = true;
    countdown.value = 5;

    if (countdownTimer) {
      clearInterval(countdownTimer);
    }

    countdownTimer = setInterval(() => {
      countdown.value--;
      if (countdown.value <= 0) {
        clearInterval(countdownTimer);
        showPlayMessage.value = false;
        resolve();
      }
    }, 1000);
  });
};

// 플레이어 초기화
const initializePlayers = () => {
  return loadYouTubeAPI().then(YT => {
    videos.value.forEach((video, index) => {
      players.value[index] = new YT.Player(`youtube-player-${index}`, {
        videoId: video.video_id,
        height: '100%',
        width: '100%',
        playerVars: {
          rel: 0,
          autoplay: 0,
        },
        events: {
          onReady: (event) => {
            event.target.setVolume(10);
            
            if (index === 0) {
              startPlaybackDelay(event.target)
                .then(() => event.target.playVideo());
            }
          },
          onStateChange: (event) => {
            if (event.data === YT.PlayerState.ENDED) {
              isAutoPlay.value = true;
              showPlayMessage.value = false;
              if (countdownTimer) {
                clearInterval(countdownTimer);
              }
              
              const nextIndex = (index + 1) % videos.value.length;
              carousel?.to(nextIndex);
              const nextPlayer = players.value[nextIndex];
              if (nextPlayer?.playVideo) {
                nextPlayer.playVideo();
              }
            }
          }
        }
      });
    });
  }).catch(error => {
    console.error('YouTube 플레이어 초기화 실패:', error);
  });
};

// 슬라이드 변경 핸들러
const handleSlideChange = (event) => {
  const newIndex = event.to;
  activeIndex.value = newIndex;

  if (!isAutoPlay.value) {
    Object.entries(players.value).forEach(([idx, player]) => {
      if (Number(idx) !== newIndex && player.stopVideo) {
        player.stopVideo();
      }
    });

    const currentPlayer = players.value[newIndex];
    if (currentPlayer?.playVideo) {
      startPlaybackDelay(currentPlayer)
        .then(() => currentPlayer.playVideo());
    }
  }

  isAutoPlay.value = false;

  // 현재 재생 중인 썸네일이 보이도록 스크롤
  const activeThumb = document.querySelector('.playlist-thumbnail.active');
  if (activeThumb) {
    activeThumb.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
  }
};

// 영상 이동
const goToSlide = (index) => {
  if (index === activeIndex.value) return;
  
  Object.entries(players.value).forEach(([idx, player]) => {
    if (Number(idx) !== index && player.stopVideo) {
      player.stopVideo();
    }
  });

  carousel?.to(index);
  activeIndex.value = index;

  const currentPlayer = players.value[index];
  if (currentPlayer?.playVideo) {
    startPlaybackDelay(currentPlayer)
      .then(() => currentPlayer.playVideo());
  }
};

// 포맷팅 함수들
const formatDate = (dateString) => {
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  }).format(date);
};

// 플레이리스트 영상 로드
const loadPlaylistVideos = () => {
  isLoading.value = true;
  return playlistStore.getPlaylistVideos(props.playlistId)
    .then(result => {
      videos.value = result;
    })
    .catch(error => {
      console.error('플레이리스트 영상을 불러오는데 실패했습니다:', error);
    })
    .finally(() => {
      isLoading.value = false;
    });
};

// 휠 이벤트 핸들러
const handleWheel = (event) => {
  const scrollContainer = event.currentTarget;
  
  if (scrollContainer.scrollWidth > scrollContainer.clientWidth) {
    event.preventDefault();
    scrollContainer.scrollLeft += event.deltaY;
  }
};

// 영상 삭제
const removeVideo = (video) => {
  isRemoving.value = true;
  playlistStore.removeVideoFromPlaylist(props.playlistId, video.video_id)
    .then(() => loadPlaylistVideos())
    .catch(error => {
      console.error('영상 삭제 실패:', error);
    })
    .finally(() => {
      isRemoving.value = false;
    });
};

// 컴포넌트 마운트
onMounted(() => {
  loadPlaylistVideos()
    .then(() => {
      if (videos.value.length > 0) {
        carousel = new Carousel('#videoCarousel', {
          interval: false
        });

        document.getElementById('videoCarousel')?.addEventListener('slid.bs.carousel', handleSlideChange);
        
        // 휠 이벤트 리스너 추가
        const scrollContainer = document.querySelector('.playlist-scroll');
        if (scrollContainer) {
          scrollContainer.addEventListener('wheel', handleWheel, { passive: false });
        }
        
        return initializePlayers();
      }
    });
});

// 컴포넌트 언마운트
onUnmounted(() => {
  Object.values(players.value).forEach(player => {
    if (player.destroy) {
      player.destroy();
    }
  });

  carousel?.dispose();
  document.getElementById('videoCarousel')?.removeEventListener('slid.bs.carousel', handleSlideChange);
  
  const scrollContainer = document.querySelector('.playlist-scroll');
  if (scrollContainer) {
    scrollContainer.removeEventListener('wheel', handleWheel);
  }

  if (countdownTimer) {
    clearInterval(countdownTimer);
  }
});
</script>

<style scoped>
.playlist-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem;
}

.main-video-card {
  background: white;
  /* border-radius: 0.5rem; */
  overflow: hidden;
}

.video-title {
  font-size: 1.1rem;
  line-height: 1.4;
  margin: 0;
}

.play-message {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  z-index: 10;
}

.playlist-scroll-section {
  background-color: #f8f9fa;
  padding: 1rem;
  border-radius: 0.5rem;
  position: relative; /* 상대 위치 설정 */
}

.playlist-scroll {
  display: flex;
  gap: 1rem;
  overflow-x: auto;
  padding: 0.5rem;
  scroll-behavior: smooth;
  -webkit-overflow-scrolling: touch;
  
  /* 스크롤 이벤트 기본 동작 */
  overflow: hidden;
  
  /* 호버 시에만 스크롤 가능하도록 설정 */
  &:hover {
    overflow-x: auto;
  }
  
  /* Firefox */
  scrollbar-width: thin;
  scrollbar-color: #888 #f1f1f1;
  
  /* 마우스 휠 이벤트 처리를 위한 높이 설정 */
  padding-bottom: 1rem; /* 스크롤바 공간 확보 */
}

/* Webkit 브라우저용 스크롤바 스타일 */
.playlist-scroll::-webkit-scrollbar {
  height: 6px;
  /* 기본적으로 숨김 */
  opacity: 0;
  transition: opacity 0.3s;
}

.playlist-scroll:hover::-webkit-scrollbar {
  /* 호버 시 표시 */
  opacity: 1;
}

.playlist-scroll::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.playlist-scroll::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 3px;
}

.playlist-scroll::-webkit-scrollbar-thumb:hover {
  background: #555;
}

.playlist-thumbnail {
  flex: 0 0 240px;
  cursor: pointer;
  transition: transform 0.2s;
}

.playlist-thumbnail:hover {
  transform: translateY(-2px);
}

.playlist-thumbnail.active .thumbnail-container {
  box-shadow: 0 0 0 3px #66a0ff;
  border-radius: 0.5rem;
}

.thumbnail-container {
  position: relative;
  border-radius: 0.5rem;
  overflow: hidden;
  aspect-ratio: 16/9;
}

.thumbnail-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.duration {
  position: absolute;
  bottom: 0.5rem;
  right: 0.5rem;
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 0.2rem 0.4rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
}

.now-playing {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  font-size: 0.875rem;
}

.playing-indicator {
  width: 8px;
  height: 8px;
  background-color: white;
  border-radius: 50%;
  animation: pulse 1.5s infinite;
}

.thumbnail-title {
  margin-top: 0.5rem;
  font-size: 0.875rem;
  line-height: 1.4;
  height: 2.8em;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.5; }
  100% { opacity: 1; }
}

@media (max-width: 768px) {
  .playlist-thumbnail {
    flex: 0 0 200px;
  }
}
</style>