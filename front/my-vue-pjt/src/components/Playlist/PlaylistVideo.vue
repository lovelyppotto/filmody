<template>
  <div class="playlist-videos">
    <!-- 플레이리스트가 비어있을 때 -->
    <div v-if="!videos.length" class="text-center p-5">
      <h3 class="mb-3">플레이리스트가 비어있습니다</h3>
      <p class="text-muted">재생할 영상을 추가해주세요</p>
    </div>

    <!-- 플레이리스트에 영상이 있을 때만 캐러셀 표시 -->
    <template v-else>
      <div id="videoCarousel" class="carousel slide" data-bs-interval="false">
        <div class="carousel-inner">
          <div 
            v-for="(video, index) in videos" 
            :key="video.video_id"
            :class="['carousel-item', { active: index === 0 }]"
          >
            <div class="card">
              <div class="row g-0">
                <div class="col-md-12">
                  <div class="ratio ratio-16x9 position-relative">
                    <div :id="`youtube-player-${index}`"></div>
                    <!-- 재생 대기 메시지 -->
                    <div v-if="showPlayMessage && activeIndex === index" 
                      class="play-message" 
                      style="position: absolute; z-index: 10; background: rgba(0,0,0,0.7); color: white; padding: 1rem;">
                      {{ countdown }}초 후 재생됩니다...
                    </div>
                  </div>
                </div>
                <div class="col-md-12">
                  <div class="card-body">
                    <h5 class="card-title">{{ video.title }}</h5>
                    <div class="d-flex justify-content-between align-items-center mt-3">
                      <small class="text-muted">
                        {{ formatDate(video.published_at) }}
                      </small>
                      <button 
                        class="btn btn-danger btn-sm"
                        @click="removeVideo(video)"
                        :disabled="isLoading"
                      >
                        <span v-if="isLoading" class="spinner-border spinner-border-sm me-1"></span>
                        삭제
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <button class="carousel-control-prev" type="button" data-bs-target="#videoCarousel" data-bs-slide="prev">
          <span class="carousel-control-prev-icon" aria-hidden="true"></span>
          <span class="visually-hidden">Previous</span>
        </button>
        <button class="carousel-control-next" type="button" data-bs-target="#videoCarousel" data-bs-slide="next">
          <span class="carousel-control-next-icon" aria-hidden="true"></span>
          <span class="visually-hidden">Next</span>
        </button>
      </div>

      <div class="video-thumbnails mt-3 d-flex overflow-auto">
        <div 
          v-for="(video, index) in videos" 
          :key="video.video_id"
          class="thumbnail-item me-2"
          @click="goToSlide(index)"
        >
          <img 
            :src="video.thumbnail_url" 
            :alt="video.title"
            class="img-fluid rounded"
            style="width: 160px; height: 90px; object-fit: cover;"
          >
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { usePlaylistStore } from '@/stores/playlist';
import { Carousel } from 'bootstrap';

// 자동 재생 상태 여부 추적하는 변수
const isAutoPlay = ref(false);

const showPlayMessage = ref(false);
const countdown = ref(5);
let countdownTimer = null;

const startPlaybackDelay = (player, isAutoplay = false) => {
  if (isAutoplay) {
    return Promise.resolve();
  }

  console.log("카운트다운 시작");
  showPlayMessage.value = true;
  countdown.value = 5;

  if (countdownTimer) {
    clearInterval(countdownTimer);
  }

  return new Promise((resolve) => {
    countdownTimer = setInterval(() => {
      countdown.value--;
      console.log("현재 countdown 값:", countdown.value);

      if (countdown.value <= 0) {
        clearInterval(countdownTimer);
        showPlayMessage.value = false;
        resolve();
      }
    }, 1000);
  });
};

const props = defineProps({
  playlistId: {
    type: Number,
    required: true
  }
});

const playlistStore = usePlaylistStore();
const videos = ref([]);
const isLoading = ref(false);
const activeIndex = ref(0);
let carousel = null;
const players = ref({});

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

