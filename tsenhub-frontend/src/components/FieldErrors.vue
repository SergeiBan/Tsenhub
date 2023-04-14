<script setup>
const props = defineProps({
    has_errors: Boolean,
    errors: Array
})
</script>

<template>
<template v-if="has_errors">
    <p v-for="e in errors" :key="e.id">{{ e }}121212</p>
</template>
</template>