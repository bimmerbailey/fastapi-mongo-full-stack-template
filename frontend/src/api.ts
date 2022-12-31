function authHeaders(token: string) {
  return {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${token}`,
    credentials: 'include',
  }
}

const baseURL = window.location.origin + '/api/v1'

export const AuthApi = {
  async login(email: string, password: string) {
    return await fetch(baseURL + '/login', {
      method: 'post',
      body: new URLSearchParams({ username: email, password: password }),
    })
  },
  async logOut() {
    return await fetch(baseURL + '/logout')
  },
  async signUp(email: string, password: string) {
    return await fetch(baseURL + '/users', {
      headers: {
        'Content-type': 'application/json',
      },
      method: 'post',
      body: JSON.stringify({ email: email, password: password }),
    })
  },
  async forgotPassword(email: string) {
    const url = new URL(baseURL + '/forgot/password')
    url.searchParams.append('email', email)

    return await fetch(url.toString())
      .then((resp) => {
        if (resp.ok) {
          return resp.json()
        } else {
          return resp.text().then((text) => {
            throw JSON.parse(text)
          })
        }
      })
      .catch((err) => {
        throw err
      })
  },
  async checkAuthentication(token: string | null) {
    if (token !== null) {
      return fetch(baseURL + '/authenticated', { headers: authHeaders(token) })
    } else {
      throw Error('Authentication Error')
    }
  },
  async getUsers(token: string | null) {
    if (token !== null) {
      return fetch(baseURL + '/users', { headers: authHeaders(token) })
    } else {
      throw Error('Authentication Error')
    }
  },
}
