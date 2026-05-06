"""Tests for chat store."""
import { describe, it, expect, beforeEach } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { useChatStore } from '@/stores/chat'

describe('Chat Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  describe('TC-CHAT-FE-001: Initial state', () => {
    it('should initialize with empty messages', () => {
      const store = useChatStore()
      expect(store.messages).toEqual([])
    })

    it('should initialize with free mode', () => {
      const store = useChatStore()
      expect(store.mode).toBe('free')
    })

    it('should initialize with session ID', () => {
      const store = useChatStore()
      expect(store.sessionId).toBeTruthy()
    })
  })

  describe('TC-CHAT-FE-002: Add message', () => {
    it('should add message to store', () => {
      const store = useChatStore()
      store.addMessage({
        id: 'msg-1',
        content: 'Hello',
        role: 'user',
        timestamp: new Date().toISOString(),
        type: 'text',
      })

      expect(store.messages.length).toBe(1)
    })
  })

  describe('TC-CHAT-FE-003: Clear messages', () => {
    it('should clear all messages and reset session', () => {
      const store = useChatStore()
      store.addMessage({
        id: 'msg-1',
        content: 'Hello',
        role: 'user',
        timestamp: new Date().toISOString(),
        type: 'text',
      })

      const oldSessionId = store.sessionId
      store.clearMessages()

      expect(store.messages).toEqual([])
      expect(store.sessionId).not.toBe(oldSessionId)
    })
  })

  describe('TC-CHAT-FE-004: Mode switching', () => {
    it('should switch between modes', () => {
      const store = useChatStore()
      store.setMode('task')
      expect(store.mode).toBe('task')

      store.setMode('report')
      expect(store.mode).toBe('report')

      store.setMode('free')
      expect(store.mode).toBe('free')
    })
  })

  describe('TC-CHAT-FE-005: References', () => {
    it('should add unique references', () => {
      const store = useChatStore()
      store.addReference({ id: 1, name: 'Project A' })
      store.addReference({ id: 2, name: 'Task B' })

      expect(store.references.length).toBe(2)
    })

    it('should not add duplicate references', () => {
      const store = useChatStore()
      store.addReference({ id: 1, name: 'Project A' })
      store.addReference({ id: 1, name: 'Project A' })

      expect(store.references.length).toBe(1)
    })

    it('should remove reference', () => {
      const store = useChatStore()
      store.addReference({ id: 1, name: 'Project A' })
      store.removeReference('1')

      expect(store.references.length).toBe(0)
    })

    it('should clear all references', () => {
      const store = useChatStore()
      store.addReference({ id: 1, name: 'Project A' })
      store.addReference({ id: 2, name: 'Task B' })

      store.clearReferences()

      expect(store.references).toEqual([])
    })
  })
})
