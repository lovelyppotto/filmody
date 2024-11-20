<template>
    <div class="search-box">
      <input
        :value="modelValue"
        @input="handleInput($event.target.value)"
        type="text"
        placeholder="영화 제목이나 감독명을 입력하세요"
        class="search-input"
      />
      <div v-if="isLoading" class="loading">검색중...</div>
    </div>
  </template>
  

<script setup>
import { useMovieStore } from '@/stores/movie'

const store = useMovieStore()

defineProps({
  modelValue: String,
  isLoading: Boolean
})

const emit = defineEmits(['update:modelValue'])

let searchTimer

const handleInput = (value) => {
  emit('update:modelValue', value)
  clearTimeout(searchTimer)
  searchTimer = setTimeout(() => {
    store.searchMovies(value)
  }, 300)
}
</script>

<style scoped>

</style>