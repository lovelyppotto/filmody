<!-- src/components/PlaylistReviews/AlertModal.vue -->
<template>
  <div v-if="isOpen" class="modal-backdrop">
    <div class="modal">
      <div class="modal-content">
        <h3 class="modal-title">{{ title }}</h3>
        <p class="modal-message">{{ message }}</p>
        <button class="modal-button" @click="onClose">확인</button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  isOpen: Boolean,
  title: {
    type: String,
    default: '알림'
  },
  message: String
});

const emit = defineEmits(['close']);

const onClose = () => {
  emit('close');
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
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }
  
  .modal {
    background: white;
    border-radius: 8px;
    padding: 20px;
    width: 90%;
    max-width: 400px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  }
  
  .modal-content {
    text-align: center;
  }
  
  .modal-title {
    font-size: 1.2rem;
    font-weight: bold;
    margin-bottom: 10px;
  }
  
  .modal-message {
    margin-bottom: 20px;
    color: #666;
  }
  
  .modal-button {
    background-color: #007bff;
    color: white;
    border: none;
    padding: 8px 20px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1rem;
  }
  
  .modal-button:hover {
    background-color: #0056b3;
  }
  </style>