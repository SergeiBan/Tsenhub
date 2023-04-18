<script setup>
import { onMounted, ref } from 'vue'
const props = defineProps({
    status: String
})

const header = ref(null)

onMounted(() => {
    header.value = props.status
})
</script>

<template>
<h1>{{ header }}</h1>

</template>