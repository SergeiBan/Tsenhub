<script setup>
import { onMounted } from 'vue';
import router from '../router'

const emit = defineEmits(['login'])

onMounted(() => {
    window.localStorage.removeItem('access')
    window.localStorage.removeItem('refresh')
    window.localStorage.removeItem('role')

    emit('login', false)
    router.push('/')
})
</script>