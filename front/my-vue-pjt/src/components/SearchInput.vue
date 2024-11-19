<template>
    <div class="search-box">
      <input
        :value="modelValue"
        @input="emit('update:modelValue', $event.target.value)"
        type="text"
        placeholder="영화 제목이나 감독명을 입력하세요"
        class="search-input"
      />
      <div v-if="isLoading" class="loading">검색중...</div>
    </div>
  </template>
  

<script setup>
defineProps({
  modelValue: String,
  isLoading: Boolean
})

const emit = defineEmits(['update:modelValue'])
</script>

<style scoped>

</style>