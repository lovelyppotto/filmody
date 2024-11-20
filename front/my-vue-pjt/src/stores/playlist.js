// stores/playlist.js
import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const usePlaylistStore = defineStore('playlist', () => {
  const playlists = ref([])
  const currentPlaylist = ref(null)
  const loading = ref(false)
  const error = ref(null)
  
  // API Base URL
  const BASE_URL = 'http://127.0.0.1:8000'  // Django REST API URL


  const api = axios.create({
    baseURL: 'http://127.0.0.1:8000',
    withCredentials: true,  // 쿠키를 주고받기 위해 필요
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': document.cookie.match(/csrftoken=([\w-]+)/)?.[1]
    }
  })

  // 모든 플레이리스트 가져오기
  const fetchPlaylists = () => {
    loading.value = true
    return api.get('/api/playlist/')
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

  // 특정 플레이리스트 가져오기
  const fetchPlaylistById = (id) => {
    loading.value = true
    return api.get(`/api/playlist/${id}/`)
      .then((response) => {
        currentPlaylist.value = response.data
        return response.data
      })
      .catch((error) => {
        console.error(`플레이리스트 ${id} 가져오기 실패:`, error)
        error.value = error.message
        currentPlaylist.value = null
      })
      .finally(() => {
        loading.value = false
      })
    }

  // 새 플레이리스트 생성
  const createPlaylist = (playlistData) => {
    loading.value = true
    return api.post('/api/playlist/', playlistData)
      .then((response) => {
        playlists.value.push(response.data)
        return response.data
      })
      .catch((error) => {
        console.error('플레이리스트 생성 실패:', error)
        error.value = error.message
        throw error
      })
      .finally(() => {
        loading.value = false
      })
  }

  // 플레이리스트에 트랙 추가
  const addTrackToPlaylist = (playlistId, trackData) => {
    loading.value = true
    return axios.post(`${BASE_URL}/api/playlist/${playlistId}/tracks/`, trackData)
      .then((response) => {
        const playlist = playlists.value.find(p => p.id === playlistId)
        if (playlist && playlist.tracks) {
          playlist.tracks.push(response.data)
        }
        return response.data
      })
      .catch((error) => {
        console.error('트랙 추가 실패:', error)
        error.value = error.message
      })
      .finally(() => {
        loading.value = false
      })
  }

  // 플레이리스트에서 트랙 제거
  const removeTrackFromPlaylist = (playlistId, trackId) => {
    loading.value = true
    return axios.delete(`${BASE_URL}/api/playlist/${playlistId}/tracks/${trackId}/`)
      .then(() => {
        const playlist = playlists.value.find(p => p.id === playlistId)
        if (playlist && playlist.tracks) {
          playlist.tracks = playlist.tracks.filter(track => track.id !== trackId)
        }
      })
      .catch((error) => {
        console.error('트랙 제거 실패:', error)
        error.value = error.message
      })
      .finally(() => {
        loading.value = false
      })
  }

  // YouTube URL에서 video ID 추출
  const extractVideoId = (url) => {
    const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|&v=)([^#&?]*).*/
    const match = url.match(regExp)
    return (match && match[2].length === 11) ? match[2] : null
  }

  // YouTube API로 비디오 정보 가져오기
  const fetchVideoInfo = (url) => {
    loading.value = true
    error.value = null
    const videoId = extractVideoId(url)

    if (!videoId) {
      error.value = '올바른 YouTube URL이 아닙니다'
      loading.value = false
      return Promise.reject(error.value)
    }

    // YouTube Data API endpoint
    const API_KEY = process.env.VUE_APP_YOUTUBE_API_KEY // .env 파일에서 API 키 가져오기
    const endpoint = `https://www.googleapis.com/youtube/v3/videos`

    return axios.get(endpoint, {
      params: {
        key: API_KEY,
        part: 'snippet',
        id: videoId
      }
    })
      .then((response) => {
        const videoData = response.data.items[0]
        if (!videoData) {
          throw new Error('영상을 찾을 수 없습니다')
        }

        return {
          video_id: videoId,
          title: videoData.snippet.title,
          thumbnail_url: videoData.snippet.thumbnails.default.url,
        }
      })
      .catch((err) => {
        error.value = err.message
        throw err
      })
      .finally(() => {
        loading.value = false
      })
    }

  return {
    BASE_URL,
    playlists,
    currentPlaylist,
    loading,
    error,
    fetchPlaylists,
    fetchPlaylistById,
    createPlaylist,
    addTrackToPlaylist,
    fetchVideoInfo,
    removeTrackFromPlaylist
  }
})