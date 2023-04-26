<script setup>
import { ref, onMounted } from 'vue'
import { refreshAccess } from '../js/helpers';

const props = defineProps({
    access: String
})

const emits = defineEmits(['plan-selected'])

const selectedPlan = ref(null)

const plans = ref(null)
const plansURL = '/api/v1/plans/'

async function tokenUpdatedRequest(URL, requestOptions) {
    let new_access = await refreshAccess()
    if (new_access == 'refresh expired'){
        emits('login', false)
        router.push('/login')
    }
    props.access = new_access
    requestOptions.headers.Authorization = `Bearer ${props.access}`
    const response = await fetch(URL, requestOptions)
    return response
}

async function planChange() {
    emits('plan-selected', selectedPlan.value)
}


onMounted(async () => {
    const requestOptions = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${props.access}`
        },
    }

    let plansResponse = await fetch(plansURL, requestOptions)
    if (plansResponse['status'] == 401) {
        plansResponse = await tokenUpdatedRequest(plansURL, requestOptions)}
    plans.value = await plansResponse.json()
})
</script>


<template>

<div class="col-md-6 mb-4">
    <select name="plans" id="" class="form-select" v-model="selectedPlan" @change="planChange">
        <option v-for="plan in plans" :key="plan.id" :value="plan.pk">{{ plan.discount }}%: {{ plan.name }}</option>
    </select>    
</div>
</template>