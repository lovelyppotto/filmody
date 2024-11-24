<template>
  <div class="profile-container font-nanum">
    <h1 class="profile-title">Profile</h1>
    
    <ProfileImage
      :model-value="userInfo.profile_image"
      @update="handleImageUpload"
      @delete="deleteProfileImage"
    />

      <!-- 사용자 정보 폼 -->
    <form @submit.prevent="updateProfile" class="profile-form">
      <!-- 나머지 폼 그룹들... -->
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
        <label for="current_password" class="label">현재 비밀번호</label>
        <input
          type="password"
          id="current_password"
          v-model="passwords.current_password"
          class="input-field"
        />
      </div>

      <div class="form-group">
        <label for="new_password1" class="label">새 비밀번호</label>
        <input
          type="password"
          id="new_password1"
          v-model="passwords.new_password1"
          class="input-field"
        />
      </div>

      <div class="form-group">
        <label for="new_password2" class="label">새 비밀번호 확인</label>
        <input
          type="password"
          id="new_password2"
          v-model="passwords.new_password2"
          class="input-field"
        />
      </div>

      <div class="form-group">
        <label class="label">닉네임</label>
        <input
          type="text"
          v-model="userInfo.nickname"
          class="input-field"
        />
      </div>

      <div class="form-group">
        <label class="label">이메일</label>
        <input
          type="email"
          v-model="userInfo.email"
          class="input-field"
        />
      </div>

      <div class="form-group checkbox-group">
          <input
            type="checkbox"
            v-model="userInfo.show_reviews"
            class="checkbox-input"
          />
      </div>

      <button type="submit" class="primary-button">회원정보 수정</button>
    </form>

    <button @click="showDeleteModal = true" class="delete-account-button">
      회원 탈퇴
    </button>
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
import ProfileImage from '@/components/ProfileImage.vue';
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
  current_password : '',
  new_password1 : '', 
  new_password2 : '', 
})
const deletePassword = ref(null)
const showDeleteModal = ref(false)


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
          profile_image: userInfo.value.profile_image
      }
  })
  .then((response) => {
      console.log('프로필 업데이트 성공');
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
      // console.log(response.data)
      userInfo.value = response.data
      // 프로필 이미지가 default.png인 경우 static 경로 사용
      previewImage.value = response.data.profile_image.includes('default.png') ? 
          `${store.BASE_URL}/static/images/default.png` : response.data.profile_image
  })
  .catch((error) => {
      console.log('사용자 정보 가져오기 실패 : ',error);
  })
})

// 회원 탈퇴
const deleteAccount = () => {
  const storedToken = store.token
  if(!deletePassword.value) {
      alert('비밀번호를 입력해주세요.')
      return
  }
  
  axios({
      method: 'delete',
      url: `${store.BASE_URL}/accounts/delete/`,
      headers: {
          Authorization: `Token ${storedToken}`
      },
      data: {
          password: deletePassword.value // 서버에서 기존 비밀번호와 동일한 지 검증
      }
  })
  .then(() => {
      alert('회원 탈퇴가 완료되었습니다.')
      store.logOut()
  })
  .catch((error) => {
      console.error('회원 탈퇴 실패 : ',error)
      alert('회원 탈퇴에 실패했습니다. 다시 시도해주세요.')
  })
  .finally(() => {  // 요청 성공 여부와 상관없이 공통적으로 처리하는 작업
      showDeleteModal.value=false
      deletePassword.value = null
  })
  }

// 프로필 이미지 변경
const handleImageUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
      // 파일 크기 체크
      if (file.size > 5 * 1024 * 1024) { // 5MB
          alert('파일 크기는 5MB를 초과할 수 없습니다.')
          return
      }
      // 파일 타입 체크
      if (!file.type.startsWith('image/')) { // 5MB
          alert('이미지 파일만 업로드 가능합니다.')
          return
      }

      const formData = new FormData()
      formData.append('profile_image', file)

      
      // 프로필 이미지 미리보기
      const reader = new FileReader();
      reader.onload = (e) => {
          previewImage.value = e.target.result

      };
      reader.readAsDataURL(file);

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
</script>

<style>

/* Reset styles for this component */
.profile-container {
  max-width: 600px;
  margin: 50px auto;
  padding: 20px;
  background: #ffffff;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(255, 255, 255, 0.1);
}

