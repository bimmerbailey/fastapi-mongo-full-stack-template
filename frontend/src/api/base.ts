import axios, { AxiosError } from 'axios'
import { useAuthStore } from '@/stores/auth'

const api = axios.create({
  baseURL: window.location.origin + '/api/v1',
})

api.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()
    if (authStore.authToken) {
      config.headers.Authorization = `Bearer ${authStore.authToken}`
    }
    return config
  },
  (error: AxiosError) => {
    return Promise.reject(error)
  }
)

export default api
