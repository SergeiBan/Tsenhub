<script setup>
import { ref } from 'vue'

let pricelist = ref(null)
const token = window.localStorage.getItem('token')

function addPricelist(event) {
  pricelist.value = event.target.files[0]
}

async function sendPricelist() {
  const formData = new FormData()
  formData.append('pricelist', pricelist.value)
  const headers = {'Authorization': `Token ${token}`}
  const response = await fetch('/api/v1/parts/add_parts/', { method: 'POST', body: formData, headers: headers })
  const responseJson = await response.json()
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
