<script setup>
import { useRoute } from 'vue-router';
import { onMounted, ref } from 'vue';
import router from '../router'

const route = useRoute()

const confirmURL = ref('/api/v1/users/verify-user/')
const emit = defineEmits(['login', 'roleAssigned'])

onMounted(async () => {
    if (!route.query) { router.push('/') }
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            token: route.query['token']
        })
    }
    const response = await fetch(confirmURL.value, requestOptions)
    if (response['status'] == 200) {
        const responseJSON = await response.json()
        window.localStorage.setItem('access', responseJSON['access'])
        window.localStorage.setItem('refresh', responseJSON['refresh'])
        window.localStorage.setItem('role', responseJSON['role'])

        emit('login', true)
        emit('roleAssigned', responseJSON['role'])
        router.push('/register-final')
    } else { router.push('/') }

})
</script>
