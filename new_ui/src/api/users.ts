import api from '@/api/base'
import type { AxiosError, AxiosResponse } from 'axios'
import type { UserProfile } from '@/interfaces/Profile'

export const usersApi = {
  async getUsers() {
    return await api
      .get('users')
      .then((resp: AxiosResponse<UserProfile[]>) => {
        return resp.data
      })
      .catch((err: AxiosError) => {
        throw err
      })
  }
}
