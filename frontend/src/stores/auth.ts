import { defineStore } from 'pinia'
import { AuthApi } from '@/api/auth'
import { saveLocalToken, removeLocalToken, getLocalToken } from '@/utils'
import type { UserProfile, AuthState, LoginResults } from '@/interfaces/Auth'
import { computed, ref } from 'vue'
import router from '@/router'
import type { AxiosError } from 'axios'

export const useAuthStore = defineStore('Auth', () => {
  const authState = ref<AuthState>({
    AccessToken: getLocalToken(),
    LoggedIn: false,
    AuthError: false,
    IsAdmin: false,
    User: null,
  })

  const user = computed(() => authState.value.User)
  const isAdmin = computed(() => authState.value.IsAdmin)
  const isLoggedIn = computed(() => authState.value.LoggedIn)
  const authToken = computed(() => authState.value.AccessToken)

  async function createUser(username: string, password: string) {
    await AuthApi.signUp(username, password)
      .then((resp) => {
        return resp
      })
      .then(async () => {
        await login(username, password)
      })
      .catch((err: AxiosError) => {
        throw err
      })
  }

  async function login(username: string, password: string) {
    await AuthApi.login(username, password)
      .then(async (resp: LoginResults) => {
        authState.value.AccessToken = resp.access_token
        authState.value.AuthError = false
        authState.value.LoggedIn = true
        saveLocalToken(resp.access_token)
        return await checkLoggedIn()
      })
      .catch((err) => {
        authState.value.AuthError = true
        removeLocalToken()
        throw err
      })
  }

  async function checkAuth(token: string | null) {
    if (token == null) {
      throw new Error('Authentication Error')
    }
    await AuthApi.checkAuthentication()
      .then((resp: UserProfile) => {
        authState.value.LoggedIn = true
        authState.value.User = resp
        authState.value.IsAdmin = resp.is_admin
        authState.value.AccessToken = token
      })
      .catch((err) => {
        authState.value = {
          AccessToken: '',
          LoggedIn: false,
          AuthError: false,
          IsAdmin: false,
          User: null,
        }
        removeLocalToken()
        throw err
      })
  }

  async function checkLoggedIn() {
    if (!authState.value.LoggedIn) {
      let token = authState.value.AccessToken
      if (!token) {
        const localToken = getLocalToken()
        if (localToken) {
          authState.value.AccessToken = localToken
          token = localToken
        }
      }
      if (token) {
        await checkAuth(token)
      } else {
        removeLocalToken()
        authState.value.LoggedIn = false
        authState.value.User = null
        authState.value.IsAdmin = false
        authState.value.AccessToken = null
      }
    }
  }

  async function logOut() {
    AuthApi.logOut()
      .catch((err) => {
        return err
      })
      .finally(() => {
        removeLocalToken()
        authState.value.LoggedIn = false
        authState.value.User = null
        authState.value.IsAdmin = false
        authState.value.AccessToken = null
        return router.push('/login')
      })
  }

  return {
    authState,
    user,
    isAdmin,
    login,
    checkLoggedIn,
    logOut,
    createUser,
    isLoggedIn,
    authToken,
  }
})
