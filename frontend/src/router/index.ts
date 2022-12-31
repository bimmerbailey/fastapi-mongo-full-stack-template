import { createRouter, createWebHistory } from 'vue-router'
import { getLocalToken } from '@/utils'
import { useAuthStore } from '@/stores/auth'
import { computed } from 'vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue'),
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
    },
    // {
    //   path: '/forgot-password',
    //   name: 'forgot-password',
    //   component: () => import('../components/ForgotPassword.vue'),
    // },
    // {
    //   path: '/signup',
    //   name: 'signup',
    //   component: () => import('../components/SignUp.vue'),
    // },
    {
      path: '/users',
      name: 'users',
      component: () => import('../views/UsersView.vue'),
      meta: {
        requiresAuth: true,
      },
    },
  ],
})

router.beforeEach(async (to, from, next) => {
  const store = useAuthStore()
  await store.checkLoggedIn()
  const loggedIn = computed(() => store.authState.LoggedIn)
  const isAuth = Boolean(getLocalToken())

  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (!isAuth) {
      return next({
        name: 'login',
        state: { nextURL: to.fullPath },
      })
    } else {
      if (!loggedIn.value) {
        return next({
          name: 'login',
          state: { nextURL: to.fullPath },
        })
      } else {
        return next()
      }
    }
  } else {
    return next()
  }
})
export default router
