import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { authApi } from '@/apis/modules/auth'

/**
 * Auth composable for authentication operations
 */
export function useAuth() {
  const router = useRouter()
  const authStore = useAuthStore()

  const isAuthenticated = computed(() => authStore.isAuthenticated)

  const currentUser = computed(() => authStore.user)

  const login = async (username: string, password: string) => {
    try {
      const response = await authApi.login({ username, password })
      authStore.setToken(response.token)
      authStore.setUser(response.user)
      router.push('/dashboard')
    } catch (error) {
      throw error
    }
  }

  const logout = async () => {
    try {
      await authApi.logout()
    } finally {
      authStore.logout()
      router.push('/login')
    }
  }

  const checkAuth = async () => {
    if (!authStore.token) {
      return false
    }

    try {
      const user = await authApi.getCurrentUser()
      authStore.setUser(user)
      return true
    } catch {
      authStore.logout()
      return false
    }
  }

  return {
    isAuthenticated,
    currentUser,
    login,
    logout,
    checkAuth,
  }
}