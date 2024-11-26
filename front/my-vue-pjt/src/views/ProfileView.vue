<template>
  <div class="profile-image-section">
    <h1 class="profile-title">Profile Update</h1>
    <div class="image-wrapper">
      <label>
      <img
        :key="userInfo.profile_image"
        :src="previewImage || `${userInfo.profile_image}`"
        alt=""
        class="profile-preview"
      />
      <input
        type="file"
        ref="fileInput"
        @change.stop="handleImageUpload"
        accept="image/*"
        class="hidden-input"
      />
      <br>
      <button 
        class="camera-button"
        @click.prevent="$refs.fileInput.click()"
      >
        <i class="fas fa-camera"></i>
      </button>
    </label>
    </div>
    <button
      v-if="userInfo.profile_image && !userInfo.profile_image.includes('default.png')"
      @click.prevent="deleteProfileImage"
      class="image-delete-button"
    >
      이미지 삭제
    </button>
  </div>

  <form @submit.prevent="updateProfile" class="profile-form">
    <div class="form-group">
      <label for="username">아이디</label>
      <input 
        type="text" 
        id="username" 
        v-model="userInfo.username" 
        disabled
      />
    </div>

    <div class="form-group">
      <label for="current_password">현재 비밀번호</label>
      <input 
        type="password" 
        id="current_password" 
        v-model="passwords.current_password"
      />
    </div>

    <div class="form-group">
      <label for="new_password1">새 비밀번호</label>
      <input 
        type="password" 
        id="new_password1" 
        v-model="passwords.new_password1"
        @input="validatePassword"
      />
      <p v-if="!isPasswordValid && passwords.new_password1" class="error-message">
        비밀번호는 특수문자(@,!,^,_)/숫자/영어를 모두 포함하여 8자 이상이어야 합니다.
      </p>
    </div>

    <div class="form-group">
      <label for="new_password2">새 비밀번호 확인</label>
      <input 
        type="password" 
        id="new_password2" 
        v-model="passwords.new_password2"
        @input="validatePasswordMatch"
      />
      <p v-if="!isPasswordMatch && passwords.new_password2" class="error-message">
        비밀번호가 일치하지 않습니다.
      </p>
    </div>

    <div class="form-group">
      <label for="nickname">닉네임</label>
      <input 
        type="text" 
        id="nickname" 
        v-model="userInfo.nickname"
        @input="validateNickname"
      />
      <p v-if="!isNicknameValid && userInfo.nickname" class="error-message">
        닉네임은 10글자를 초과할 수 없습니다.
      </p>
    </div>

    <div class="form-group">
      <label for="email">이메일</label>
      <input 
        type="email" 
        id="email" 
        v-model="userInfo.email"
        @input="validateEmail"
      />
      <p v-if="!isEmailValid && userInfo.email" class="error-message">
        유효한 이메일 주소를 입력해주세요.
      </p>
    </div>

    <div class="form-group">
      <div class="checkbox-container">
        <label class="checkbox-label">
          리뷰 가리기
          <input
            type="checkbox"
            v-model="userInfo.show_reviews"
            class="checkbox-input"
          />
        </label>
        <div class="help-button-container">
          <button 
            class="help-button"
            @click.prevent="toggleHelpPopover"
            aria-label="리뷰 가리기 설명"
            ref="helpButton"
          >
            ?
          </button>
          <!-- 팝오버 -->
          <div 
            v-if="showHelpPopover" 
            class="help-popover"
            ref="helpPopover"
          >
            <div class="help-popover-content">
              <h4>리뷰 가리기 기능이란 <i class="fa-solid fa-question fa-xs"></i></h4>
              <p>활성화시 작성된 리뷰를 자동으로 가리게 됩니다. 언제든 '리뷰 확인하기' 버튼을 눌러 내용을 확인할 수 있습니다!</p>
              <button 
                class="help-popover-close"
                @click="showHelpPopover = false"
              >
                닫기
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <button 
      type="submit" 
      class="profile-button"
      :class="{ 'profile-button-disabled': !isFormValid }"
      :disabled="!isFormValid"
    >
      변경사항 저장
    </button>
  </form>
  <button @click="showDeleteModal = true" class="delete-button">회원 탈퇴</button>

  <div v-if="showDeleteModal" class="modal">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">회원 탈퇴</h5>
          <button type="button" class="btn-close" @click="showDeleteModal = false">&times;</button>
        </div>
        <div class="modal-body">
          <p>회원 탈퇴를 하시려면 비밀번호를 입력해주세요.<br>비밀번호 입력 후 탈퇴 버튼 선택 시, 계정은 삭제되며 복구되지 않습니다.</p>
          <input 
            type="password" 
            v-model="deletePassword" 
            placeholder="비밀번호를 입력해주세요"
          >
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="showDeleteModal = false">취소</button>
          <button type="button" class="btn btn-danger" @click="deleteAccount">탈퇴</button>
        </div>
      </div>
    </div>
  </div>

  
