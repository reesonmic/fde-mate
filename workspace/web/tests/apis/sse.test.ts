"""Tests for SSE client."""
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { openSse, SSEClient } from '@/apis/sse'

describe('SSE Client', () => {
  beforeEach(() => {
    vi.restoreAllMocks()
  })

  describe('TC-SSE-001: SSEClient class', () => {
    it('should create SSEClient instance', () => {
      const client = new SSEClient('http://localhost:8090/ai/chat')
      expect(client).toBeTruthy()
    })

    it('should report disconnected initially', () => {
      const client = new SSEClient('http://localhost:8090/ai/chat')
      expect(client.isConnected()).toBe(false)
    })
  })

  describe('TC-SSE-002: openSse function', () => {
    it('should return AbortController', () => {
      // Mock fetch
      vi.stubGlobal('fetch', vi.fn().mockResolvedValue({
        ok: true,
        body: {
          getReader: () => ({
            read: vi.fn().mockResolvedValue({ done: true, value: null }),
          }),
        },
      }))

      const controller = openSse({
        url: '/copilot/chat',
        body: { message: 'test' },
        onMessage: vi.fn(),
        onDone: vi.fn(),
      })

      expect(controller).toBeTruthy()
      expect(controller.abort).toBeTruthy()
    })
  })
})
