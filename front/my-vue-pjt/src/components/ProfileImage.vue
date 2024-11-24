<!-- ProfileImage.vue -->
<template>
    <div class="image-upload-section">
      <img
        :key="modelValue"
        :src="previewImage || modelValue"
        alt=""
        class="profile-preview"
      />
      <input
        type="file"
        @change="onImageChange"
        accept="image/*"
        class="file-input"
      />
      <button
        v-if="modelValue && !modelValue.includes('default.png')"
        @click="onDelete"
        class="delete-button"
      >
        이미지 삭제
      </button>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  
  const props = defineProps({
    modelValue: String
  });
  
  const emit = defineEmits(['update', 'delete']);
  const previewImage = ref('');
  
  const onImageChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      emit('update', file);
    }
  };
  
  const onDelete = () => {
    emit('delete');
  };
  </script>