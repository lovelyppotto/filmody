<template>
    <div class="signup-container font-nanum">
      <h1 class="signup-title">Sign Up</h1>
      <form @submit.prevent="signUp" class="signup-form">
        <div class="form-group">
          <label for="username">아이디</label>
          <input type="text" id="username" v-model.trim="username" placeholder="아이디를 입력하세요">
        </div>
  
        <div class="form-group">
          <label for="password1">비밀번호</label>
          <input type="password" id="password1" v-model.trim="password1" placeholder="비밀번호를 입력하세요">
        </div>
  
        <div class="form-group">
          <label for="password2">비밀번호 확인</label>
          <input type="password" id="password2" v-model.trim="password2" placeholder="비밀번호를 다시 입력하세요">
        </div>
  
        <div class="form-group">
          <label for="nickname">닉네임</label>
          <input type="text" id="nickname" v-model.trim="nickname" placeholder="닉네임을 입력하세요">
        </div>
  
        <div class="form-group">
          <label for="email">이메일</label>
          <input type="text" id="email" v-model.trim="email" placeholder="이메일 주소를 입력하세요">
        </div>
  
        <button type="submit" class="signup-button">회원가입</button>
      </form>
    </div>
  </template>
  
  <script setup>
  import { useAuthStore } from '@/stores/auth';
  import { ref } from 'vue';
  
  const store = useAuthStore();
  
  const username = ref(null);
  const password1 = ref(null);
  const password2 = ref(null);
  const nickname = ref(null);
  const email = ref(null);
  
  const signUp = function () {
    const payload = {
      username: username.value,
      password1: password1.value,
      password2: password2.value,
      nickname: nickname.value,
      email: email.value,
    };
    store.signUp(payload);
  };
  </script>
  
  <style scoped>

  /* 컨테이너 */
  .signup-container {
    max-width: 600px;
    margin: 50px auto;
    padding: 20px;
    background: #ffffff;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(255, 255, 255, 0.1);
    font-family: 'Arial', sans-serif;
  }
  
  /* 타이틀 */
  .signup-title {
    font-size: 2rem;
    text-align: center;
    margin: 40px 0 40px 0;
    color: #374c72;
  }
  
  /* 폼 */
  .signup-form {
    display: flex;
    flex-direction: column;
    gap: 15px;
  }
  
  /* 폼 그룹 */
  .form-group {
    display: flex;
    flex-direction: column;
    margin-bottom: 20px;
  }
  
  /* 레이블 */
  .form-group label {
    font-size: 1rem;
    font-weight: 500;
    margin-bottom: 5px;
    color: #48505e;
  }
  
  /* 입력 필드 */
  .form-group input {
    height: 50px;
    padding: 10px;
    border-width: 0 0 1px;
    font-size: 1rem;
    transition: border-color 0.3s ease;
  }
  
  .form-group input:focus {
    outline: none;
    border-color: #b4c4dc;
    box-shadow: 0 0 2px rgba(110, 138, 181, 0.3);
  }
  
  /* 버튼 */
  .signup-button {
    padding: 10px 20px;
    background-color: #ffffff;
    color:  #42464b;
    border: 1px solid #42464b;
    border-radius: 5px;
    font-size: 1rem;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  
  .signup-button:hover {
    background-color:#42464b;
    border: 1px solid #42464b;
    color: #ffffff;
  }
  
  /* 반응형 */
  @media (max-width: 768px) {
    .signup-container {
      padding: 15px;
    }
  
    .signup-title {
      font-size: 1.5rem;
    }
  
    .form-group label {
      font-size: 0.9rem;
    }
  
    .form-group input {
      font-size: 0.9rem;
    }
  
    .signup-button {
      font-size: 0.9rem;
    }
  }
  </style>
  