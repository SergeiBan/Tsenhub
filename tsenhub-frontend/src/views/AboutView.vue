<script setup>
import { ref } from 'vue'
import { refreshAccess } from '../js/helpers'
import router from '../router';

const emits = defineEmits(['login'])
let quote_request_list = ref(null)
let downloadLink = ref(null)
const generateURL = '/api/v1/parts/generate_quotes/'
let access = window.localStorage.getItem('access')

function addQuoteRequests(event) {
  quote_request_list.value = event.target.files[0]
}


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


async function sendQuotesRequest() {
  const formData = new FormData()
  formData.append('quotes_request', quote_request_list.value)
  const headers = {'Authorization': `Bearer ${access}`}
  const requestOptions = { method: 'POST', body: formData, headers: headers }
  let response = await fetch(generateURL, requestOptions)
  
  if (response['status'] == 401) {
    response = await tokenUpdatedRequest(generateURL, requestOptions)
  }

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
  <form @submit.prevent="sendQuotesRequest">
    <input type="file" @change="addQuoteRequests">
    <input type="submit">
  </form>
  <a v-if="downloadLink" :href="downloadLink" download="Стоимость.xlsx"></a>
</template>
