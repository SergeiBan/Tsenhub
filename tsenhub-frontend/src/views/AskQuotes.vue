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

  if (response['status'] == 403) {
    status.value = 'Извините, Запчастица еще не готова вас обслуживать'
    return
  } else if (response['status'] != 200) {
      status.value = 'Извините, но при загрузке произошла ошибка'
      return
  }

  const responseBlob = await response.blob()
  const blobUrl = URL.createObjectURL(responseBlob)
  downloadLink.value = blobUrl;
}

</script>

<template>
  <div class="col-lg-6">

    <form @submit.prevent="sendQuotesRequest" class="mb-4">
      <input type="file" @change="addQuoteRequests" class="form-control mb-2">
      <input type="submit" class="form-control btn btn-info">
    </form>
    <p class="display-6">Для получения цен загрузите файл .xlsx</p>
    <p class="display-6">Начиная с первой строки: в первой колонке должны стоять артикулы, а во второй - количество запчастей</p>
    <p v-if="status">{{ status }}</p>
    <div class="col-12">
      <a v-if="downloadLink" :href="downloadLink" download="Стоимость.xlsx" class="btn btn-primary w-100">
    Скачать таблицу цен</a>
    </div>
  </div>
  <div class="col-lg-6">
    <img src="../assets/quotes_request.jpg" class="img-fluid">
  </div>
</template>
