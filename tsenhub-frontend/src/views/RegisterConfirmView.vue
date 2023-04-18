<script setup>
import { useRoute } from 'vue-router';
import { onMounted, ref } from 'vue';
import router from '../router'
import EnterStatus from '../components/EnterStatus.vue';

const route = useRoute()

const confirmURL = ref('/api/accounts/verify-registration/')

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
        router.push('/register-final')
    }
    router.push('/')

})
</script>