</template>

<script setup>
import { useAuthStore } from '@/stores/auth';
import axios from 'axios';
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router'

const router = useRouter()
const store = useAuthStore()
const userInfo = ref({
  username: '',
  nickname: '',
  email: '',
  show_reviews: false,
  profile_image: '',
})
const previewImage = ref('')
const passwords = ref({
  current_password: '',
  new_password1: '', 
  new_password2: '', 
})
const deletePassword = ref(null)
const showDeleteModal = ref(false)

// 도움말 모달 상태
const showHelpPopover = ref(false)
const helpButton = ref(null)
const helpPopover = ref(null)

// 유효성 검사 상태
const isPasswordValid = ref(true)
const isPasswordMatch = ref(true)
const isNicknameValid = ref(true)
const isEmailValid = ref(true)

// 비밀번호 유효성 검사
const validatePassword = () => {
  if (!passwords.value.new_password1) {
    isPasswordValid.value = true
    return
  }

  const passwordRegex = /^(?=.*[@!^_])(?=.*[0-9])(?=.*[a-zA-Z]).{8,}$/
  isPasswordValid.value = passwordRegex.test(passwords.value.new_password1)
  validatePasswordMatch()
}

// 비밀번호 일치 검사
const validatePasswordMatch = () => {
  if (!passwords.value.new_password2) {
    isPasswordMatch.value = true
    return
  }
  isPasswordMatch.value = passwords.value.new_password1 === passwords.value.new_password2
}

// 닉네임 유효성 검사
const validateNickname = () => {
  if (!userInfo.value.nickname) {
    isNicknameValid.value = true
    return
  }
  isNicknameValid.value = userInfo.value.nickname.length <= 10
}

// 이메일 유효성 검사
const validateEmail = () => {
  if (!userInfo.value.email) {
    isEmailValid.value = true
    return
  }
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  isEmailValid.value = emailRegex.test(userInfo.value.email)
}

// 폼 전체 유효성 검사
const isFormValid = computed(() => {
  // 비밀번호 변경이 있는 경우
  if (passwords.value.new_password1 || passwords.value.new_password2 || passwords.value.current_password) {
    return userInfo.value.nickname &&
           userInfo.value.email &&
           passwords.value.current_password &&
           isPasswordValid.value &&
           isPasswordMatch.value &&
           isNicknameValid.value &&
           isEmailValid.value
  }
  
  // 비밀번호 변경이 없는 경우
  return userInfo.value.nickname &&
         userInfo.value.email &&
         isNicknameValid.value &&
         isEmailValid.value
})

