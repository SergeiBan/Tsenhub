import { createRouter, createWebHistory } from 'vue-router'
import AddPricelist from '../views/AddPricelist.vue'
import AskQuotes from '../views/AskQuotes.vue'
import RegisterView from '../views/RegisterView.vue'
import RegisterConfirmView from '../views/RegisterConfirmView.vue'
import RegisterSentView from '../views/RegisterSentView.vue'
import RegisterFinalView from '../views/RegisterFinalView.vue'
import LogoutView from '../views/LogoutView.vue'
import LoginView from '../views/LoginView.vue'
import UsersPlansView from '../views/UsersPlansView.vue'
import EditPlansView from '../views/EditPlansView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/add-pricelist',
      name: 'add-pricelist',
      component: AddPricelist,
      beforeEnter(to, from) {
        if (window.localStorage.getItem('role') != 'supplier') { return false }
      }
    },
    {
      path: '/ask-quotes',
      name: 'ask-quotes',
      component: AskQuotes
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
    },
    {
      path: '/logout',
      name: 'logout',
      component: LogoutView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/users-plans',
      name: 'users-plans',
      component: UsersPlansView,
      beforeEnter(to, from) {
        if (window.localStorage.getItem('role') != 'supplier') { return false }
      }
    },
    {
      path: '/edit-plans',
      name: 'edit-plans',
      component: EditPlansView,
      beforeEnter(to, from) {
        if (window.localStorage.getItem('role') != 'supplier') { return false }
      }
    }
  ]
})

export default router
