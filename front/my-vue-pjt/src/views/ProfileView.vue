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
        />
      </div>

      <div class="form-group">
        <label for="new_password2">새 비밀번호 확인</label>
        <input 
          type="password" 
          id="new_password2" 
          v-model="passwords.new_password2"
        />
      </div>

      <div class="form-group">
        <label for="nickname">닉네임</label>
        <input 
          type="text" 
          id="nickname" 
          v-model="userInfo.nickname"
        />
      </div>

      <div class="form-group">
        <label for="email">이메일</label>
        <input 
          type="email" 
          id="email" 
          v-model="userInfo.email"
        />
      </div>

      <div class="form-group">
        <label class="checkbox-label">
          리뷰 가리기
          <input
            type="checkbox"
            v-model="userInfo.show_reviews"
            class="checkbox-input"
          />
        </label>
      </div>
        <button type="submit" class="profile-button">변경사항 저장</button>
    </form>
      <button @click="showDeleteModal = true" class="delete-button">회원 탈퇴</button>

      <div v-if="showDeleteModal" class="modal" tabindex="-1">
          <div class="modal-dialog">
              <div class="modal-content">
              <div class="modal-header">
                  <h5 class="modal-title">회원 탈퇴</h5>
                  <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" @click="showDeleteModal=false"></button>
              </div>
              <div class="modal-body">
                  <p>회원 탈퇴를 하시려면 비밀번호를 입력해주세요. 비밀번호 입력 후 탈퇴 버튼 선택 시, 
                      계정은 삭제되며 복구되지 않습니다.</p>
                  <input type="password" v-model="deletePassword" placeholder="비밀번호를 입력해주세요.">
              </div>
              <div class="modal-footer">
                  <button type="button" class="btn btn-danger" @click="deleteAccount">탈퇴</button>
                  <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="showDeleteModal=false">취소</button>
              </div>
              </div>
          </div>
      </div>

</template>

<script setup>
import { useAuthStore } from '@/stores/auth';
import axios from 'axios';
import { ref, onMounted } from 'vue';

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
          // profile_image: userInfo.value.profile_image
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
      console.log(response.data)
      userInfo.value = response.data
      // 초기 프로필 이미지 설정

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



.delete-button {
  color: #dc3545;
  border-color: #dc3545;
  margin-bottom: 60px;
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