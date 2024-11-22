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
