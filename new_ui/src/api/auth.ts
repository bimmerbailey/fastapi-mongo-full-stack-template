import type { AxiosError, AxiosResponse } from 'axios'

import api from './base'
import type { LoginResults, User } from '@/interfaces/Auth'

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
  async forgotPassword(email: string) {
    const params = { email: email }

    return await api
      .get('forgot/password', { params })
      .then((resp: AxiosResponse<User>) => {
        return resp.data
      })
      .catch((err) => {
        throw err
      })
  },
  async checkAuthentication() {
    return await api
      .get('authenticated')
      .then((resp: AxiosResponse<User>) => {
        return resp.data
      })
      .catch((err) => {
        throw err
      })
  }
}
