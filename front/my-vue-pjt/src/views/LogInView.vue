<template>
  <div class="login-container font-nanum">
    <h1 class="login-title">Login</h1>
    <form @submit.prevent="logIn" class="login-form">
      <div class="form-group">
        <label for="username">아이디</label>
        <input type="text" id="username" v-model.trim="username" placeholder="아이디를 입력하세요">
      </div>

      <div class="form-group">
        <label for="password">비밀번호</label>
        <input type="password" id="password" v-model.trim="password" placeholder="비밀번호를 입력하세요">
      </div>

      <div v-if="loginError" class="error-message">
        아이디 또는 비밀번호가 올바르지 않습니다.
      </div>

      <button type="submit" class="login-button">로그인</button>
    </form>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const store = useAuthStore();

const username = ref(null);
const password = ref(null);
const loginError = ref(false);

const logIn = async function () {
  if (!username.value || !password.value) {
    loginError.value = true;
    return;
  }

  const payload = {
    username: username.value,
    password: password.value,
  };

  try {
    // 로그인 요청
    const result = await store.logIn(payload);
    
    // store의 token이나 isAuthenticated 상태를 확인
    if (store.token) {  // 또는 store.isAuthenticated 등 인증 상태 확인
      loginError.value = false;
      router.push({ name: 'home' });
    } else {
      loginError.value = true;
    }
  } catch (error) {
    console.error('로그인 실패:', error);
    loginError.value = true;
    // 입력 필드 초기화 (선택사항)
    password.value = null;
  }
};
</script>

<style scoped>
/* 컨테이너 */
.login-container {
  max-width: 600px;
  margin: 50px auto;
  padding: 20px;
  background: #ffffff;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(255, 255, 255, 0.1);
  font-family: 'Arial', sans-serif;
}

/* 타이틀 */
.login-title {
  font-size: 2rem;
  text-align: center;
  margin: 40px 0 40px 0;
  color: #374c72;
}

/* 폼 */
.login-form {
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
  border-color: #a8aeb5;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.form-group input:focus {
  outline: none;
  border-color: #b4c4dc;
  box-shadow: 0 0 2px rgba(110, 138, 181, 0.3);
}

/* 버튼 */
.login-button {
  padding: 10px 20px;
  background-color: #ffffff;
  color: #42464b;
  border: 1px solid #42464b;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.login-button:hover {
  background-color:#42464b;
    border: 1px solid #42464b;
    color: #ffffff;
}

.error-message {
  color: #dc3545;
  font-size: 0.875rem;
  text-align: center;
}

/* 반응형 */
@media (max-width: 768px) {
  .login-container {
    padding: 15px;
  }

  .login-title {
    font-size: 1.5rem;
  }

  .form-group label {
    font-size: 0.9rem;
  }

  .form-group input {
    font-size: 0.9rem;
  }

  .login-button {
    font-size: 0.9rem;
  }
}
</style>
