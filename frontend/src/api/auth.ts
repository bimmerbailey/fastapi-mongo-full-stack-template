import type { AxiosError, AxiosResponse } from 'axios'

import api from './base'
import type { LoginResults } from '@/interfaces/Auth'

export const AuthApi = {
  async login(email: string, password: string) {
    const params = new URLSearchParams({ username: email, password: password })
    return await api
      .post('login', params)
      .then((resp: AxiosResponse<LoginResults>) => {
        return resp.data
      })
      .catch((err: AxiosError) => {
        throw err
      })
  },
  async logOut() {
    return api.get('logout').catch((err) => {
      throw err
    })
  },
  async signUp(email: string, password: string) {
    return await api
      .post('users', { email: email, password: password })
      .then((resp) => {
        return resp.data
      })
      .catch((err) => {
        throw err
      })
  },
  async forgotPassword(email: string) {
    const params = { email: email }

    return await api
      .get('forgot/password', { params })
      .then((resp) => {
        return resp.data
      })
      .catch((err) => {
        throw err
      })
  },
  async checkAuthentication() {
    return await api
      .get('authenticated')
      .then((resp) => {
        return resp.data
      })
      .catch((err) => {
        throw err
      })
  },
}