// 정보 수정
const updateProfile = () => {
  const storedToken = store.token

  if(passwords.value.current_password && !passwords.value.new_password1){
    alert('새 비밀번호를 입력해주세요.')
    return
  }
  // 비번 변경 있을 때
  if (passwords.value.new_password1) {
    if (!passwords.value.current_password && (passwords.value.new_password1 || passwords.value.new_password2)) {
      alert('현재 비밀번호를 입력해주세요.')
      return
    }
    if (!passwords.value.current_password) {
      alert('현재 비밀번호를 입력해주세요.')
      return
    }
    if(!passwords.value.new_password2) {
      alert('새 비밀번호 확인을 입력해주세요.')
      return
    }
    if (passwords.value.new_password1 !== passwords.value.new_password2) {
      alert ('새 비밀번호가 일치하지 않습니다.')
      return
    }
    axios({
      method: 'post',
      url: `${store.BASE_URL}/accounts/password/change/`,
      headers: {
        Authorization: `Token ${storedToken}`,
        'Content-Type': 'application/json'
      },
      data: {
        old_password: passwords.value.current_password,
        new_password1: passwords.value.new_password1,
        new_password2: passwords.value.new_password2
      }
    })
    .then(() => {
      alert('비밀번호가 성공적으로 변경되었습니다.')
      passwords.value.current_password=''
      passwords.value.new_password1=''
      passwords.value.new_password2=''
      updateUserInfo()
    })
    .catch((error) => {
      console.error('비밀번호 변경 실패:', error)
      console.log('에러 응답 데이터:', error.response?.data)
    })
  } else {
    updateUserInfo()
  }
}

// 프로필 정보 수정
const updateUserInfo = () => {
  const storedToken = store.token

  // 필수 필드 검증
  if (!userInfo.value.nickname || !userInfo.value.email) {
    alert('닉네임과 이메일은 필수 입력사항입니다.')
    return
  }

  axios({
    method: 'put',  
    url: `${store.BASE_URL}/accounts/user/`,
    headers: {
      Authorization: `Token ${storedToken}`,
      'Content-Type': 'application/json'
    },
    data: {
      nickname: userInfo.value.nickname,
      email: userInfo.value.email,
      show_reviews: userInfo.value.show_reviews,
    }
  })
  .then((response) => {
    console.log('프로필 업데이트 성공')
    alert('프로필이 성공적으로 업데이트되었습니다.')
    userInfo.value = response.data
  })
  .catch((error) => {
    alert('프로필 업데이트에 실패했습니다.')
    console.error('프로필 업데이트 실패:', error)
  })
}

// 사용자 정보 가져오기
onMounted(() => {
  const storedToken = store.token
  axios({
    method: 'get',
    url:`${store.BASE_URL}/accounts/user/`,
    headers: {
      Authorization: `Token ${storedToken}`
    }
  })
  .then((response) => {
    console.log(response.data)
    userInfo.value = response.data
    previewImage.value = response.data.profile_image.includes('default.png') ? 
      `${store.BASE_URL}/static/images/default.png` : response.data.profile_image
  })
  .catch((error) => {
    console.log('사용자 정보 가져오기 실패 : ',error)
  })
})

// 회원 탈퇴
const deleteAccount = async () => {
  try {
    const storedToken = store.token
    
    // 비밀번호 검증
    if(!deletePassword.value) {
      alert('비밀번호를 입력해주세요.')
      return
    }

    // 재확인 절차 추가
    if(!confirm('정말 탈퇴하시겠습니까? 이 작업은 되돌릴 수 없습니다.')) {
      return
    }
    
    // 서버로 전송할 데이터 형식 변경
    const response = await axios({
      method: 'delete',
      url: `${store.BASE_URL}/accounts/delete/`,
      headers: {
        Authorization: `Token ${storedToken}`,
        'Content-Type': 'application/json'
      },
      data: {
        current_password: deletePassword.value  // 키 이름을 current_password로 변경
      }
    })

    if (response.status === 200 || response.status === 204) {
      alert('회원 탈퇴가 완료되었습니다.')
      await store.logOut() // await 추가
      router.push('/') // 경로를 직접 지정
    }
  } catch (error) {
    console.error('회원 탈퇴 실패:', error)
    if (error.response?.status === 400) {
      alert('비밀번호가 올바르지 않습니다.')
    } else {
      alert('회원 탈퇴에 실패했습니다. 다시 시도해주세요.')
    }
  } finally {
    showDeleteModal.value = false
    deletePassword.value = null
  }
}

