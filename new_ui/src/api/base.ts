import axios, { AxiosError } from 'axios'
import { useAuthStore } from '@/stores/authentication'

export interface RequestError {
  detail?: string
}

const api = axios.create({
  baseURL: window.location.origin + '/api/v1'
})

api.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()
    if (authStore.authToken) {
      config.headers.Authorization = `Bearer ${authStore.authToken}`
    }
    return config
  },
  (error: AxiosError<RequestError>) => {
    console.log('Request Error', error)
    return Promise.reject(error)
  }
)

export default api
