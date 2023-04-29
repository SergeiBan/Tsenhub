<script setup>
const props = defineProps({
    has_errors: Boolean,
    errors: Array
})
</script>

<template>
<template v-if="has_errors">
    <p class="text-info" v-for="e in errors" :key="e.id">{{ e }}</p>
</template>
</template>