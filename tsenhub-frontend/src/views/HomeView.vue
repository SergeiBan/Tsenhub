<script setup>
import { ref } from 'vue'
import TheWelcome from '../components/TheWelcome.vue'

let pricelist = ref(null)


function addPricelist(event) {
  pricelist.value = event.target.files[0]
}

async function sendPricelist() {
  const formData = new FormData()
  formData.append('pricelist', pricelist.value)
  const response = await fetch('/api/v1/parts/add_parts/', { method: 'POST', body: formData })
  const responseJson = response.json()
  console.log(responseJson)
}
</script>

<template>
  <main>
    <form @submit.prevent="sendPricelist">
      <input type="file" @change="addPricelist">
      <input type="submit">

    </form>
    <TheWelcome />
  </main>
</template>