// 프로필 이미지 변경
const handleImageUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    if (file.size > 5 * 1024 * 1024) {
      alert('파일 크기는 5MB를 초과할 수 없습니다.')
      return
    }
    if (!file.type.startsWith('image/')) {
      alert('이미지 파일만 업로드 가능합니다.')
      return
    }

    const formData = new FormData()
    formData.append('profile_image', file)
    
    const reader = new FileReader()
    reader.onload = (e) => {
      previewImage.value = e.target.result
    }
    reader.readAsDataURL(file)

      axios({
          method: 'patch',
          url: `${store.BASE_URL}/accounts/user/`,
          headers: {
              Authorization: `Token ${store.token}`,
          },
          data: formData
      })
      .then((response) => {
          userInfo.value.profile_image = response.data.profile_image;
          console.log('프로필 사진 업데이트')
      })
      .catch((error) => {
          console.error('프로필 업데이트 실패 : ', error);
          if (error.response) {
      // 서버 응답이 있는 경우
      console.log('에러 응답 데이터:', error.response.data);
      // 에러 메시지 표시
  } else {
      // 서버 응답이 없는 경우
      alert('프로필 업데이트에 실패했습니다. 다시 시도해주세요.');
  }
      // 업로드 실패시 미리보기 초기화
      previewImage.value = null
      })

  }

}

// 프로필 사진 삭제
const deleteProfileImage = () => {
  const storedToken = store.token
  if(confirm('프로필 사진을 삭제하시겠습니까?')) {
      axios({
          method:'delete',
          url: `${store.BASE_URL}/accounts/profile-image`,
          headers: {
              Authorization: `Token ${storedToken}`
          }
      })
      .then((response) => {
          userInfo.value.profile_image = response.data.profile_image
          previewImage.value = null
      })
      .catch((error) => {
          console.error('프로필 사진 삭제 실패 : ', error);
      })
  }
}

// 팝오버 토글
const toggleHelpPopover = () => {
  showHelpPopover.value = !showHelpPopover.value
}

// 외부 클릭 감지
const handleClickOutside = (event) => {
  if (showHelpPopover.value && 
      helpPopover.value && 
      helpButton.value && 
      !helpPopover.value.contains(event.target) &&
      !helpButton.value.contains(event.target)) {
    showHelpPopover.value = false
  }
}

// 이벤트 리스너 등록 및 해제
onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.profile-title{
  font-size: 2rem;
  text-align: center;
  margin: 50px 0 40px 0;
  color: #374c72;
}

.profile-container {
  max-width: 700px;
  margin: 50px auto;
  padding: 20px;
  background: #ffffff;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(255, 255, 255, 0.1);
  font-family: 'Arial', sans-serif;
}

.profile-title {
  font-size: 2rem;
  text-align: center;
  margin: 30px 0 40px 0;
  color: #374c72;
}

.profile-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 20px;
  width: 100%;  /* 추가 */
  max-width: 700px;  /* 추가 */
  margin-left: auto;  /* 추가 - 중앙 정렬 */
  margin-right: auto;  /* 추가 - 중앙 정렬 */
}

.form-group label {
  font-size: 1rem;
  font-weight: 500;
  margin-bottom: 5px;
  color: #48505e;
}

.form-group input {
  height: 50px;
  padding: 10px;
  border: none;  /* 변경 */
  border-bottom: 1px solid #a8aeb5;  /* 변경 */
  font-size: 1rem;
  transition: border-color 0.3s ease;
  width: 100%;  /* 추가 */
}

.form-group input:focus {
  outline: none;
  border-color: #b4c4dc;
  box-shadow: 0 0 2px rgba(110, 138, 181, 0.3);
}

