<script setup>
import router from '../router'

function goHome() {
    router.push('/')
}
</script>

<template>

<h1>Учетная запись подтверждена.</h1>
<button class="btn btn-info" @click="goHome">Получить расценки!</button>

</template>