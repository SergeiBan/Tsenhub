<script setup>
import { useRoute } from 'vue-router';
import { onMounted } from 'vue';

const route = useRoute()

onMounted(() => {
    console.log(route.query, 'query')

})
</script>

<template>
    <h1>Hihi</h1>
</template>