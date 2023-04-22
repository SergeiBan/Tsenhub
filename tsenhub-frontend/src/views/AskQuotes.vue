<script setup>
import { ref } from 'vue'
import { refreshAccess } from '../js/helpers'
import router from '../router';

const emits = defineEmits(['login'])
let quote_request_list = ref(null)
let downloadLink = ref(null)
const generateURL = '/api/v1/parts/generate_quotes/'
let access = window.localStorage.getItem('access')

const status = ref(null)

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
  if (response['status'] != 200) {
    status.value = 'Извините, но при загрузке произошла ошибка'
    return
  }

  const responseBlob = await response.blob()
  const blobUrl = URL.createObjectURL(responseBlob)
  downloadLink.value = blobUrl;
}

</script>

<template>
  <div class="col-12">
    <p>Для получения цен необходимо загрузить файл xlsx.</p>
  </div>
  <div class="col-12">
    <p>Файл должен содержать две колонки. В первой - артикулы, во второй - количество запчастей.</p>
  </div>
  <div class="col-md-10 offset-md-1">  
    <form @submit.prevent="sendQuotesRequest" class="mb-4">
      <input type="file" @change="addQuoteRequests" class="form-control mb-2">
      <input type="submit" class="form-control btn btn-info">
    </form>
  </div>
  <div class="col-12" v-if="status"><p>{{ status }}</p></div>
  <div class="col-12">
    <a v-if="downloadLink" :href="downloadLink" download="Стоимость.xlsx" class="btn btn-primary w-100">
  Скачать таблицу цен</a>
  </div>
</template>