/* 체크박스 스타일 */
.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.checkbox-input {
  width: 16px;
  height: 16px;
  margin: 0;
}

/* 이미지 섹션 스타일 */
.image-delete-button {
  padding: 4px 8px;  /* 더 작은 패딩 */
  font-size: 0.8rem;  /* 더 작은 글씨 */
  color: #dc3545;
  border-color: #dc3545;
  position: absolute;  /* 추가 */
  right: 0;  /* 추가 */
  top: 0;  /* 추가 */
  margin: 0;  /* 추가 */
}

.profile-image-section {
  position: relative;  /* 추가 */
  width: 100%;  /* 추가 */
  max-width: 500px;  /* 추가 - form-group과 같은 너비 */
  margin: 120px auto 30px;  /* 중앙 정렬 및 아래 여백 */
}

.image-wrapper {
  position: relative;
  display: flex;
  justify-content: center;
  width: 100%;
}

.hidden-input {
  display: none;
}

.profile-preview {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
}

/* 버튼 스타일 */
button {
  padding: 10px 20px;
  background-color: #ffffff;
  color: #42464b;
  border: 1px solid #42464b;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

button:hover {
  background-color: #42464b;
  color: #ffffff;
}

.profile-button {
  width: 100%;
  margin-top: 20px;
}

.delete-button {
  width: 100%;
  max-width: 500px;
  margin: 5px auto 0;
  display: block;  /* 중앙 정렬을 위해 추가 */
  color: #dc3545;
  border-color: #dc3545;
  padding: 8px 16px;  /* profile-button과 동일한 패딩 */
  font-size: 0.9rem;  /* profile-button과 동일한 글자 크기 */
}

.delete-button:hover {
  background-color: #dc3545;
  color: #ffffff;
}

.image-delete-button {
  padding: 4px 8px;
  font-size: 0.8rem;
  color: #dc3545;
  border-color: #dc3545;
  position: absolute;
  right: 0;
  top: 160px;
}

.image-delete-button:hover {
  background-color: #dc3545;
  color: #ffffff;
}

/* 버튼 컨테이너 */
.button-container {
  width: 100%;
  max-width: 500px;
  margin: 20px auto 0;
}

/* 버튼 스타일 수정 */
.profile-button{
  width: 100%;
  padding: 8px 16px;
  font-size: 0.9rem;
  margin-top: 0;
}


.profile-form {
  position: relative;  /* 버튼들의 기준점 */
  width: 100%;
  max-width: 500px;
  margin: 0 auto;

}

/* 각 버튼의 너비를 동일하게 설정 */


.image-controls {
  position: absolute;
  bottom: 0;
  right: 0;
  display: flex;
  gap: 8px;
}

.camera-button {
  width: 36px;
  height: 36px;
  padding: 0;
  border-radius: 50%;
  background-color: #ffffff;
  border: 1px solid #42464b;
  display: flex;
  align-items: center;
  justify-content: center;
}

.camera-button i {
  font-size: 16px;
}

.camera-button:hover {
  background-color: #42464b;
  color: #ffffff;
}

.image-controls {
  position: absolute;
  bottom: 10px;
  right: 10px;
  display: flex;
  gap: 8px;
}

.camera-button {
  position: absolute;
  bottom: 10px;
  right: calc(50% - 85px);  /* 이미지 크기의 절반(75px) + 약간의 여백(10px) */
  width: 36px;
  height: 36px;
  padding: 0;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.9);
  border: 1px solid #42464b;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.camera-button:hover {
  background-color: #42464b;
  color: #ffffff;
}


/* 체크박스 스타일 */
.form-group .checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  font-size: 1rem;
  color: #48505e;
}

.form-group .checkbox-label input[type="checkbox"] {
  width: 14px !important;  /* !important 추가 */
  height: 14px !important;  /* !important 추가 */
  min-width: 14px;  /* 추가 */
  min-height: 14px;  /* 추가 */
  margin: 0;
  cursor: pointer;
  padding: 0;
}

