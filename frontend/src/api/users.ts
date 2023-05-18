import api from '@/api/base'
import type { AxiosError, AxiosResponse } from 'axios'
import type { ProfileI } from '@/interfaces/Profile'

export const usersApi = {
  async getUsers() {
    return await api
      .get('users')
      .then((resp: AxiosResponse<ProfileI[]>) => {
        return resp.data
      })
      .catch((err: AxiosError) => {
        throw err
      })
  },
}
