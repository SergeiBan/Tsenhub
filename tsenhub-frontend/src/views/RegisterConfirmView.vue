<script setup>
import { useRoute } from 'vue-router';
import { onMounted, ref } from 'vue';
import router from '../router'
import EnterStatus from '../components/EnterStatus.vue';

const route = useRoute()

const confirmURL = ref('/api/accounts/verify-registration/')
const emit = defineEmits(['login'])

onMounted(async () => {
    if (!route.query) { router.push('/') }
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            user_id: route.query['user_id'],
            timestamp: route.query['timestamp'],
            signature: route.query['signature']
        })
    }
    const response = await fetch(confirmURL.value, requestOptions)
    if (response['status'] == 200) {
        const responseJSON = await response.json()
        const token = responseJSON['token']
        window.localStorage.setItem('token', token)
        emit('login', true)
        router.push('/register-final')
    }
    router.push('/')

})
</script>
