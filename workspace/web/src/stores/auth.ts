import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@apis/modules/auth'
import type { UserInfo } from '@types/api'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('access_token'))
  const refreshToken = ref<string | null>(localStorage.getItem('refresh_token'))
  const user = ref<UserInfo | null>(null)

  const isAuthenticated = computed(() => !!token.value)
  const isLoggedIn = computed(() => !!token.value)

  const setToken = (newToken: string, newRefresh?: string) => {
    token.value = newToken
    localStorage.setItem('access_token', newToken)
    if (newRefresh) {
      refreshToken.value = newRefresh
      localStorage.setItem('refresh_token', newRefresh)
    }
  }

  const login = async (username: string, password: string) => {
    const res = await authApi.login({ username, password })
    setToken(res.accessToken, res.refreshToken)
    return res
  }

  const refresh = async () => {
    if (!refreshToken.value) throw new Error('No refresh token')
    const res = await authApi.refresh(refreshToken.value)
    setToken(res.accessToken, res.refreshToken)
    return res
  }

  const logout = () => {
    token.value = null
    refreshToken.value = null
    user.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }

  return {
    token,
    refreshToken,
    user,
    isAuthenticated,
    isLoggedIn,
    setToken,
    login,
    refresh,
    setUser: (userData: UserInfo) => { user.value = userData },
    logout,
  }
})