<script setup>
import { onMounted } from 'vue';
import router from '../router'

const emit = defineEmits(['login', 'role'])

onMounted(() => {
    window.localStorage.removeItem('access')
    window.localStorage.removeItem('refresh')
    window.localStorage.removeItem('role')

    emit('login', false)
    emit('role', null)
    router.push('/login')
})
</script>