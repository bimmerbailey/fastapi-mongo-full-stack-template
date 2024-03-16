import { createRouter, createWebHistory } from 'vue-router'
import { businessInfo } from '@/business'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      meta: {
        title: 'Dashboard',
        requiresAuth: true,
      },
      path: '/',
      name: 'home',
      component: () => import('@/views/HomeView.vue'),
    },
    {
      meta: {
        title: 'Profile',
        requiresAuth: true,
      },
      path: '/profile',
      name: 'profile',
      component: () => import('@/views/ProfileView.vue'),
    },
    {
      meta: {
        title: 'Users',
        requiresAuth: true,
      },
      path: '/users',
      name: 'users',
      component: () => import('@/views/UsersView.vue'),
    },
    {
      meta: {
        title: 'Items',
        requiresAuth: true,
      },
      path: '/items',
      name: 'items',
      component: () => import('@/views/ItemsView.vue'),
    },
    {
      meta: {
        title: 'Login',
      },
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue'),
    },
    {
      meta: {
        title: 'Error',
      },
      path: '/error',
      name: 'error',
      component: () => import('@/views/ErrorView.vue'),
    },
  ],
  scrollBehavior(to, from, savedPosition) {
    return savedPosition || { top: 0 }
  },
})

router.beforeEach(async (to, from, next) => {
  const store = useAuthStore()
  await store.checkLoggedIn()

  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (!store.authToken) {
      return next({
        name: 'login',
        state: { nextURL: to.fullPath },
      })
    } else {
      return next()
    }
  } else {
    return next()
  }
})

const defaultDocumentTitle = businessInfo.name
/* Set document title from route meta */
router.afterEach((to) => {
  document.title = to.meta?.title
    ? `${to.meta.title} — ${defaultDocumentTitle}`
    : defaultDocumentTitle
})

export default router
