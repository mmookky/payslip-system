import axios from 'axios'

export const useApi = () => {
  const config = useRuntimeConfig()
  const tokenCookie = useCookie('token')
  const roleCookie = useCookie('role')

  const api = axios.create({
    baseURL: config.public.apiBase,
  })

  // attach token every request
  api.interceptors.request.use((cfg) => {
    const token = tokenCookie.value
    if (token) {
      cfg.headers.Authorization = `Bearer ${token}`
    }
    return cfg
  })

  // token exp - redirect to login
  api.interceptors.response.use(
    (response) => response,
    (error) => {
      if (error.response?.status === 401 && process.client) {
        tokenCookie.value = null
        roleCookie.value = null
        window.location.href = '/'
      }
      return Promise.reject(error)
    }
  )

  return { api }
}