<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { onMounted, ref } from 'vue'
import router from './router';

let is_logged = ref(false)
let role = ref(null)

onMounted(async () => {
  role.value = window.localStorage.getItem('role')
  const access = window.localStorage.getItem('access')
  if (access) { is_logged.value = true }
})


</script>

<template>

  <header class="row mb-1">
    <div class="col-12">
      <nav class="nav navbar-light navbar-expand-lg bg-light justify-content-between mb-1">
        <RouterLink v-if="is_logged == true && role == 'supplier'" to="/users-plans" class="nav-item nav-link">Назначить тариф</RouterLink>
        <RouterLink v-if="is_logged == true && role == 'supplier'" to="/add-pricelist" class="nav-item nav-link">Добавить прайслист</RouterLink>
        <RouterLink v-if="is_logged == true && role == 'supplier'" to="/edit-plans" class="nav-item nav-link">Тарифы</RouterLink>
        <RouterLink v-if="is_logged == true" to="/ask-quotes" class="nav-item nav-link">Цены и заказ</RouterLink>
        
        <RouterLink v-if="is_logged == true" to="/logout" class="nav-item nav-link">Выйти</RouterLink>
        <RouterLink v-if="is_logged == false" to="/register" class="nav-item nav-link">Впервые? Зарегистрируйся!</RouterLink>
        <RouterLink v-if="is_logged == false" to="/login" class="nav-item nav-link">Вход</RouterLink>
      </nav>
    </div>
    <div class="col-12">
      <p class="lead"><b>Запчасти для John Deere!</b><br>
        На сельскохозяйственные, строительные и лесозаготовительные машины.</p>
    </div>
  </header>
  <main class="row">
    <RouterView @login="(status) => is_logged = status" @roleAssigned="(status) => role = status"/>
  </main>
</template>
