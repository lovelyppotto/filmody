<template>
    <div>
    <h1>Sign Up Page</h1>
    <form @submit.prevent="signUp">
        <label for="username">아이디 : </label>
        <input type="text" id="username" v-model.trim="username"><br>

        <label for="password1">비밀번호 : </label>
        <input type="password" id="password1" v-model.trim="password1"><br>

        <label for="password2">비밀번호 확인 : </label>
        <input type="password" id="password2" v-model.trim="password2">

        <div>
            <label for="nickname">닉네임 : </label>
            <input type="text" id="nickname" v-model.trim="nickname">
        </div>
        <div>
            <label for="email">이메일 : </label>
            <input type="text" id="email" v-model.trim="email">
        </div>
        <input type="submit" value="SignUp">
    </form>
    </div>
</template>

<script setup>
    import { useMovieStore } from '@/stores/movie';
    import { ref } from 'vue'
    const store = useMovieStore()

    const username = ref(null)
    const password1 = ref(null)
    const password2 = ref(null)
    const nickname = ref(null)
    const email = ref(null)

    const signUp = function () {
    const payload = {
        username: username.value,
        password1: password1.value,
        password2: password2.value,
        nickname: nickname.value,
        email: email.value
    }
    store.signUp(payload)
    }
</script>

<style scoped>

</style>