import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import { useAuthStore } from '@/stores/authentication'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/items',
      name: 'items',
      component: () => import('../views/ItemsView.vue')
    }
  ]
})

// TODO: routes for auth
// router.beforeEach((to) => {
//   const authStore = useAuthStore()
//   if (!authStore.isLoggedIn && to.name !== 'login') {
//     return { name: 'login' }
//
// })

export default router
