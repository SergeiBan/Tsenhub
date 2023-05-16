<script setup>
import { ref } from 'vue'
import { refreshAccess } from '../js/helpers'
import router from '../router';

const emits = defineEmits(['login'])
let quote_request_list = ref(null)
let downloadLink = ref(null)
let orderURL = '/api/v1/parts/place_order/'
let orderInstruction = ref(
  'Если расценки подходят, вы можете разместить заказ немедленно')
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
  status.value = null

  const responseBlob = await response.blob()
  const blobUrl = URL.createObjectURL(responseBlob)
  downloadLink.value = blobUrl;
}

async function placeOrder() {
  const headers = {'Authorization': `Bearer ${access}`}
  const requestOptions = { method: 'POST', headers: headers}
  let response = await fetch(orderURL, requestOptions)

  if (response['status'] != 201) {
    response = await tokenUpdatedRequest(orderURL, requestOptions)
  }
  if (response['status'] == 201) {
    orderInstruction.value = 'Заказ отправлен!'
  } else {
    orderInstruction.value = 'При отправке заказа возникла ошибка!'
  }
}

</script>

<template>
  <div class="col-lg-6">

    <form @submit.prevent="sendQuotesRequest" class="mb-4">
      <input type="file" @change="addQuoteRequests" class="form-control mb-2">
      <input type="submit" class="form-control btn btn-info">
    </form>

    <div class="row mb-3">
      <div class="col-lg-8 col-6">
        <img src="../assets/upload_instruction.jpg" class="img-fluid">
      </div>
      <div class="col-lg-4 col-6"><p class="lead"><b>Образец заполнения</b></p>
      </div>
    </div>
    <p class="display-6">Загрузите файл .xlsx</p>
    <p class="lead">Не пропускайте пустых строк</p>
    <p class="lead">В первой колонке должны стоять артикулы, а во второй - количество запчастей</p>
    <p class="fw-bold">Цены даны по сегодняшнему курсу евро ЦБ</p>
    <p v-if="status">{{ status }}</p>
    <div class="col-12 mb-2">
      <a v-if="downloadLink" :href="downloadLink" download="Запчастица_Расценки.xlsx" class="btn btn-primary w-75 mb-2">
    Скачать таблицу цен</a>
      <p v-if="downloadLink">{{ orderInstruction }}</p>
      <a v-if="downloadLink" :href="orderLink" class="btn btn-info w-75" @click="placeOrder">
    Заказать!</a>
    </div>
  </div>
  <div class="col-lg-6">
    <img src="../assets/quotes_request.jpg" class="img-fluid">
  </div>
</template>
