<template>
    <div class="polaroid">
        <img src="https://cdn.imweb.me/upload/S20210807d1f68b7a970c2/7170113c6a983.jpg" alt="Example">
        <div class="polaroid-text">Your Caption Here</div>
    </div>
</template>

<style scoped>
.polaroid {
    position: relative;
    background: #fff; /* 배경색을 하얀색으로 변경 */
    border: solid #fff;
    border-width: 6px 6px 40px 6px; /* 하단 여백을 60px에서 40px로 줄임 */
    box-shadow: 2px 2px 8px #333;
    height: 300px;
    width: 250px;
}

.polaroid img {
    display: block;
    width: 100%;
    height: calc(100% - 40px); /* 하단 여백 조정에 맞춰 수정 */
    object-fit: cover;
    border-bottom: solid 6px #fff;
}

.polaroid-text {
    position: absolute;
    bottom: 10px; /* 위치 조정 */
    width: 100%;
    text-align: center;
    font-size: 16px;
    font-family: Arial, sans-serif;
    color: #000;
    line-height: 1.2;
}
</style>