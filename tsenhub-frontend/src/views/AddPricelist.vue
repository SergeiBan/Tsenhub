<script setup>
import { ref } from 'vue'
import { getResponse, refreshAccess } from '../js/helpers';

let pricelist = ref(null)
let access = window.localStorage.getItem('access')
const pricelistURL = '/api/v1/parts/add_parts/'

const loadStatus = ref(null)

function addPricelist(event) {
  pricelist.value = event.target.files[0]
}

async function sendPricelist() {
  const formData = new FormData()
  formData.append('pricelist', pricelist.value)
  const headers = {'Authorization': `Bearer ${access}`}
  const requestOptions = { method: 'POST', body: formData, headers: headers }

  loadStatus.value = 'Загрузка займет около 25 секунд. По завершении будет показано уведомление.'
  let response = await fetch(pricelistURL, requestOptions)

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
  loadStatus.value = 'Загрузка успешно завершена'
  console.log(response['status'])
  if (response['status'] != 200) { 
    loadStatus.value = 'Извините, но при загрузке произошла ошибка' 
  }
}
</script>

<template>
  <div class="col-md-6">
    <p>Загрузите прайслист в формате .csv</p>
    <p>В таблице должны быть колонки article_ и netprice_dso.
      В article_ - артикулы, в netprice_dso - базовые цены.
    </p>
    
    <form @submit.prevent="sendPricelist">
      <input type="file" @change="addPricelist" class="form-control mb-2">
      <input type="submit" class="form-control btn btn-info mb-4">
    </form>
    <p>{{ loadStatus }}</p>
</div>
</template>
