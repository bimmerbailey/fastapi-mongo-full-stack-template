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

export interface AuthState {
  AccessToken: string | null
  LoggedIn: boolean
  AuthError: boolean
  IsAdmin: boolean
  User: UserProfile | null
}
