"""Tests for composable useAuth."""
import { describe, it, expect, beforeEach } from 'vitest'
import { useAuth } from '@/composables/useAuth'

describe('useAuth Composable', () => {
  beforeEach(() => {
    vi.resetModules()
  })

  describe('TC-AUTH-COMP-001: Initial state', () => {
    it('should return auth composable', () => {
      const auth = useAuth()
      expect(auth).toBeTruthy()
      expect(typeof auth.checkAuth).toBe('function')
    })
  })

  describe('TC-AUTH-COMP-002: Check auth', () => {
    it('should return false when no token', () => {
      const auth = useAuth()
      expect(auth.checkAuth()).toBe(false)
    })
  })
})
