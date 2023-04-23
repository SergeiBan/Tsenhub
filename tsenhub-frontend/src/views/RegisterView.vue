<script setup>
import { ref } from 'vue'
import FiedErrors from '../components/FieldErrors.vue'
import router from '../router'

const email = ref(null)
const entity = ref(null)
const password = ref(null)
const password_confirm = ref(null)
const submitURL = '/api/v1/users/'

const errors = {
    email: null, entity: null, password: null, password_confirm: null, non_field_errors: null
}
const has_errors = ref(false)

async function submitRegistraion() {
    if (password.value !== password_confirm.value) {
        has_errors.value = true
        errors.password = ['Пароли не совпадают']
        errors.password_confirm = ['Пароли не совпадают']
        return
    }
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            email: email.value,
            entity: entity.value,
            password: password.value
        })
    }
    const response = await fetch(submitURL, requestOptions)
    const responseJSON = await response.json()

    if (response['status'] == 201) { 
        router.push('/register-sent')
    }
    has_errors.value = false
    const fields = ['email', 'entity', 'password', 'non_field_errors']
    fields.forEach(element => {
        errors[`${element}`] = element in responseJSON ? responseJSON[element] : null
        has_errors.value = element in responseJSON ? true : has_errors.value
    });
}
</script>

<template>
<h2 class="col-12">Регистрация</h2>
<form @submit.prevent="submitRegistraion" class="col-md-6">
    <FiedErrors :has_errors="has_errors" :errors="errors.non_field_errors" />

    <label for="email-field" class="form-label mb-2">Почта</label>
    <input type="email" v-model="email" required id="email-field" class="form-control mb-2">
    <FiedErrors :has_errors="has_errors" :errors="errors.email" />

    <label for="entity-field" class="form-label mb-2">Название организации</label>
    <input type="text" v-model="entity" required id="entity-field" class="form-control mb-2">
    <FiedErrors :has_errors="has_errors" :errors="errors.entity" />
    
    <label for="password-field" class="form-label mb-2">Пароль</label>
    <input type="password" v-model="password" required id="password-field" class="form-control mb-2">
    <FiedErrors :has_errors="has_errors" :errors="errors.password" />

    <label for="password_confirm-field" class="form-label mb-2">Пароль повторно</label>
    <input type="password" v-model="password_confirm" required id="password_confirm-field" class="form-control mb-2">
    <FiedErrors :has_errors="has_errors" :errors="errors.password_confirm" />

    <input type="submit" value="Зарегистрироваться" class="btn btn-info form-control mt-4">

</form>
</template>