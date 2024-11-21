// stores/playlist.js
import { ref } from 'vue'
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

  const addVideoToPlaylist = (playlistId, videoData) => {
    loading.value = true
    const payload = {
      video_id: videoData.id.videoId,  // 여기는 그대로
      title: videoData.snippet.title,
      thumbnail_url: videoData.snippet.thumbnails.medium.url,
      published_at: videoData.snippet.publishTime
    }
    
    console.log('전송할 데이터:', payload)  // 데이터 확인
    console.log('PlaylistId:', playlistId) // playlistId 확인
    console.log('Token:', authStore.token)  // 토큰 확인
    
    return axios({
      method: 'post',
      url: `${authStore.BASE_URL}/api/playlist/${playlistId}/videos/`,
      headers: {
        'Authorization': `Token ${authStore.token}`,
        'Content-Type': 'application/json'
      },
      data: payload
    })
      .then((response) => {
        console.log('서버 응답:', response.data)  // 성공 응답 확인
        const playlist = playlists.value.find(p => p.id === playlistId)
        if (playlist && playlist.videos) {
          playlist.videos.push(response.data)
        }
        return response.data
      })
      .catch((error) => {
        console.log('에러 상세:', error.response)  // 자세한 에러 정보 확인
        console.error('비디오 추가 실패:', error.response?.data || error.message)
        error.value = error.response?.data?.error || error.message
        throw error
      })
      .finally(() => {
        loading.value = false
      })
  }

  // 플레이리스트에 비디오 추가
// const addVideoToPlaylist = (playlistId, videoData) => {
//   loading.value = true
//   const payload = {
//     video_id: videoData.id.videoId,
//     title: videoData.snippet.title,
//     description: videoData.snippet.description,
//     thumbnail_url: videoData.snippet.thumbnails.medium.url,
//     published_at: videoData.snippet.publishTime
//   }
  
//   return axios({
//     method: 'post',
//     url: `${authStore.BASE_URL}/api/playlist/${playlistId}/videos/`,
//     headers: {
//       'Authorization': `Token ${authStore.token}`,
//       'Content-Type': 'application/json'
//     },
//     data: payload
//   })
//     .then((response) => {
//       const playlist = playlists.value.find(p => p.id === playlistId)
//       if (playlist && playlist.videos) {
//         playlist.videos.push(response.data)
//       }
//       return response.data
//     })
//     .catch((error) => {
//       console.error('비디오 추가 실패:', error.response?.data || error.message)
//       error.value = error.response?.data?.error || error.message
//       throw error
//     })
//     .finally(() => {
//       loading.value = false
//     })
// }



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

  return {
    apiRequest,
    playlists,
    reviews,
    currentPlaylist,
    loading,
    error,
    fetchPlaylists,
    createPlaylist,
    updatePlaylist,
    deletePlaylist,
    fetchReviews,
    addVideoToPlaylist,
    getPlaylistVideos,
    removeVideoFromPlaylist,
    getPlaylistVideos,
  }
})