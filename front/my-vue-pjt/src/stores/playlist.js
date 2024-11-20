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
      headers: {
        'Authorization': `Token ${authStore.token}`,
      }
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

  // 플레이리스트 목록 가져오기
  const fetchPlaylists = () => {
    loading.value = true
    return apiRequest('get', '/api/playlist/')
      .then((response) => {
        playlists.value = response.data
        return response.data
      })
      .catch((error) => {
        console.error('플레이리스트 가져오기 실패:', error)
        error.value = error.message
        playlists.value = []
      })
      .finally(() => {
        loading.value = false
      })
  }

  // 새 플레이리스트 생성
  const createPlaylist = (formData) => {
    loading.value = true
    return apiRequest('post', '/api/playlist/', formData, true)
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
    fetchReviews
  }
})