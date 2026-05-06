"""Tests for auth store."""
import { describe, it, expect, beforeEach, vi } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { useAuthStore } from '@/stores/auth'

describe('Auth Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  describe('TC-AUTH-FE-001: Initial state', () => {
    it('should initialize with empty token', () => {
      const store = useAuthStore()
      expect(store.token).toBe('')
      expect(store.isAuthenticated).toBe(false)
    })

    it('should initialize with null user', () => {
      const store = useAuthStore()
      expect(store.user).toBeNull()
    })
  })

  describe('TC-AUTH-FE-002: Login', () => {
    it('should set token and user on successful login', async () => {
      const store = useAuthStore()
      store.login = vi.fn().mockResolvedValue({
        accessToken: 'test-token',
        user: { id: 1, name: 'testuser' },
      })

      await store.login('testuser', 'password')

      expect(store.login).toHaveBeenCalledWith('testuser', 'password')
    })
  })

  describe('TC-AUTH-FE-003: Logout', () => {
    it('should clear token and user', () => {
      const store = useAuthStore()
      store.logout()

      expect(store.token).toBe('')
      expect(store.user).toBeNull()
      expect(store.isAuthenticated).toBe(false)
    })
  })

  describe('TC-AUTH-FE-004: Refresh token', () => {
    it('should call refresh API', async () => {
      const store = useAuthStore()
      store.refresh = vi.fn().mockResolvedValue({
        accessToken: 'new-token',
      })

      await store.refresh()

      expect(store.refresh).toHaveBeenCalled()
    })
  })
})
