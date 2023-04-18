<script setup>
import { onMounted } from 'vue';
import router from '../router'

const emit = defineEmits(['login'])

onMounted(() => {
    window.localStorage.removeItem('token')
    emit('login', false)
    router.push('/')
})
</script>