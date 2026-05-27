import axios from 'axios'

export const useApi = () => {
  const config = useRuntimeConfig()
  
  const getToken = () => {
    if (process.client) {
      return localStorage.getItem('token')
    }
    return null
  }

  const api = axios.create({
    baseURL: config.public.apiBase,
  })

  // attach token every request
  api.interceptors.request.use((config) => {
    const token = getToken()
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  })

  //  token exp - redirect to login
  api.interceptors.response.use(
    (response) => response,
    (error) => {
      if (error.response?.status === 401 && process.client) {
        localStorage.removeItem('token')
        localStorage.removeItem('role')
        window.location.href = '/'
      }
      return Promise.reject(error)
    }
  )

  return { api }
}