.profile-container .profile-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.profile-container .form-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 20px;
}

.profile-container .form-group label {
  font-size: 1rem;
  font-weight: 500;
  margin-bottom: 5px;
  color: #48505e;
}
/* 
.profile-container .form-group input {
  height: 50px;
  padding: 10px;
  border: none;
  border-bottom: 1px solid #ced4da;
  font-size: 1rem;
  background: transparent;
  width: 100%;
  box-sizing: border-box;
} */

.profile-container .form-group input:focus {
  outline: none;
  box-shadow: none;
}

.profile-container button {
  padding: 10px 20px;
  background-color: #ffffff;
  color: #42464b;
  border: 1px solid #42464b;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}
/* 컨테이너 */
.profile-container {
  max-width: 600px;
  margin: 50px auto;
  padding: 20px;
  background: #ffffff;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(255, 255, 255, 0.1);
}

/* 타이틀 */
.profile-title {
  font-size: 2rem;
  text-align: center;
  margin: 30px 0 40px 0;
  color: #374c72;
}

/* 폼 */
.profile-form {
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
  border: none;
  border-width: 0 0 1px;
  font-size: 1rem;
  /* transition: border-color 0.3s ease; */
}
.form-group input:focus {
  outline: none;  /* focus 시 테두리 제거 */
  border-bottom: 2px solid #b4c4dc;  /* focus 시 밑줄 강조 */
  box-shadow: none;  /* 그림자 효과 제거 */
}

.form-group input:disabled {
  background-color: transparent;
  border: none;
  border-bottom: 1px solid #ced4da;
  opacity: 0.7;
}

/* 이미지 관련 */
.profile-image-container {
  margin: 20px 0;
  text-align: center;
}

.profile-preview {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  margin: 10px 0;
  object-fit: cover;
}

/* 버튼 */
button {
  padding: 10px 20px;
  background-color: #ffffff;
  color: #42464b;
  border: 1px solid #42464b;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #42464b;
  border: 1px solid #42464b;
  color: #ffffff;
}

.delete-account-button {
  width: 100%;
  margin-top: 20px;
  color: #dc3545;
  border-color: #dc3545;
}

.delete-account-button:hover {
  background-color: #dc3545;
  color: #ffffff;
  border-color: #dc3545;
}

/* 체크박스 */
.checkbox-input {
  margin-right: 8px;
}

/* 모달 스타일 */
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
  border-radius: 5px;
  padding: 20px;
}

.profile-image-container::before {
  display: none;
}

.image-section {
  display: flex;
  justify-content: center;
  margin: 20px 0;
}

.image-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
}

.profile-preview {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
}

.image-controls {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.file-input {
  width: auto;
}

/* 이미지 섹션 관련 스타일 */
.form-group .image-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 20px 0;
  gap: 15px;
}

.profile-preview {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
}

.image-controls {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.profile-container .form-group input[type="text"],
.profile-container .form-group input[type="password"],
.profile-container .form-group input[type="email"] {
  height: 50px;
  padding: 10px;
  border: none;
  border-bottom: 1px solid #ced4da;
  font-size: 1rem;
  background: transparent;
  border-radius: 0;
}

/* focus 스타일도 같이 적용 */
.profile-container .form-group input[type="text"]:focus,
.profile-container .form-group input[type="password"]:focus,
.profile-container .form-group input[type="email"]:focus {
  outline: none;
  border-bottom: 2px solid #b4c4dc;
  box-shadow: none;
  border-radius: 0;
}

.profile-container .form-group input[type="checkbox"] {
  width: 16px;
  height: 16px;
  margin-right: 8px;
  cursor: pointer;
}

/* 체크박스 컨테이너 스타일 */
.profile-container .form-group.checkbox-group {
  flex-direction: row;
  align-items: center;
}

/* 체크박스 라벨 스타일 */
.profile-container .form-group.checkbox-group .checkbox-label {
  display: flex;
  align-items: center;
  font-size: 1rem;
  color: #48505e;
  cursor: pointer;
  margin: 0;
}


/* 반응형 */
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
  height: 50px;
  padding: 10px;
  border: none;  /* 모든 테두리 제거 */
  border-bottom: 1px solid #ced4da;  /* 밑줄만 추가 */
  font-size: 1rem;
  background: transparent;  /* 배경 투명하게 */
}


  button {
    font-size: 0.9rem;
  }
}
</style>