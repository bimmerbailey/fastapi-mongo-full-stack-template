export interface Item {
  id: string
  cost: number
  name: string
  description: string
  quantity: number
}

export interface PaginatedReturn {
  items: Array<Item>
  count: number
}

export interface ItemUpdate {
  cost: number | null
  name: string | null
  description: string | null
  quantity: number | null
}

export interface ItemCreate {
  cost: number
  name: string
  description: string
  quantity: number
}
