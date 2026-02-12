import { defineStore } from 'pinia'
import { AuthApi } from '@/api/auth'
import { saveLocalToken, removeLocalToken, getLocalToken } from '@/stores/utils'
import type { LoginResults, User } from '@/interfaces/Auth'
import { ref } from 'vue'
import router from '@/router'

// FIXME: Come back to look at this, I think I can do better

export const useAuthStore = defineStore('Auth', () => {
  const authToken = ref<string | null>(getLocalToken())
  const isAdmin = ref<boolean>(false)
  const isLoggedIn = ref<boolean>(false)
  const user = ref<User>()

  async function login(username: string, password: string) {
    await AuthApi.login(username, password)
      .then(async (resp: LoginResults) => {
        authToken.value = resp.access_token
        isLoggedIn.value = true
        saveLocalToken(resp.access_token)
        return await checkLoggedIn()
      })
      .catch((err) => {
        removeLocalToken()
        throw err
      })
  }

  async function checkAuth(token: string | null) {
    if (token == null) {
      throw new Error('Authentication Error')
    }
    await AuthApi.checkAuthentication()
      .then((resp: User) => {
        isLoggedIn.value = true
        user.value = resp
        isAdmin.value = resp.is_admin
        authToken.value = token
      })
      .catch((err) => {
        authToken.value = null
        isAdmin.value = false
        isLoggedIn.value = false
        user.value = undefined
        removeLocalToken()
        throw err
      })
  }

  async function checkLoggedIn() {
    if (!isLoggedIn.value) {
      let token = authToken.value
      if (!token) {
        const localToken = getLocalToken()
        if (localToken) {
          authToken.value = localToken
          token = localToken
        }
      }
      if (token) {
        await checkAuth(token)
      } else {
        removeLocalToken()
        authToken.value = null
        isAdmin.value = false
        isLoggedIn.value = false
        user.value = undefined
      }
    }
  }

  async function logOut() {
    return await AuthApi.logOut()
      .catch((err) => {
        return err
      })
      .finally(() => {
        removeLocalToken()
        authToken.value = null
        isAdmin.value = false
        isLoggedIn.value = false
        user.value = undefined
        return router.push('/login')
      })
  }

  return {
    user,
    isAdmin,
    login,
    logOut,
    isLoggedIn,
    authToken
  }
})
