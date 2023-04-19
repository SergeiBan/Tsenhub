<script setup>
import { onMounted, ref } from 'vue';

const userListURL = '/api/v1/users/'
const plansListURL = '/api/v1/plans/'
const token = window.localStorage.getItem('token')
const users = ref(null)
const plans = ref(null)

const selectedUsers = ref([])

onMounted(async () => {
    const requestOptions = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${token}`
        },
    }
    const usersResponse = await fetch(userListURL, requestOptions)
    users.value = await usersResponse.json()

    const plansResponse = await fetch(plansListURL, requestOptions)
    plans.value = await plansResponse.json()
})
</script>

<template>
<p>Выберите заказчиков и затем установите для них новый тариф из выпадающего списка</p>
<select name="plans" id="" class="form-select mb-4">
    <option v-for="plan in plans" :key="plan.id">{{ plan.discount }}%: {{ plan.name }}</option>
</select>

<div class="list-group">
    <label class="list-group-item" v-for="user in users" :key="user.id">
        <input type="checkbox" class="form-check-input me-1" name="customers"
        v-model="selectedUsers" :id="user.username">
        {{ user.username }}: {{ user.email }} 
        <span v-if="user.plan" class="text-primary">{{ user.plan.discount }}%</span>
        
    </label>
</div>
</template>