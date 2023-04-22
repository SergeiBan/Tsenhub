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
      <nav class="nav nav-pills navbar-light navbar-expand-lg bg-light">
        <RouterLink v-if="is_logged == true && role == 'supplier'" to="/users-plans" class="nav-item nav-link">Назначить тариф</RouterLink>
        <RouterLink v-if="is_logged == true && role == 'supplier'" to="/" class="nav-item nav-link">Добавить прайслист</RouterLink>
        <RouterLink v-if="is_logged == true" to="/about" class="nav-item nav-link">Получить цены</RouterLink>
        <RouterLink v-if="is_logged == true" to="/logout" class="nav-item nav-link">Выйти</RouterLink>
        <RouterLink v-if="is_logged == false" to="/register" class="nav-item nav-link">Регистрация</RouterLink>
        <RouterLink v-if="is_logged == false" to="/login" class="nav-item nav-link">Вход</RouterLink>
      </nav>
    </div>
  </header>

  <RouterView class="row" @login="(status) => is_logged = status"/>
</template>
