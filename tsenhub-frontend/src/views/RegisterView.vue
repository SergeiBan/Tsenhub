<script setup>
import { ref } from 'vue'
import FiedErrors from '../components/FieldErrors.vue'
import router from '../router'
import EnterStatus from '../components/EnterStatus.vue'

const email = ref(null)
const username = ref(null)
const password = ref(null)
const password_confirm = ref(null)
const submitURL = '/api/accounts/register/'

const errors = {
    email: null, username: null, password: null, password_confirm: null, non_field_errors: null
}
const has_errors = ref(false)

async function submitRegistraion() {
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            email: email.value,
            username: username.value,
            password: password.value,
            password_confirm: password_confirm.value
        })
    }
    const response = await fetch(submitURL, requestOptions)
    const responseJSON = await response.json()

    if (response['status'] == 201) { 
        router.push('/register-sent')
    }

    has_errors.value = false
    const fields = ['email', 'username', 'password', 'password_confirm', 'non_field_errors']
    fields.forEach(element => {
        console.log(element, element in responseJSON, responseJSON)
        errors[`${element}`] = element in responseJSON ? responseJSON[element] : null
        has_errors.value = element in responseJSON ? true : has_errors.value
    });
}
</script>

<template>
<h2 class="col">Регистрация</h2>
<form @submit.prevent="submitRegistraion" class="col-md-6">
    <FiedErrors :has_errors="has_errors" :errors="errors.non_field_errors" />

    <label for="email-field" class="form-label mb-2">Почта</label>
    <input type="email" v-model="email" required id="email-field" class="form-control mb-2">
    <FiedErrors :has_errors="has_errors" :errors="errors.email" />

    <label for="username-field" class="form-label mb-2">Название организации или ваше имя</label>
    <input type="text" v-model="username" required id="username-field" class="form-control mb-2">
    <FiedErrors :has_errors="has_errors" :errors="errors.username" />
    
    <label for="password-field" class="form-label mb-2">Пароль</label>
    <input type="password" v-model="password" required id="password-field" class="form-control mb-2">
    <FiedErrors :has_errors="has_errors" :errors="errors.password" />

    <label for="password_confirm-field" class="form-label mb-2">Пароль повторно</label>
    <input type="password" v-model="password_confirm" required id="password_confirm-field" class="form-control mb-2">
    <FiedErrors :has_errors="has_errors" :errors="errors.password_confirm" />

    <input type="submit" value="Зарегистрироваться" class="btn btn-info form-control mt-4">

</form>
</template>