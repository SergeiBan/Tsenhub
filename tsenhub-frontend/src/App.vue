<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { onMounted, ref } from 'vue'

let is_logged = ref(false)

onMounted(() => {
  const token = window.localStorage.getItem('token')
  if (token) { is_logged.value = true }
})
</script>

<template>

  <header class="row mb-5">
    <div class="col">
      <nav class="nav nav-pills navbar-light navbar-expand-lg bg-light">
        <RouterLink v-if="is_logged == true" to="/" class="nav-item nav-link">Добавить прайслист</RouterLink>
        <RouterLink v-if="is_logged == true" to="/about" class="nav-item nav-link">Расценки</RouterLink>
        <RouterLink v-if="is_logged == true" to="/logout" class="nav-item nav-link">Выйти</RouterLink>
        <RouterLink v-if="is_logged == false" to="/register" class="nav-item nav-link">Регистрация</RouterLink>
        <RouterLink v-if="is_logged == false" to="/login" class="nav-item nav-link">Вход</RouterLink>
      </nav>
    </div>
  </header>

  <RouterView class="row" @login="(status) => is_logged = status"/>
</template>
