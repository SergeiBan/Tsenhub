import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AboutView from '../views/AboutView.vue'
import RegisterView from '../views/RegisterView.vue'
import RegisterConfirmView from '../views/RegisterConfirmView.vue'
import RegisterSentView from '../views/RegisterSentView.vue'
import RegisterFinalView from '../views/RegisterFinalView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      component: AboutView
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView
    },
    {
      path: '/verify-user',
      name: 'verify-user',
      component: RegisterConfirmView

    },
    {
      path: '/register-sent',
      name: 'register-sent',
      component: RegisterSentView,
      beforeEnter(to, from) {
        if (from['path'] != '/register') { return false }
      }
    },
    {
      path: '/register-final',
      name: 'register-final',
      component: RegisterFinalView
    }
  ]
})

export default router
