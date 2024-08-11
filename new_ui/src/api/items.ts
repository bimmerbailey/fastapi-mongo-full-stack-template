import api from '@/api/base'
import type { AxiosError, AxiosResponse } from 'axios'
import type {
  Item,
  ItemUpdate,
  ItemCreate,
  PaginatedReturn,
} from '@/interfaces/Items'

interface GetItem {
  search: string | undefined
  limit: number
  skip: number
}

export const itemApi = {
  async getItems(
    search: string | undefined,
    limit: number = 20,
    offset: number = 0
  ) {
    const getParams = { limit: limit, skip: offset } as GetItem
    if (search !== undefined) {
      getParams['search'] = search
    }
    return await api
      .get('items', { params: getParams })
      .then((resp: AxiosResponse<PaginatedReturn>) => {
        return resp.data
      })
      .catch((err: AxiosError) => {
        throw err
      })
  },
  async deleteItem(ItemId: number) {
    return await api.delete(`items/${ItemId}`).catch((err: AxiosError) => {
      throw err
    })
  },
  async updateItem(ItemId: number, update: ItemUpdate) {
    return await api
      .put(`items/${ItemId}`, update)
      .then((resp: AxiosResponse<Item>) => {
        return resp.data
      })
      .catch((err) => {
        throw err
      })
  },
  async createItem(data: ItemCreate) {
    return await api
      .post('items', { data })
      .then((resp: AxiosResponse<Item>) => {
        return resp.data
      })
      .catch((err) => {
        throw err
      })
  },
  //   TODO: Import bulk from file
}