const initializePlayers = async () => {
try {
  const YT = await loadYouTubeAPI();

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
        onReady: async (event) => {
          event.target.setVolume(10);
          
          if (index === 0) {
            await startPlaybackDelay(event.target);
            event.target.playVideo();
          }
        },
        onStateChange: (event) => {
          // 영상이 끝났을 때 
          if (event.data === YT.PlayerState.ENDED) {
            isAutoPlay.value = true;  // 자동 재생 상태로 설정
            showPlayMessage.value = false;  // 메시지 숨기기
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
} catch (error) {
  console.error('YouTube 플레이어 초기화 실패:', error);
}
};

const handleSlideChange = async (event) => {
const newIndex = event.to;
activeIndex.value = newIndex;

// 자동 재생이 아닌 경우에만 딜레이와 메시지를 표시
if (!isAutoPlay.value) {
  // 이전 영상들 정지
  Object.entries(players.value).forEach(([idx, player]) => {
    if (Number(idx) !== newIndex && player.stopVideo) {
      player.stopVideo();
    }
  });

  // 새 영상 딜레이 후 재생
  const currentPlayer = players.value[newIndex];
  if (currentPlayer?.playVideo) {
    await startPlaybackDelay(currentPlayer);
    currentPlayer.playVideo();
  }
}

// 상태 초기화
isAutoPlay.value = false;
};


const goToSlide = async (index) => {
  carousel?.to(index);
  const currentPlayer = players.value[index];
  if (currentPlayer?.playVideo) {
    await startPlaybackDelay(currentPlayer);
    currentPlayer.playVideo();
  }
};

const formatDate = (dateString) => {
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  }).format(date);
};

const loadPlaylistVideos = async () => {
  try {
    videos.value = await playlistStore.getPlaylistVideos(props.playlistId);
  } catch (error) {
    console.error('플레이리스트 영상을 불러오는데 실패했습니다:', error);
  }
};

const removeVideo = async (video) => {
  isLoading.value = true;
  try {
    await playlistStore.removeVideoFromPlaylist(props.playlistId, video.video_id);
    await loadPlaylistVideos();
  } catch (error) {
    console.error('영상 삭제 실패:', error);
  } finally {
    isLoading.value = false;
  }
};

onMounted(async () => {
  await loadPlaylistVideos();
  
  carousel = new Carousel('#videoCarousel', {
    interval: false
  });

  document.getElementById('videoCarousel')?.addEventListener('slid.bs.carousel', handleSlideChange);

  if (videos.value.length > 0) {
    await initializePlayers();
  }
});

onUnmounted(() => {
  Object.values(players.value).forEach(player => {
    if (player.destroy) {
      player.destroy();
    }
  });

  carousel?.dispose();
  document.getElementById('videoCarousel')?.removeEventListener('slid.bs.carousel', handleSlideChange);
});
</script>

<style scoped>
/* 기존 스타일 유지 */
.carousel-control-prev,
.carousel-control-next {
  background-color: rgba(0, 0, 0, 0.5);
  width: 5%;
}

.carousel-item {
  padding: 1rem;
}

.video-thumbnails {
  scrollbar-width: thin;
  scrollbar-color: #888 #f1f1f1;
}

.video-thumbnails::-webkit-scrollbar {
  height: 6px;
}

.video-thumbnails::-webkit-scrollbar-track {
  background: #f1f1f1;

}

.video-thumbnails::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 3px;
}

.thumbnail-item {
  transition: transform 0.2s;
}

.thumbnail-item:hover {
  transform: translateY(-2px);
}

.carousel-control-prev,
.carousel-control-next {
background-color: rgba(0, 0, 0, 0.5); /* 버튼 배경 투명도 */
width: 2rem; /* 버튼 너비 */
height: 2rem; /* 버튼 높이 */
border-radius: 50%; /* 원형 버튼 */
display: flex;
align-items: center;
justify-content: center;
position: absolute;
top: 45%; /* 캐러셀 높이의 50%로 버튼 위치 설정 */
transform: translateY(-50%); /* 정확히 중앙에 정렬 */
z-index: 10; /* 버튼이 영상 위에 보이도록 설정 */
}

.carousel-control-prev {
left: 0.5rem; /* 왼쪽 버튼 위치 */
}

.carousel-control-next {
right: 0.5rem; /* 오른쪽 버튼 위치 */
}

.carousel-control-prev-icon,
.carousel-control-next-icon {
width: 1rem; /* 아이콘 크기 */
height: 1rem;
}


</style>