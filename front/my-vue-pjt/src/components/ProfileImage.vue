<template>
    <div class="image-upload-section">
      <img
        :key="modelValue"
        :src="previewImage || modelValue"
        alt="프로필 이미지"
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
  import { ref, watch } from 'vue';
  
  const props = defineProps({
    modelValue: String
  });
  
  const emit = defineEmits(['update', 'delete']);
  const previewImage = ref('');
  
  // modelValue가 바뀔 때마다 previewImage를 업데이트
  watch(
    () => props.modelValue,
    (newValue) => {
      previewImage.value = newValue;
    },
    { immediate: true }
  );
  
  const onImageChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      // 파일이 선택되면 부모에게 변경된 파일을 전달
      const reader = new FileReader();
      reader.onload = () => {
        emit('update', reader.result); // 미리보기 이미지 데이터를 부모에게 전달
      };
      reader.readAsDataURL(file); // 파일을 Data URL로 읽어들임
    }
  };
  
  const onDelete = () => {
    // 삭제 시 부모에게 알림
    emit('delete');
    previewImage.value = ''; // 로컬 미리보기 이미지 초기화
  };
  </script>
  
  