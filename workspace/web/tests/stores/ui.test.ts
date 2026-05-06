"""Tests for UI store."""
import { describe, it, expect, beforeEach } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { useUiStore } from '@/stores/ui'

describe('UI Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  describe('TC-UI-FE-001: Initial state', () => {
    it('should initialize with light theme', () => {
      const store = useUiStore()
      expect(store.theme).toBe('light')
    })

    it('should initialize with nav not collapsed', () => {
      const store = useUiStore()
      expect(store.navCollapsed).toBe(false)
    })

    it('should initialize with copilot open', () => {
      const store = useUiStore()
      expect(store.copilotOpen).toBe(true)
    })
  })

  describe('TC-UI-FE-002: Toggle theme', () => {
    it('should toggle from light to dark', () => {
      const store = useUiStore()
      store.toggleTheme()

      expect(store.theme).toBe('dark')
    })

    it('should toggle from dark to light', () => {
      const store = useUiStore()
      store.theme = 'dark'
      store.toggleTheme()

      expect(store.theme).toBe('light')
    })
  })

  describe('TC-UI-FE-003: Toggle copilot', () => {
    it('should toggle copilot open/close', () => {
      const store = useUiStore()
      store.toggleCopilot()

      expect(store.copilotOpen).toBe(false)
    })
  })

  describe('TC-UI-FE-004: Toggle nav', () => {
    it('should toggle nav collapsed', () => {
      const store = useUiStore()
      store.toggleNav()

      expect(store.navCollapsed).toBe(true)
    })
  })
})
