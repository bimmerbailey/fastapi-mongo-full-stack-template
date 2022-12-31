export const getLocalToken = () => sessionStorage.getItem('token')

export const saveLocalToken = (token: string) =>
  sessionStorage.setItem('token', token)

export const removeLocalToken = () => sessionStorage.removeItem('token')
