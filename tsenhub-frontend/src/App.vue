<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { onMounted, ref } from 'vue'

let is_logged = ref(false)
let role = ref(null)

onMounted(async () => {
  const access = window.localStorage.getItem('access')
  if (access) { 
    is_logged.value = true
  }
  role.value = window.localStorage.getItem('role')
})


</script>

<template>

  <header class="row mb-5">
    <div class="col">
      <nav class="nav nav-pills navbar-light navbar-expand-lg bg-light justify-content-between">
        <RouterLink v-if="is_logged == true && role == 'supplier'" to="/users-plans" class="nav-item nav-link">Назначить тариф</RouterLink>
        <RouterLink v-if="is_logged == true && role == 'supplier'" to="/add-pricelist" class="nav-item nav-link">Добавить прайслист</RouterLink>
        <RouterLink v-if="is_logged == true && role == 'supplier'" to="/edit-plans" class="nav-item nav-link">Тарифы</RouterLink>
        <RouterLink v-if="is_logged == true" to="/ask-quotes" class="nav-item nav-link">Получить цены</RouterLink>
        
        <RouterLink v-if="is_logged == true" to="/logout" class="nav-item nav-link">Выйти</RouterLink>
        <RouterLink v-if="is_logged == false" to="/register" class="nav-item nav-link">Регистрация</RouterLink>
        <RouterLink v-if="is_logged == false" to="/login" class="nav-item nav-link align-self-end">Вход</RouterLink>
      </nav>
    </div>
  </header>
  <main class="row">
    <RouterView @login="(status) => is_logged = status" @roleAssigned="(status) => role = status"/>
  </main>
</template>
