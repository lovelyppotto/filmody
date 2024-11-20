<template>
    <div>
        <h1>홈입니다</h1>
    </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth';
import { onMounted } from 'vue';
const store = useAuthStore()

onMounted(() => {
    console.log(store.token);
    
})
</script>

<style scoped>

</style>