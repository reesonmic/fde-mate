"""Tests for copilot store."""
import { describe, it, expect, beforeEach } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { useCopilotStore } from '@/stores/copilot'

describe('Copilot Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  describe('TC-COP-FE-001: Initial state', () => {
    it('should initialize with empty messages', () => {
      const store = useCopilotStore()
      expect(store.getMessages('task')).toEqual([])
      expect(store.getMessages('project')).toEqual([])
      expect(store.getMessages('coach')).toEqual([])
      expect(store.getMessages('file')).toEqual([])
    })

    it('should initialize with session IDs', () => {
      const store = useCopilotStore()
      expect(store.getSessionId('task')).toBeTruthy()
      expect(store.getSessionId('project')).toBeTruthy()
    })

    it('should initialize with null pending action', () => {
      const store = useCopilotStore()
      expect(store.pendingAction).toBeNull()
    })
  })

  describe('TC-COP-FE-002: Add message', () => {
    it('should add user message', () => {
      const store = useCopilotStore()
      store.addMessage('task', {
        id: 'msg-1',
        content: 'Hello',
        role: 'user',
        timestamp: new Date().toISOString(),
        type: 'text',
      })

      const messages = store.getMessages('task')
      expect(messages.length).toBe(1)
      expect(messages[0].content).toBe('Hello')
      expect(messages[0].role).toBe('user')
    })

    it('should add assistant message', () => {
      const store = useCopilotStore()
      store.addMessage('task', {
        id: 'msg-2',
        content: 'Hi there!',
        role: 'assistant',
        timestamp: new Date().toISOString(),
        type: 'text',
      })

      const messages = store.getMessages('task')
      expect(messages.length).toBe(1)
      expect(messages[0].role).toBe('assistant')
    })
  })

  describe('TC-COP-FE-003: Clear session', () => {
    it('should clear messages for specific assistant', () => {
      const store = useCopilotStore()
      store.addMessage('task', {
        id: 'msg-1',
        content: 'Hello',
        role: 'user',
        timestamp: new Date().toISOString(),
        type: 'text',
      })

      store.clearSession('task')

      expect(store.getMessages('task')).toEqual([])
    })

    it('should not affect other assistants', () => {
      const store = useCopilotStore()
      store.addMessage('project', {
        id: 'msg-2',
        content: 'Project msg',
        role: 'user',
        timestamp: new Date().toISOString(),
        type: 'text',
      })

      store.clearSession('task')

      expect(store.getMessages('project').length).toBe(1)
    })
  })

  describe('TC-COP-FE-004: Cancel action', () => {
    it('should clear pending action', () => {
      const store = useCopilotStore()
      store.pendingAction = { actionId: 'test-action' }

      store.cancelAction('test-action')

      expect(store.pendingAction).toBeNull()
    })
  })

  describe('TC-COP-FE-005: Send message', () => {
    it('should add user message before API call', async () => {
      const store = useCopilotStore()

      // Mock the copilotApi
      vi.mock('@/apis/modules/copilot', () => ({
        copilotApi: {
          chat: vi.fn(() => {}),
        },
      }))

      await store.sendMessage('task', 'Test message')

      const messages = store.getMessages('task')
      expect(messages.length).toBe(2) // user + assistant (empty)
      expect(messages[0].role).toBe('user')
      expect(messages[0].content).toBe('Test message')
    })
  })
})
