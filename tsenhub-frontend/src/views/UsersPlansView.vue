<script setup>
import { onMounted, ref } from 'vue';
import { refreshAccess } from '../js/helpers';

let userListURL = '/api/v1/users/'
const plansListURL = '/api/v1/plans/'
const planUpdateURL = '/api/v1/usersplan/'

let access = window.localStorage.getItem('access')
const users = ref(null)
const plans = ref(null)

const prevURL = ref(null)
const nextURL = ref(null)

const selectedUsers = ref([])
const selectedPlan = ref(null)

async function tokenUpdatedRequest(URL, requestOptions) {
    let new_access = await refreshAccess()
    if (new_access == 'refresh expired'){
        emits('login', false)
        router.push('/login')
    }
    access = new_access
    requestOptions.headers.Authorization = `Bearer ${access}`
    const response = await fetch(URL, requestOptions)
    return response
}

async function get_users() {
    const requestOptions = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${access}`
        },
    }
    let usersResponse = await fetch(userListURL, requestOptions)
    if (usersResponse['status'] == 401) {
        usersResponse = await tokenUpdatedRequest(userListURL, requestOptions)}
        
    const users_data = await usersResponse.json()
    users.value = users_data['results']
    prevURL.value = users_data['previous']
    nextURL.value = users_data['next']
}

onMounted(async () => {
    await get_users()
    const requestOptions = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${access}`
        },
    }

    let plansResponse = await fetch(plansListURL, requestOptions)
    if (plansResponse['status'] == 401) {
        plansResponse = await tokenUpdatedRequest(plansListURL, requestOptions)}
    plans.value = await plansResponse.json()
})


async function planChange() {
    const requestOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${access}`
        },
        body: JSON.stringify({
            users: selectedUsers.value,
            plan: selectedPlan.value
        })
    }
    let response = await fetch(planUpdateURL, requestOptions)
    if (response['status'] == 401) {
        response = await tokenUpdatedRequest(planUpdateURL, requestOptions)}
    await get_users()
    selectedUsers.value = []
}

async function get_prev() {
    userListURL = prevURL.value
    await get_users()
}
async function get_next() {
    userListURL = nextURL.value
    await get_users()
}

</script>

<template>
<div class="col-12">
    <p>Отметьте заказчиков, затем выберите для них тариф из выпадающего списка</p>
</div>
<div class="col-12 mb-4">
    <select name="plans" id="" class="form-select" v-model="selectedPlan" @change="planChange">
        <option v-for="plan in plans" :key="plan.id" :value="plan.pk">{{ plan.discount }}%: {{ plan.name }}</option>
    </select>    
</div>


<div class="col-12 mb-2">
    <div class="row justify-content-between">
        <div class="col-4">
            <button v-if="prevURL" class="btn btn-info w-100" @click="get_prev">Пред.</button>
        </div>
        <div class="col-4">
            <button v-if="nextURL" class="btn btn-info w-100" @click="get_next">След.</button>
        </div>
    </div>
</div>

<div class="list-group col-md-8 offset-md-2">
    <label class="list-group-item" v-for="user in users" :key="user.id">
        <input type="checkbox" class="form-check-input me-1" :name="user.email"
        v-model="selectedUsers" :id="user.email" :value="user.pk">
        {{ user.entity }}: {{ user.email }}
        <span v-if="user.plan" class="text-primary">{{ user.plan.discount }}%</span>
        <span v-else class="text-danger small">не назначено</span>
    </label>
</div>

</template>