<script setup>
import { ref } from 'vue'
import FiedErrors from '../components/FieldErrors.vue'
import router from '../router'

const email = ref(null)
const password = ref(null)
const submitURL = '/api/token/'

const emits = defineEmits(['login'])

const errors = {
    email: null, password: null, non_field_errors: null
}
const has_errors = ref(false)

async function submitLogin() {
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            email: email.value,
            password: password.value,
        })
    }
    const response = await fetch(submitURL, requestOptions)
    const responseJSON = await response.json()

    if (response['status'] == 200) {
        window.localStorage.setItem('access', responseJSON['access'])
        window.localStorage.setItem('refresh', responseJSON['refresh'])
        window.localStorage.setItem('role', responseJSON['role'])
        emits('login', true)
        router.push('/')
    }

    has_errors.value = false
    const fields = ['email', 'password', 'non_field_errors']
    fields.forEach(element => {
        errors[`${element}`] = element in responseJSON ? responseJSON[element] : null
        has_errors.value = element in responseJSON ? true : has_errors.value
    });
}
</script>

<template>
<h2>Вход</h2>
<form @submit.prevent="submitLogin" class="col-md-6">
    <FiedErrors :has_errors="has_errors" :errors="errors.non_field_errors" />

    <label for="email-field" class="form-label mb-2">Почта</label>
    <input type="email" v-model="email" required id="email-field" class="form-control mb-2">
    <FiedErrors :has_errors="has_errors" :errors="errors.email" />
    
    <label for="password-field" class="form-label mb-2">Пароль</label>
    <input type="password" v-model="password" required id="password-field" class="form-control mb-2">
    <FiedErrors :has_errors="has_errors" :errors="errors.password" />

    <input type="submit" value="Войти" class="btn btn-info form-control mt-4">

</form>
</template>