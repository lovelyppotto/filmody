<template>
    <div class="profile-container font-nanum">
      <h1 class="profile-title">Profile</h1>
      <form @submit.prevent="updateProfile" class="profile-form">
        <!-- Profile Image Section -->
        <div class="form-group profile-image-container">
          <label for="profile_image" class="label">
            프로필 사진:
            <img
              :key="userInfo.profile_image"
              :src="previewImage || `${userInfo.profile_image}`"
              alt="프로필 사진"
              class="profile-preview"
            />
          </label>
          <button
            v-if="userInfo.profile_image && !userInfo.profile_image.includes('default.png')"
            @click.prevent="deleteProfileImage"
            class="delete-button"
          >
            삭제
          </button>
          <input
            type="file"
            id="profile_image"
            @change.stop="handleImageUpload"
            accept="image/*"
            class="file-input"
          />
        </div>
  
        <!-- Username -->
        <div class="form-group">
          <label for="username" class="label">아이디:</label>
          <input
            type="text"
            id="username"
            v-model="userInfo.username"
            disabled
            class="input-field"
          />
        </div>
  
        <!-- Passwords -->
        <div class="form-group">
          <label for="current_password" class="label">현재 비밀번호:</label>
          <input
            type="password"
            id="current_password"
            v-model="passwords.current_password"
            class="input-field"
          />
        </div>
        <div class="form-group">
          <label for="new_password1" class="label">새 비밀번호:</label>
          <input
            type="password"
            id="new_password1"
            v-model="passwords.new_password1"
            class="input-field"
          />
        </div>
        <div class="form-group">
          <label for="new_password2" class="label">새 비밀번호 확인:</label>
          <input
            type="password"
            id="new_password2"
            v-model="passwords.new_password2"
            class="input-field"
          />
        </div>
  
        <!-- Nickname -->
        <div class="form-group">
          <label class="label">닉네임:</label>
          <input
            type="text"
            v-model="userInfo.nickname"
            class="input-field"
          />
        </div>
  
        <!-- Email -->
        <div class="form-group">
          <label class="label">이메일:</label>
          <input
            type="text"
            v-model="userInfo.email"
            class="input-field"
          />
        </div>
  
        <!-- Show Reviews -->
        <div class="form-group">
          <label class="label">리뷰 보기:</label>
          <input
            type="checkbox"
            v-model="userInfo.show_reviews"
            class="checkbox-input"
          />
        </div>
  
        <button type="submit" class="save-button">Save Changes</button>
      </form>
  
      <!-- 회원 탈퇴 -->
      <button @click="showDeleteModal = true" class="delete-account-button">회원 탈퇴</button>
  
      <!-- Modal -->
      <div v-if="showDeleteModal" class="modal">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">회원 탈퇴</h5>
              <button
                type="button"
                class="btn-close"
                aria-label="Close"
                @click="showDeleteModal = false"
              ></button>
            </div>
            <div class="modal-body">
              <p>비밀번호 입력 후 탈퇴 버튼 선택 시, 계정은 삭제되며 복구되지 않습니다.</p>
              <input
                type="password"
                v-model="deletePassword"
                placeholder="비밀번호를 입력해주세요."
                class="input-field"
              />
            </div>
            <div class="modal-footer">
              <button
                type="button"
                class="delete-button"
                @click="deleteAccount"
              >
                탈퇴
              </button>
              <button
                type="button"
                class="cancel-button"
                @click="showDeleteModal = false"
              >
                취소
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  

<script setup>
import { useAuthStore } from '@/stores/auth';
import axios from 'axios';
import { ref, onMounted } from 'vue';

const store = useAuthStore();
const userInfo = ref({
    username: '',
    nickname: '',
    email: '',
    show_reviews: false,
    profile_image: '',
});
const previewImage = ref('');
const passwords = ref({
    current_password: '',
    new_password1: '',
    new_password2: '',
});
const deletePassword = ref(null);
const showDeleteModal = ref(false);

// 기존 script setup과 동일
</script>

<style scoped>
/* 스타일은 이전과 동일하게 유지 */
.modal {
    display: block;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: 1050;
}

.modal-dialog {
    position: relative;
    width: auto;
    margin: 1.75rem auto;
    max-width: 500px;
}

.modal-content {
    position: relative;
    background-color: #fff;
    border-radius: 0.3rem;
    padding: 1rem;
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    border-bottom: 1px solid #dee2e6;
}

.modal-title {
    margin: 0;
}

.modal-body {
    padding: 1rem;
}

.modal-footer {
    display: flex;
    justify-content: flex-end;
    gap: 0.5rem;
    padding: 1rem;
    border-top: 1px solid #dee2e6;
}

.btn {
    padding: 0.375rem 0.75rem;
    border-radius: 0.25rem;
    border: 1px solid transparent;
    cursor: pointer;
}

.btn-danger {
    color: #fff;
    background-color: #dc3545;
    border-color: #dc3545;
}

.btn-secondary {
    color: #fff;
    background-color: #6c757d;
    border-color: #6c757d;
}

.btn-close {
    background: transparent;
    border: 0;
    font-size: 1.5rem;
    cursor: pointer;
}

input[type="password"],
input[type="text"],
input[type="email"] {
    width: 100%;
    padding: 0.375rem 0.75rem;
    margin: 0.5rem 0;
    border: 1px solid #ced4da;
    border-radius: 0.25rem;
}

.profile-image-container {
    margin: 20px 0;
}

.profile-preview {
    width: 150px;
    height: 150px;
    border-radius: 50%;
    margin: 10px 0;
    border: 2px solid #ddd;
}

input[type="file"] {
    display: block;
    margin-top: 10px;
}

input[type="file"]::file-selector-button {
    border: 2px solid #6c757d;
    padding: 0.5em 1em;
    border-radius: 0.3em;
    background-color: white;
    cursor: pointer;
    transition: all 0.2s ease;
}

input[type="file"]::file-selector-button:hover {
    background-color: #6c757d;
    color: white;
}


</style>
