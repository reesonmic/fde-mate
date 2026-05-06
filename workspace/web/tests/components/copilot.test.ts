"""Tests for Copilot components."""
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import MessageRenderer from '@/components/copilot/MessageRenderer.vue'
import ChatInput from '@/components/copilot/ChatInput.vue'
import ActionCard from '@/components/copilot/cards/ActionCard.vue'

describe('MessageRenderer Component', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('should render user message', () => {
    const wrapper = mount(MessageRenderer, {
      props: {
        message: {
          id: 'msg-1',
          content: 'Hello',
          role: 'user',
          timestamp: new Date().toISOString(),
          type: 'text',
        },
        assistantType: 'chat',
      },
    })

    expect(wrapper.text()).toContain('Hello')
  })

  it('should render assistant text message', () => {
    const wrapper = mount(MessageRenderer, {
      props: {
        message: {
          id: 'msg-2',
          content: 'Hi there!',
          role: 'assistant',
          timestamp: new Date().toISOString(),
          type: 'text',
        },
        assistantType: 'chat',
      },
    })

    expect(wrapper.text()).toContain('Hi there!')
  })

  it('should render action card', () => {
    const wrapper = mount(MessageRenderer, {
      props: {
        message: {
          id: 'msg-3',
          content: '',
          role: 'assistant',
          timestamp: new Date().toISOString(),
          type: 'action',
          metadata: {
            actionId: 'test-action',
            toolName: 'update_task',
            params: { status: 'done' },
            preview: 'Update task status',
          },
        },
        assistantType: 'task',
      },
    })

    expect(wrapper.find('.action-card').exists()).toBe(true)
  })
})

describe('ChatInput Component', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('should render input field', () => {
    const wrapper = mount(ChatInput, {
      props: { assistantType: 'chat' },
    })

    expect(wrapper.exists()).toBe(true)
  })

  it('should emit send on Enter', async () => {
    const wrapper = mount(ChatInput, {
      props: { assistantType: 'chat' },
    })

    const input = wrapper.find('textarea')
    await input.setValue('Test message')
    await input.trigger('keydown', { key: 'Enter' })

    expect(wrapper.emitted('send')).toBeTruthy()
    expect(wrapper.emitted('send')[0]).toEqual(['Test message', []])
  })

  it('should not emit send for empty message', async () => {
    const wrapper = mount(ChatInput, {
      props: { assistantType: 'chat' },
    })

    const input = wrapper.find('textarea')
    await input.setValue('')
    await input.trigger('keydown', { key: 'Enter' })

    expect(wrapper.emitted('send')).toBeFalsy()
  })
})

describe('ActionCard Component', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.useFakeTimers()
  })

  it('should render action details', () => {
    const wrapper = mount(ActionCard, {
      props: {
        action: {
          actionId: 'test-action',
          toolName: 'update_task',
          params: { status: 'done' },
          preview: 'Update task status to done',
        },
        assistantType: 'task',
      },
    })

    expect(wrapper.text()).toContain('update_task')
    expect(wrapper.text()).toContain('确认执行')
  })

  it('should emit confirm on button click', async () => {
    const wrapper = mount(ActionCard, {
      props: {
        action: {
          actionId: 'test-action',
          toolName: 'update_task',
          params: {},
          preview: 'Test',
        },
        assistantType: 'task',
      },
    })

    await wrapper.findAll('button')[0].trigger('click')

    expect(wrapper.emitted('click')).toBeTruthy()
  })

  afterEach(() => {
    vi.useRealTimers()
  })
})
