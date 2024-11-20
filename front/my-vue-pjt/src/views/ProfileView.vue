<template>
    <div>
        <h1>Profile</h1>
        <form @submit.prevent="updateProfile">
            <div>
                <label for="username">
                    아이디 :
                    <input type="text" id="username" v-model="userInfo.username" disabled>
                </label>
            </div>
            <div>
                <label for="current_password">
                    현재 비밀번호 :
                    <input type="password" id="current_password" v-model="passwords.current_password">
                </label>
            </div>
            <div>
                <label for="new_password1">
                    새 비밀번호 :
                    <input type="password" id="new_password1" v-model="passwords.new_password1">
                </label>
            </div>
            <div>
                <label for="new_password2">
                    새 비밀번호 확인 :
                    <input type="password" id="new_password2" v-model="passwords.new_password2">
                </label>
            </div>
            <div>
                <label for="">
                    닉네임 :
                    <input type="text" v-model="userInfo.nickname">
                </label>
            </div>
            <div>
                <label for="">
                    이메일 :
                    <input type="text" v-model="userInfo.email">
                </label>
            </div>
            <div>
                <label for="">
                    리뷰 보기 :
                    <input type="checkbox" v-model="userInfo.show_reviews">
                </label>
            </div>
            <button type="submit">Save Changes</button>
        </form>

        <!-- 회원 탈퇴 -->
        <button @click="showDeleteModal=true">회원 탈퇴</button>
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
    show_reviews: false
})
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
            show_reviews: userInfo.value.show_reviews
        }
    })
    .then((response) => {
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
    .then((res) => {
        userInfo.value = res.data
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
</script>

<style scoped>
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

input[type="password"] {
    width: 100%;
    padding: 0.375rem 0.75rem;
    margin: 0.5rem 0;
    border: 1px solid #ced4da;
    border-radius: 0.25rem;
}
</style>