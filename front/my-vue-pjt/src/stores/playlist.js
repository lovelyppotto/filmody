// stores/playlist.js
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useAuthStore } from './auth'

export const usePlaylistStore = defineStore('playlist', () => {
  const playlists = ref([])
  const reviews = ref({})
  const currentPlaylist = ref(null)
  const loading = ref(false)
  const error = ref(null)
  const authStore = useAuthStore()

  // API 요청 함수
  const apiRequest = (method, endpoint, data = null, isFormData = false) => {
    const config = {
      method: method,
      url: `${authStore.BASE_URL}${endpoint}`,
      headers: {}  // 기본 헤더를 비움
    }
  
    // 토큰이 있을 때만 Authorization 헤더 추가
    if (authStore.token) {
      config.headers['Authorization'] = `Token ${authStore.token}`
    }
  
    // FormData가 아닐 경우에만 Content-Type 설정
    if (!isFormData) {
      config.headers['Content-Type'] = 'application/json'
    }
  
    if (data) {
      config.data = data
    }
  
    return axios(config)
  }

  
  // 플레이리스트 목록 가져오기(방금고침)
  // stores/playlist.js의 fetchPlaylists 함수 수정
  const fetchPlaylists = () => {
    loading.value = true;
    return apiRequest('get', '/api/playlist/')
      .then((response) => {
        playlists.value = response.data;
        // 단일 플레이리스트 조회 시에도 사용할 수 있도록 데이터 반환
        return response.data;
      })
      .catch((error) => {
        console.error('플레이리스트 가져오기 실패:', error);
        error.value = error.message;
        playlists.value = [];
        // 에러를 다시 throw하여 컴포넌트에서 처리할 수 있게 함
        throw error;
      })
      .finally(() => {
        loading.value = false;
      });
  };
  
  // 새 플레이리스트 생성
  const createPlaylist = (formData) => {
    loading.value = true
    return apiRequest('post', '/api/playlist/create/', formData, true)
      .then((response) => {
        playlists.value.push(response.data)
        return response.data
      })
      .catch((error) => {
        console.error('플레이리스트 생성 실패:', error.response?.data)
        throw error
      })
      .finally(() => {
        loading.value = false
      })
  }

  // 단일 플레이리스트 조회
  const fetchPlaylist = (id) => {
    loading.value = true;
    return apiRequest('get', `/api/playlist/${id}/`)
      .then((response) => {
        return response.data;
      })
      .catch((error) => {
        console.error('플레이리스트 조회 실패:', error);
        error.value = error.message;
        throw error;
      })
      .finally(() => {
        loading.value = false;
      });
  };



  // 플레이리스트 수정
  const updatePlaylist = (playlistId, playlistData) => {
    loading.value = true
    return apiRequest('put', `/api/playlist/${playlistId}/`, playlistData)
      .then((response) => {
        const index = playlists.value.findIndex(p => p.id === playlistId)
        if (index !== -1) {
          playlists.value[index] = response.data
        }
        return response.data
      })
      .catch((error) => {
        console.error('플레이리스트 수정 실패:', error)
        error.value = error.message
        throw error
      })
      .finally(() => {
        loading.value = false
      })
  }

  // 플레이리스트 삭제
  const deletePlaylist = (playlistId) => {
    loading.value = true
    return apiRequest('delete', `/api/playlist/${playlistId}/`)
      .then(() => {
        playlists.value = playlists.value.filter(p => p.id !== playlistId)
      })
      .catch((error) => {
        console.error('플레이리스트 삭제 실패:', error)
        error.value = error.message
        throw error
      })
      .finally(() => {
        loading.value = false
      })
  }

  // 해당 플레이리스트의 리뷰 가져오기
  const fetchReviews = (playlistId) => {
    if (reviews.value[playlistId]) {
      return Promise.resolve(reviews.value[playlistId]); // 이미 리뷰가 있다면 그대로 반환
    }
    loading.value = true;
    return apiRequest('get', `/api/playlist/${playlistId}/reviews/`)
      .then((response) => {
        reviews.value[playlistId] = response.data;
        return response.data;
      })
      .catch((err) => {
        console.error(`리뷰 가져오기 실패: ${err}`);
        error.value = err.message;
        reviews.value[playlistId] = [];
      })
      .finally(() => {
        loading.value = false;
      });
  };

  const getPlaylistVideos = (playlistId) => {
    loading.value = true
    return apiRequest('get', `/api/playlist/${playlistId}/videos/`)
      .then((response) => {
        const playlist = playlists.value.find(p => p.id === playlistId)
        if (playlist) {
          playlist.videos = response.data
        }
        return response.data
      })
      .catch((error) => {
        console.error('비디오 목록 가져오기 실패:', error)
        error.value = error.message
        throw error
      })
      .finally(() => {
        loading.value = false
      })
  }

  // stores/playlist.js
  const addVideoToPlaylist = (playlistId, videoData) => {
    loading.value = true
    const payload = {
      video_id: videoData.id.videoId,
      title: videoData.snippet.title,
      thumbnail_url: videoData.snippet.thumbnails.medium.url,
      published_at: videoData.snippet.publishTime
    }
    
    return apiRequest('post', `/api/playlist/${playlistId}/videos/`, payload)
      .then((response) => {
        const playlist = playlists.value.find(p => p.id === playlistId)
        if (playlist) {
          if (!playlist.videos) {
            playlist.videos = []
          }
          playlist.videos.push(response.data)
        }
        return response.data
      })
      .catch((error) => {
        console.error('비디오 추가 실패:', error.response?.data || error.message)
        error.value = error.response?.data?.error || error.message
        throw error
      })
      .finally(() => {
        loading.value = false
      })
}


  // 플레이리스트에서 비디오 삭제
  const removeVideoFromPlaylist = (playlistId, videoId) => {
    loading.value = true
    return apiRequest('delete', `/api/playlist/${playlistId}/videos/?video_id=${videoId}`)
      .then(() => {
        const playlist = playlists.value.find(p => p.id === playlistId)
        if (playlist && playlist.videos) {
          playlist.videos = playlist.videos.filter(v => v.video_id !== videoId)
        }
      })
      .catch((error) => {
        console.error('비디오 삭제 실패:', error)
        error.value = error.message
        throw error
      })
      .finally(() => {
        loading.value = false
      })
  }

  // 좋아요 토글 함수
  const toggleLike = (playlistId) => {
    return apiRequest('post', `/api/playlist/${playlistId}/like/`)
      .then((response) => {
        playlists.value = playlists.value.map(playlist => {
          if (playlist.id === playlistId) {
            return {
              ...playlist,
              is_liked: response.data.liked,
              likes_count: response.data.likes_count
            }
          }
          return playlist
        })
        return response.data
      })
      .catch((error) => {
        console.error('좋아요 처리 실패:', error)
        throw error
      })
}

  const canLikePlaylist = computed(() => {
    if (!currentPlaylist.value || !authStore.userData) return false;
    return currentPlaylist.value.user !== authStore.userData.id;
  });

  const likedPlaylists = ref([]) 
  const myPlaylists = ref([]) 

  const fetchLikedPlaylists = () => {
    console.log('fetchLikedPlaylists 시작')
    loading.value = true
    error.value = null
    
    return apiRequest('get', `/api/playlist/liked-playlist/`)
      .then(response => {
        console.log('받아온 데이터:', response.data)
        likedPlaylists.value = response.data
        console.log('저장된 데이터:', likedPlaylists.value)
      })
      .catch(err => {
        console.error('API 에러:', err.response?.data || err)
        error.value = '회원에게 제공되는 기능입니다.'
      })
      .finally(() => {
        loading.value = false
        // console.log('최종 상태:', {
        //   loading: loading.value,
        //   error: error.value,
        //   playlistsCount: likedPlaylists.value.length,
        //   playlists: likedPlaylists.value
        // })
      })
  }

  const fetchMyPlaylist = () => {
    loading.value = true
    error.value = null
    
    return apiRequest('get', `/api/playlist/my-playlist/`)
      .then(response => {
        console.log('받아온 데이터:', response.data)
        myPlaylists.value = response.data
        console.log('저장된 데이터:', myPlaylists.value)
      })
      .catch(err => {
        console.error('API 에러:', err.response?.data || err)
        error.value = '플레이리스트를 불러오는데 실패했습니다.'
      })
      .finally(() => {
        loading.value = false
        console.log('최종 상태:', {
          loading: loading.value,
          error: error.value,
          playlistsCount: myPlaylists.value.length,
          playlists: myPlaylists.value
        })
      })
  }


  return {
    apiRequest,
    playlists,
    reviews,
    currentPlaylist,
    loading,
    error,
    fetchPlaylists,
    fetchPlaylist,
    createPlaylist,
    updatePlaylist,
    deletePlaylist,
    fetchReviews,
    addVideoToPlaylist,
    removeVideoFromPlaylist,
    getPlaylistVideos,
    toggleLike,
    canLikePlaylist,
    fetchLikedPlaylists,
    likedPlaylists,
    myPlaylists,
    fetchMyPlaylist,
  }
})