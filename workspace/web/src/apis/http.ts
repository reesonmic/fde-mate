import axios, { type AxiosInstance, type InternalAxiosRequestConfig } from 'axios'
import { message } from 'ant-design-vue'
import { useAuthStore } from '@stores/auth'
import router from '@/router'

export const http: AxiosInstance = axios.create({
  baseURL: '/api/v1',
  timeout: 15000,
  headers: { 'Content-Type': 'application/json' },
})

let isRefreshing = false
let pendingQueue: Array<(t: string) => void> = []

export function setupAxiosInterceptors() {
  http.interceptors.request.use((config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem('access_token')
    if (token) config.headers.Authorization = `Bearer ${token}`
    config.headers['X-Request-Id'] = crypto.randomUUID?.() || Date.now().toString(36) + Math.random().toString(36).slice(2)
    return config
  })

  http.interceptors.response.use(
    (resp) => {
      const { code, data, message: msg } = resp.data
      if (code !== undefined && code !== 0) {
        // Handle business-level authentication errors (code 2001, 2002)
        if (code === 2001 || code === 2002) {
          // Authentication failed or token expired
          const auth = useAuthStore()
          auth.logout()
          // Redirect to login page with current path as redirect query
          const currentPath = window.location.pathname + window.location.search
          router.push(`/login?redirect=${encodeURIComponent(currentPath)}`)
          return Promise.reject({ code, message: msg })
        }
        return Promise.reject({ code, message: msg })
      }
      // If API wraps response in {code, data}, unwrap it; otherwise return resp.data directly
      return data !== undefined ? data : resp.data
    },
    async (err) => {
      const status = err.response?.status
      if (status === 401) {
        const auth = useAuthStore()
        if (!auth.token) { router.push('/login'); return Promise.reject(err) }
        if (isRefreshing) {
          return new Promise((resolve, reject) => {
            // Add 30s timeout for pending requests
            const timeout = setTimeout(() => {
              reject(new Error('Token refresh timeout'))
            }, 30000)
            
            pendingQueue.push((t) => {
              clearTimeout(timeout)
              err.config.headers.Authorization = `Bearer ${t}`
              resolve(http(err.config))
            })
          })
        }
        isRefreshing = true
        try {
          // Add 30s timeout for token refresh
          const refreshPromise = auth.refresh()
          const timeoutPromise = new Promise((_, reject) => 
            setTimeout(() => reject(new Error('刷新超时')), 30000)
          )
          await Promise.race([refreshPromise, timeoutPromise])
          
          pendingQueue.forEach((cb) => cb(auth.token!))
          pendingQueue = []
          err.config.headers.Authorization = `Bearer ${auth.token}`
          return http(err.config)
        } catch {
          auth.logout(); router.push('/login'); return Promise.reject(err)
        } finally { isRefreshing = false }
      }
      message.error(err.response?.data?.message || err.message || '网络错误')
      return Promise.reject(err)
    },
  )
}
