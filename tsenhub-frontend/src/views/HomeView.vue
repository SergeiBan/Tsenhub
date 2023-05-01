<script setup>
import router from '../router';

const role = window.localStorage.getItem('role')
if (role == 'seeker') { router.push('/ask-quotes') }
if (role == 'supplier') { router.push('/users-plans') }
router.push('/login')

</script>