<!-- components/VideoCard.vue -->
<template>
    <div class="flex items-center justify-between bg-white p-4 rounded-lg shadow hover:shadow-md transition-shadow">
      <!-- 썸네일과 제목 영역 -->
      <div class="flex items-center gap-4">
        <div class="w-32 h-20 overflow-hidden rounded-md">
          <img 
            :src="video.thumbnail_url" 
            :alt="video.title"
            class="w-full h-full object-cover"
          >
        </div>
        <div>
          <h3 class="font-medium text-gray-800">{{ video.title }}</h3>
          <p class="text-sm text-gray-500">{{ formatOrderNum }}</p>
        </div>
      </div>
  
      <!-- 컨트롤 버튼들 -->
      <div class="flex items-center gap-2">
        <button 
          @click="$emit('play')"
          class="p-2 text-blue-500 hover:bg-blue-50 rounded-full"
          title="재생"
        >
          ▶️
        </button>
        <button 
          v-if="isEditable"
          @click="$emit('remove')"
          class="p-2 text-red-500 hover:bg-red-50 rounded-full"
          title="삭제"
        >
          🗑️
        </button>
      </div>
    </div>
  </template>
  
  <script setup>
  import { computed } from 'vue'
  
  const props = defineProps({
    video: {
      type: Object,
      required: true
    },
    isEditable: {
      type: Boolean,
      default: false
    }
  })
  
  const formatOrderNum = computed(() => {
    return `#${props.video.order_num}`
  })
  
  defineEmits(['play', 'remove'])
  </script>