"""Tests for useMention composable."""
import { describe, it, expect, beforeEach, vi } from 'vitest'
import { useMention } from '@/composables/useMention'

describe('useMention Composable', () => {
  beforeEach(() => {
    vi.resetModules()
  })

  describe('TC-MENTION-COMP-001: Initial state', () => {
    it('should initialize with empty mentions', () => {
      const mention = useMention()
      expect(mention.getMentions()).toEqual([])
    })
  })

  describe('TC-MENTION-COMP-002: Add mention', () => {
    it('should add a mention', () => {
      const mention = useMention()
      const item = { type: 'task', id: 1, name: 'Test Task' }
      mention.addMention(item)

      expect(mention.getMentions()).toContain(item)
    })

    it('should not add duplicate mentions', () => {
      const mention = useMention()
      const item = { type: 'task', id: 1, name: 'Test Task' }
      mention.addMention(item)
      mention.addMention(item)

      expect(mention.getMentions().length).toBe(1)
    })
  })

  describe('TC-MENTION-COMP-003: Clear mentions', () => {
    it('should clear all mentions', () => {
      const mention = useMention()
      mention.addMention({ type: 'task', id: 1, name: 'Task 1' })
      mention.addMention({ type: 'project', id: 2, name: 'Project 1' })

      mention.clearMentions()

      expect(mention.getMentions()).toEqual([])
    })
  })
})
