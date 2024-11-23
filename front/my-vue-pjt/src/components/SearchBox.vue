<template>
  <div class="search-box">
    <div class="search-input-wrapper">
      <i class="fa-solid fa-magnifying-glass fa-s search-icon" style="color: #7989a4;"></i>
      <input
        :value="modelValue"
        @input="handleInput($event.target.value)"
        type="text"
        placeholder="영화 제목이나 감독명을 입력하세요"
        class="search-input"
      />
    </div>
    <div v-if="isLoading" class="loading">검색중...</div>
  </div>
</template>

<script setup>
defineProps({
  modelValue: String,
  isLoading: Boolean
})

const emit = defineEmits(['update:modelValue'])

const handleInput = (value) => {
  emit('update:modelValue', value)
}
</script>

<style scoped>
.search-box {
  width: 100%;
  max-width: 500px;
  position: relative;
  text-align: center;
  border-bottom: 1px solid #ccc;
}

.search-input-wrapper {
  display: flex;
  align-items: center;
  position: relative;
}

.search-icon {
  position: absolute;
  left: 15px;
  top: 50%;
  transform: translateY(-50%);
  z-index: 1;
}

.search-input {
  border: none;
  width: 100%;
  padding: 15px;
  padding-left: 45px; /* 아이콘 공간 확보 */
  font-size: 16px;
  border: none;
  border-radius: 8px;
  outline: none;
  transition: border-color 0.3s ease;
}

.search-input:focus {
  border-color: #007BFF;
}

.loading {
  margin-top: 10px;
  font-size: 14px;
  color: hsl(0, 0%, 53%);
}
</style>