.form-buttons-wrapper {
  width: 100%;
  max-width: 500px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  gap: 10px;
}

.error-message{
  color: #dc3545;
  font-size: 14px;
  margin: 5px 0px 0px 0px;
}



.delete-button {
  color: #dc3545;
  border-color: #dc3545;
  margin-bottom: 60px;
}

/* 모달 스타일링 */
.modal {
  display: flex;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-dialog {
  position: relative;
  width: 100%;
  max-width: 600px;
  margin: 1.75rem auto;
  text-align: center;
}

.modal-content {
  position: relative;
  background-color: #fff;
  border-radius: 0.3rem;
  padding: 1rem;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  border-bottom: 1px solid #dee2e6;
}

.modal-title {
  margin: 0;
  font-size: 1.25rem;
}

.modal-body {
  padding: 1rem;
}

.modal-body input {
  width: 100%;
  padding: 0.5rem;
  margin-top: 0.5rem;
  border: 1px solid #ced4da;
  border-radius: 0.25rem;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  padding: 1rem;
  border-top: 1px solid #dee2e6;
}

.btn-close {
  padding: 0.5rem;
  background: transparent;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
}

/* 모달 버튼 스타일링 */
.btn {
  padding: 0.375rem 0.75rem;
  border-radius: 0.25rem;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.15s ease-in-out;
}

.btn-danger {
  color: #fff;
  background-color: #dc3545;
  border: 1px solid #dc3545;
}

.btn-danger:hover {
  background-color: #c82333;
  border-color: #bd2130;
}

.btn-secondary {
  color: #fff;
  background-color: #6c757d;
  border: 1px solid #6c757d;
}

.btn-secondary:hover {
  background-color: #5a6268;
  border-color: #545b62;
}

/* 체크박스 컨테이너 */
.checkbox-container {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* 도움말 버튼 */
.help-button {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 1px solid #666;
  background: white;
  color: #666;
  font-size: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  padding: 0;
  margin: 0;
}

.help-button:hover {
  background: #f0f0f0;
  color: #333;
}

/* 도움말 버튼 컨테이너 */
.help-button-container {
  position: relative;
  display: inline-block;
}

/* 도움말 버튼 */
.help-button {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 1px solid #666;
  background: white;
  color: #666;
  font-size: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  padding: 0;
  margin: 0;
}

.help-button:hover {
  background: #f0f0f0;
  color: #333;
}

/* 팝오버 스타일 */
.help-popover {
  position: absolute;
  left: calc(100% + 10px); /* 버튼 오른쪽에 10px 간격 */
  top: 50%;
  transform: translateY(-50%);
  background: white;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  width: 250px;
  z-index: 1000;
}

.help-popover::before {
  content: '';
  position: absolute;
  left: -6px;
  top: 50%;
  transform: translateY(-50%);
  width: 0;
  height: 0;
  border-top: 6px solid transparent;
  border-bottom: 6px solid transparent;
  border-right: 6px solid white;
}

.help-popover-content {
  text-align: left;
}

.help-popover-content h4 {
  margin: 0 0 8px 0;
  color: #333;
  font-size: 14px;
}

.help-popover-content p {
  margin: 0 0 12px 0;
  color: #666;
  font-size: 13px;
  line-height: 1.4;
}

.help-popover-close {
  padding: 4px 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: white;
  color: #666;
  cursor: pointer;
  font-size: 12px;
  display: block;
  margin-left: auto;
}

.help-popover-close:hover {
  background: #f0f0f0;
  color: #333;
}

@media (max-width: 768px) {
  .profile-container {
    padding: 15px;
  }

  .profile-title {
    font-size: 1.5rem;
  }

  .form-group label {
    font-size: 0.9rem;
  }

  .form-group input {
    font-size: 0.9rem;
  }

  button {
    font-size: 0.9rem;
  }
}
</style>