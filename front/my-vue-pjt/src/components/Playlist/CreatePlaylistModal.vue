<template>
  <div 
    class="modal fade show d-block"
    style="background-color: rgba(0, 0, 0, 0.5);"
  >
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">새 플레이리스트 만들기</h5>
          <button 
            type="button" 
            class="btn-close" 
            @click="handleClose"
          ></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="handleSubmit">
            <!-- 제목 입력 -->
            <div class="mb-3">
              <label class="form-label">제목</label>
              <input 
                v-model="formData.title"
                type="text"
                class="form-control"
                required
              >
            </div>

            <!-- 이미지 업로드 -->
            <div class="mb-3">
              <label class="form-label">커버 이미지</label>
              <input 
                type="file"
                class="form-control"
                @change="handleImageUpload"
                accept="image/*"
              >
              <div v-if="imagePreview" class="mt-2">
                <img 
                  :src="imagePreview" 
                  alt="Preview" 
                  class="img-thumbnail"
                  style="max-width: 200px;"
                >
              </div>
            </div>

            <!-- 공개 여부 -->
            <div class="mb-3">
              <div class="form-check">
                <input 
                  type="checkbox"
                  class="form-check-input"
                  id="isPublic"
                  v-model="formData.is_public"
                >
                <label class="form-check-label" for="isPublic">공개</label>
              </div>
            </div>

            <div class="modal-footer">
              <button 
                type="button" 
                class="btn btn-secondary" 
                @click="handleClose"
              >
                취소
              </button>
              <button 
                type="submit" 
                class="btn btn-primary"
                :disabled="loading"
              >
                {{ loading ? '생성 중...' : '만들기' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits } from 'vue'

const props = defineProps({
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'submit', 'close'])

const imagePreview = ref(null)
const formData = ref({
  title: '',
  cover_img: null,
  is_public: true
})

const handleImageUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    formData.value.cover_img = file
    const reader = new FileReader()
    reader.onload = e => {
      imagePreview.value = e.target.result
    }
    reader.readAsDataURL(file)
  }
}

const handleSubmit = () => {
  const submitData = new FormData()
  submitData.append('title', formData.value.title)
  submitData.append('is_public', formData.value.is_public)
  if (formData.value.cover_img) {
    submitData.append('cover_img', formData.value.cover_img)
  }
  emit('submit', submitData)
}

const handleClose = () => {
  emit('close')
  resetForm()
}

const resetForm = () => {
  formData.value = {
    title: '',
    cover_img: null,
    is_public: true
  }
  imagePreview.value = null
}
</script>