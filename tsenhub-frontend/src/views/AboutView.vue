<script setup>
import { ref } from 'vue'

let quote_request_list = ref(null)
let downloadLink = ref(null)
const token = window.localStorage.getItem('token')

function addQuoteRequests(event) {
  quote_request_list.value = event.target.files[0]
}

async function sendPricelist() {
  console.log(token)
  const formData = new FormData()
  formData.append('quotes_request', quote_request_list.value)
  const headers = {'Authorization': `Token ${token}`}
  const response = await fetch('/api/v1/parts/generate_quotes/', { method: 'POST', body: formData, headers: headers})
  const responseBlob = await response.blob()
  const blobUrl = URL.createObjectURL(responseBlob)

  var link = document.createElement("a"); // Or maybe get it from the current document
  link.href = blobUrl;
  link.download = "123.xlsx";
  link.innerHTML = "Click here to download the file";
  document.body.appendChild(link); // Or append it whereever you want
}

</script>

<template>
  <p>Для получения цен необходимо загрузить файл xlsx.</p>
  <form @submit.prevent="sendPricelist">
    <input type="file" @change="addQuoteRequests">
    <input type="submit">
  </form>
  <a v-if="downloadLink" :href="downloadLink" download="Стоимость.xlsx"></a>
</template>
