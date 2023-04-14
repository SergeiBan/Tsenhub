<script setup>
import { ref } from 'vue'
import FiedErrors from '../components/FieldErrors.vue'

const email = ref(null)
const username = ref(null)
const password = ref(null)
const passwordConfirm = ref(null)
const submitURL = '/api/v1/accounts/register/'

const errors = {
    email: null, username: null, password: null, passwordConfirm: null
}
const has_errors = ref(false)

async function submitRegistraion() {
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            'email': email.value,
            'username': username.value,
            'password': password.value,
            'password_confirm': passwordConfirm.value
        })
    }
    const response = await fetch(submitURL, requestOptions)
    console.log(response)
    const responseJSON = await response.json()
    console.log(responseJSON)

    has_errors.value = false
    const fields = ['email', 'username', 'password', 'password_confirm']
    fields.forEach(element => {
        console.log(element, element in responseJSON, responseJSON)
        errors[`${element}`] = element in responseJSON ? responseJSON[element] : null
        has_errors.value = element in responseJSON ? true : has_errors.value
    });
}
</script>

<template>
<h2>Регистрация</h2>
<form @submit.prevent="submitRegistraion">
    <label for="email-field" class="form-label mb-2">Почта</label>
    <input type="email" v-model="email" required id="email-field" class="form-control mb-2">
    <FiedErrors :has_errors="has_errors" :errors="errors.email" />

    <label for="username-field" class="form-label mb-2">Название организации или ваше имя</label>
    <input type="text" v-model="username" required id="username-field" class="form-control mb-2">
    <FiedErrors :has_errors="has_errors" :errors="errors.username" />
    
    <label for="password-field" class="form-label mb-2">Пароль</label>
    <input type="password" v-model="password" required id="password-field" class="form-control mb-2">
    <FiedErrors :has_errors="has_errors" :errors="errors.password" />

    <label for="password-confirm-field" class="form-label mb-2">Пароль повторно</label>
    <input type="password" v-model="passwordConfirm" required id="password-confirm-field" class="form-control mb-2">
    <FiedErrors :has_errors="has_errors" :errors="errors.passwordConfirm" />

    <input type="submit" value="Зарегистрироваться" class="btn btn-info form-control">

</form>
</template>