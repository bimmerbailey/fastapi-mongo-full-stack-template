import api from '@/api/base'

export const usersApi = {
  async getUsers() {
    return await api
      .get('users')
      .then((resp) => {
        return resp.data
      })
      .catch((err) => {
        throw err
      })
  },
}
