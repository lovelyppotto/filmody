<template>
    <div v-if="isVisible" @click="handleBackdropClick" class="modal-backdrop">
      <div class="modal-content" @click.stop>
        <p class="modal-message">회원가입이 정상적으로 처리되었습니다.</p>
        <p class="modal-message">자동으로 로그인됩니다.</p>
        <button @click="onConfirm" class="modal-button">확인</button>
      </div>
    </div>
  </template>
  
  <script setup>
  import { defineProps, defineEmits } from 'vue';
  
  const props = defineProps({
    isVisible: {
      type: Boolean,
      required: true
    }
  });
  
  const emit = defineEmits(['confirm', 'close']);
  
  const handleBackdropClick = () => {
    emit('close');
  };
  
  const onConfirm = () => {
    emit('confirm');
  };
  </script>
  
  <style scoped>
  .modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
  }
  
  .modal-content {
    background-color: white;
    padding: 2rem;
    border-radius: 8px;
    text-align: center;
    max-width: 90%;
    width: 400px;
  }
  
  .modal-message {
    margin: 2px 0;
    font-size: 1.1rem;
    color: #333;
  }
  
  .modal-button {
    margin-top: 1.5rem;
    padding: 0.5rem 2rem;
    background-color: #374c72;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1rem;
    transition: background-color 0.3s;
  }
  
  .modal-button:hover {
    background-color: #747c98;
  }
  </style>