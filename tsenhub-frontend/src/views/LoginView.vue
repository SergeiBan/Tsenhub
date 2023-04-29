<script setup>
import { ref } from 'vue'
import FiedErrors from '../components/FieldErrors.vue'
import router from '../router'

const email = ref(null)
const password = ref(null)
const submitURL = '/api/token/'

const emits = defineEmits(['login', 'roleAssigned'])

const errors = {
    email: null, password: null, non_field_errors: null, detail: null
}
const has_errors = ref(false)

async function submitLogin() {
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            email: email.value,
            password: password.value
        })
    }
    const response = await fetch(submitURL, requestOptions)
    const responseJSON = await response.json()

    if (response['status'] == 200) {
        window.localStorage.setItem('access', responseJSON['access'])
        window.localStorage.setItem('refresh', responseJSON['refresh'])
        window.localStorage.setItem('role', responseJSON['role'])
        emits('login', true)
        emits('roleAssigned', responseJSON['role'])
        router.push('/ask-quotes')
    }

    const responseContent = Object.keys(responseJSON)
    has_errors.value = false
    const fields = ['email', 'password', 'non_field_errors', 'detail']
    fields.forEach(element => {
        errors[`${element}`] = null
        errors[`${element}`] =  responseContent.includes(element) ? responseJSON[element] : null
        has_errors.value = responseContent.includes(element) ? true : has_errors.value
    });
    return
}
</script>

<template>
    <div class="col-lg-6">
        <form @submit.prevent="submitLogin">
            <FiedErrors :has_errors="has_errors" :errors="errors.non_field_errors" />
            <p v-if="errors.detail">{{ errors.detail }}</p>

            <input type="email" v-model="email" required id="email-field" class="form-control mb-2">
            <FiedErrors :has_errors="has_errors" :errors="errors.email" />
            <label for="email-field" class="form-label mb-3">Почта</label>
            
            <input type="password" v-model="password" required id="password-field" class="form-control mb-2">
            <FiedErrors :has_errors="has_errors" :errors="errors.password" />
            <label for="password-field" class="form-label mb-3">Пароль</label>
            
            <input type="submit" value="Войти" class="btn btn-info form-control">
        </form>
        <h2>Вход</h2>
        <p class="display-6">Введите свою электронную почту и пароль. Следом вы сможете запросить расценки на запчасти.</p>
    </div>
    <div class="col-lg-6">
        <img class="img-fluid" src="../assets/root_machine.jpg">
    </div>
</template>