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
        <input 
          type="password" 
          id="password1" 
          v-model.trim="password1" 
          @input="validatePassword"
          placeholder="비밀번호를 입력하세요"
        >
        <p v-if="!isPasswordValid && password1" class="error-message">
          비밀번호는 특수문자(@,!,^,_)/숫자/영어를 모두 포함하여 8자 이상이어야 합니다.
        </p>
      </div>

      <div class="form-group">
        <label for="password2">비밀번호 확인</label>
        <input 
          type="password" 
          id="password2" 
          v-model.trim="password2"
          @input="validatePasswordMatch"
          placeholder="비밀번호를 다시 입력하세요"
        >
        <p v-if="!isPasswordMatch && password2" class="error-message">
          비밀번호가 일치하지 않습니다.
        </p>
      </div>

      <div class="form-group">
        <label for="nickname">닉네임</label>
        <input 
          type="text" 
          id="nickname" 
          v-model.trim="nickname" 
          @input="validateNickname"
          placeholder="닉네임을 입력하세요"
        >
        <p v-if="!isNicknameValid && nickname" class="error-message">
          닉네임은 10글자를 초과할 수 없습니다.
        </p>
      </div>

      <div class="form-group">
        <label for="email">이메일</label>
        <input 
          type="text" 
          id="email" 
          v-model.trim="email"
          @input="validateEmail"
          placeholder="이메일 주소를 입력하세요"
        >
        <p v-if="!isEmailValid && email" class="error-message">
          유효한 이메일 주소를 입력해주세요.
        </p>
      </div>

      <p>프로필 이미지는 기본 이미지로 설정됩니다. 추후 프로필 페이지에서 변경해 주세요.</p>

      <button 
        type="submit" 
        class="signup-button"
        :class="{ 'signup-button-disabled': !isFormValid }"
        :disabled="!isFormValid"
      >
        회원가입
      </button>
    </form>

    <SignupModal 
      :is-visible="showModal"
      @confirm="handleModalConfirm"
      @close="handleModalClose"
    />
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth';
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import SignupModal from '@/components/SignupModal.vue';

const store = useAuthStore();
const router = useRouter();
const showModal = ref(false);

const username = ref(null);
const password1 = ref(null);
const password2 = ref(null);
const nickname = ref(null);
const email = ref(null);

const isPasswordValid = ref(true);
const isPasswordMatch = ref(true);
const isNicknameValid = ref(true);
const isEmailValid = ref(true);

// 비밀번호 유효성 검사
const validatePassword = () => {
  if (!password1.value) {
    isPasswordValid.value = true;
    return;
  }

  const passwordRegex = /^(?=.*[@!^_])(?=.*[0-9])(?=.*[a-zA-Z]).{8,}$/;
  isPasswordValid.value = passwordRegex.test(password1.value);
  validatePasswordMatch();
};

// 비밀번호 일치 검사
const validatePasswordMatch = () => {
  if (!password2.value) {
    isPasswordMatch.value = true;
    return;
  }
  isPasswordMatch.value = password1.value === password2.value;
};

// 닉네임 유효성 검사
const validateNickname = () => {
  if (!nickname.value) {
    isNicknameValid.value = true;
    return;
  }
  isNicknameValid.value = nickname.value.length <= 10;
};

// 이메일 유효성 검사
const validateEmail = () => {
  if (!email.value) {
    isEmailValid.value = true;
    return;
  }
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  isEmailValid.value = emailRegex.test(email.value);
};

// 폼 전체 유효성 검사
const isFormValid = computed(() => {
  return username.value && 
         password1.value && 
         password2.value && 
         nickname.value && 
         email.value && 
         isPasswordValid.value && 
         isPasswordMatch.value &&
         isNicknameValid.value &&
         isEmailValid.value;
});

const handleModalConfirm = async () => {
  try {
    // 저장된 로그인 정보로 로그인 시도
    if (loginCredentials.value) {
      await store.logIn(loginCredentials.value);
    }
    showModal.value = false;
    router.push({ name: 'home' });
  } catch (error) {
    console.error('로그인 중 에러 발생:', error);
    // 에러 처리
  }
};

const handleModalClose = () => {
  handleModalConfirm(); // 동일한 로직 실행
};

// 로그인 정보를 저장할 ref
const loginCredentials = ref(null);

const signUp = async function () {
  if (!isFormValid.value) return;
  
  const payload = {
    username: username.value,
    password1: password1.value,
    password2: password2.value,
    nickname: nickname.value,
    email: email.value,
  };

  try {
    // 회원가입 시도
    const result = await store.signUp(payload);
    
    // 로그인을 위한 정보 저장
    loginCredentials.value = result.credentials;
    
    // 모달 표시
    showModal.value = true;
  } catch (error) {
    console.error('회원가입 중 에러 발생:', error);
    // 에러 처리
  }
};
</script>

<style scoped>
.error-message {
  color: #dc3545;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

.signup-button {
  width: 100%;
  padding: 0.75rem;
  background-color: #374c72;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.signup-button:hover:not(:disabled) {
  background-color: #374c72;
}

.signup-button-disabled {
  background-color: #e8e3e3;
  cursor: not-allowed;
  opacity: 0.7;
}

  p {
    display: flex;
    flex-direction: column;
    text-align: center;
    color: #3e5275;
  }

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
    margin: 30px 0 40px 0;
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

  .error-message {
  color: red;
  font-size: 0.875rem;
  margin-top: 0.25rem;
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
  