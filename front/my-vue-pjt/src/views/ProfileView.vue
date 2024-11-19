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
    </div>
</template>

<script setup>
import { useMovieStore } from '@/stores/movie';
import axios from 'axios';
import { ref, onMounted } from 'vue';

const store = useMovieStore()
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


// 정보 수정
const updateProfile = () =>{
    const storedToken = store.token
    // 비밀번호, 비밀번호 확인이 다를 때
    if (passwords.value.new_password1 !== passwords.value.new_password2) {
        alert('새 비밀번호가 일치하지 않습니다.')
        return
    }
    // 비번 변경 있을 때
    if (passwords.value.new_password1) {
        axios({
            method:'post',
            url: `${store.BASE_URL}/accounts/password/change/`,
            headers: {
                Authorization: `Token ${storedToken}`
            },
            data: {
                current_password : passwords.value.current_password,
                new_password1 : passwords.value.new_password1,
                new_password2 : passwords.value.new_password2,
            }
        })
        .then(() => {
            // 비번 변경 성공 후 프로필 정보 업데이트
            axios({
                method: 'put',  
                url: `${store.BASE_URL}/accounts/user/`,
                headers: {
                    Authorization: `Token ${storedToken}`
                },
                data: {
                    nickname: userInfo.value.nickname,
                    email: userInfo.value.email,
                    show_reviews: userInfo.value.show_reviews
                }
            })
            .then(() => {
                alert('프로필이 성공적으로 업데이트되었습니다.')
            })
            .catch((error) => {
                alert('프로필 업데이트에 실패했습니다.')
                console.error('프로필 업데이트 실패:', error)
            })
        })
        .catch((error) => {
            alert('비밀번호 변경에 실패했습니다.')
            console.error('비밀번호 변경 실패:', error)
        })
    } else {
        // 비번 변경 없이 다른 정보만 수정
        axios({
            method:'put',
            url: `${store.BASE_URL}/accounts/user/`,
            headers: {
                    Authorization: `Token ${storedToken}`
                },
            data: {
                    nickname: userInfo.value.nickname,
                    email: userInfo.value.email
                }
        })
        .then(() => {
                alert('프로필이 성공적으로 업데이트되었습니다.')
        })
        .catch((error) => {
            alert('프로필 업데이트에 실패했습니다.')
            console.error('프로필 업데이트 실패:', error)
        })
    }
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
</script>

<style scoped>

</style>