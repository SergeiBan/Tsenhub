<script setup>
import { onMounted, ref } from 'vue'
import { refreshAccess } from '../js/helpers';

const emits = defineEmits(['logout'])

const plansURL = '/api/v1/plans/'
const removePlansURL = '/api/v1/plans/remove_plans/'

const markup = ref(null)
const muliplier = ref(null)
const description = ref(null)

const plans = ref(null)
const selectedPlans = ref([])

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
            markup: markup.value,
            multiplier: muliplier.value,
            name: description.value
        })
    }
    let response = await fetch(plansURL, requestOptions)
    if (response['status'] == 401) {
        response = await tokenUpdatedRequest(plansURL, requestOptions)}
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

async function removePlans() {
    const requestOptions = {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${access}` },
        body: JSON.stringify({
            plans: selectedPlans.value
        })
    }
    let response = await fetch(removePlansURL, requestOptions)
    if (response['status'] == 401) {
        response = await tokenUpdatedRequest(removePlansURL, requestOptions)}
    plans.value = await response.json()
}

onMounted(async () => {
    await getPlans()
})
</script>

<template>
    <div class="col-lg-6">
        <p>Заполните поля, чтобы добавить новый тариф. Ненужные тарифы можно удалять в списке ниже.</p>
        <form @submit.prevent="addPlan">
            <div class="row g-3">
                <div class="col-6">
                    <label for="markup-field" class="form-label">Размер наценки в %</label>
                    <input type="number" step="1" min=0 class="form-control mb-2" id="markup-field" v-model="markup" required>
                </div>
                <div class="col-6">
                    <label for="multiplier-field" class="form-label">Множитель</label>
                    <input type="number" step="0.01" min=0 class="form-control mb-2" id="multiplier-field" v-model="muliplier" required>
                </div>
            </div>
            <label for="description-field" class="form-label">Название тарифа</label>
            <input type="text" class="form-control mb-4" id="description-field" v-model="description" required>

            <input type="submit" class="form-control mb-5 btn btn-primary" value="Добавить тариф">
        </form>

        <div class="mb-4">
            <p>Удаляемые тарифы могут быть привязаны к покупателям.
                Назначьте им новый тариф и они снова смогут запрашивать цены
            </p>
            <label class="list-group-item mb-1" v-for="plan in plans" :id="plan.id">
                <input type="checkbox" class="form-check-input me-1" :value="plan.pk" :name="all-plans" v-model="selectedPlans">
                {{ plan.markup }}% - {{ plan.multiplier }} - {{ plan.name }}
            </label>
        </div>
        <button class="btn btn-danger w-100" @click="removePlans">Удалить выбранные тарифы</button>
    </div>
</template>

