<script setup>
import { ref } from 'vue'
import { getResponse, refreshAccess } from '../js/helpers';

let pricelist = ref(null)
let access = window.localStorage.getItem('access')
const pricelistURL = '/api/v1/parts/add_parts/'

function addPricelist(event) {
  pricelist.value = event.target.files[0]
}

async function sendPricelist() {
  const formData = new FormData()
  formData.append('pricelist', pricelist.value)
  const headers = {'Authorization': `Bearer ${access}`}
  const requestOptions = { method: 'POST', body: formData, headers: headers }

  let response = await fetch(pricelistURL, requestOptions)
  if (response['status'] == 200) { return }

  if (response['status'] == 401) {
    let new_access = await refreshAccess()
    if (new_access == 'refresh expired'){
      emits('login', false)
      router.push('/login')
    }
    access = new_access
    requestOptions.headers.Authorization = `Bearer ${access}`
    response = await fetch(pricelistURL, requestOptions)
  }
}
</script>

<template>
  <main>
    <form @submit.prevent="sendPricelist">
      <input type="file" @change="addPricelist">
      <input type="submit">

    </form>
  </main>
</template>
