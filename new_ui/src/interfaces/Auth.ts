export interface LoginResults {
  access_token: string
  token_type: string
  is_admin: boolean
}

export interface UserProfile {
  email: string
  is_admin: boolean
  id: string
}

export interface User {
  first_name: string
  last_name: string
  email: string
  is_admin: boolean
}
