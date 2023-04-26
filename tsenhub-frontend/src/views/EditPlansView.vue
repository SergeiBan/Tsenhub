<script setup>
import { onMounted, ref } from 'vue'
import { refreshAccess } from '../js/helpers';

const plansURL = '/api/v1/plans/'
const selectedPlan = ref(null)

const discount = ref(null)
const description = ref(null)

const plans = ref(null)

let access = window.localStorage.getItem('access')

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

async function addPlan() {
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${access}` },
        body: JSON.stringify({
            discount: discount.value,
            name: description.value
        })
    }
    let response = await fetch(plansURL, requestOptions)
    const responseJSON = await response.json()
    if (response['status'] == 401) {
        response = await tokenUpdatedRequest(userListURL, requestOptions)}
    await getPlans()
}

async function getPlans() {
    const requestOptions = {
        method: 'GET',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${access}` },
    }
    let response = await fetch(plansURL, requestOptions)
    if (response['status'] == 401) {
        response = await tokenUpdatedRequest(plansURL, requestOptions)}
    plans.value = await response.json()
}

onMounted(async () => {
    await getPlans()
})
</script>

<template>
    <p>Заполните поля, чтобы добавить новый тариф. Ненужные тарифы можно удалять в списке ниже.</p>
    <form @submit.prevent="addPlan">
        <label for="discount-field" class="form-label">Размер скидки в %</label>
        <input type="number" step="0.01" min=0 class="form-control mb-2" id="discount-field" v-model="discount">

        <label for="description-field" class="form-label">Название тарифа</label>
        <input type="text" class="form-control mb-4" id="description-field" v-model="description">

        <input type="submit" class="form-control mb-5" value="Добавить тариф">
    </form>

    <div class="">

        <label class="list-group-item mb-1" v-for="plan in plans" :id="plan.id">
            <input type="checkbox" class="form-check-input me-1" :value="plan.pk" :name="all-plans">
            {{ plan.discount }}% {{ plan.name }} <button class="btn btn-primary">Удалить</button>
        </label>
    </div>
</template>

