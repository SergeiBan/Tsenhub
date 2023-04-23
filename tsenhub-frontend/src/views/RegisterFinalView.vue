<script setup>
import router from '../router'

function goHome() {
    router.push('/')
}
</script>

<template>

<h1 class="mb-5">Учетная запись подтверждена. Через сутки вы сможете воспользоваться функционалом прилолжения.</h1>
<button class="btn btn-info" @click="goHome">Получить расценки!</button>

</template>