<template>
    <div class="container py-4">
        <div class="mb-4">
        <h2 class="text-2xl font-bold">좋아요한 영화</h2>
        <p class="text-gray-600">마음에 드는 영화를 모아보세요 :)</p>
        </div>
        <LibraryMovieList/>
    </div>
</template>

<script setup>
import LibraryMovieList from '@/components/LibraryMovieList.vue';

</script>

<style scoped>
.container .py-4 {
    padding-top: 1.5rem;
    padding-bottom: 1.5rem;
}

h2 {
    display: block;
    font-size: 1.5em;
    margin-block-start: 0.83em;
    margin-block-end: 0.83em;
    margin-inline-start: 0px;
    margin-inline-end: 0px;
    font-weight: bold;
    unicode-bidi: isolate;
}

p {
    margin-top: 0;
    margin-bottom: 1rem;
}
</style>