"""Tests for TaskRow component."""
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import TaskRow from '@/components/business/TaskRow.vue'

describe('TaskRow Component', () => {
  it('should render task title', () => {
    const task = {
      id: 'task-1',
      title: 'Test Task',
      status: 'todo',
      priority: 'p1',
      assignee: { name: 'Test User' },
      due_at: '2026-05-01',
    }
    const wrapper = mount(TaskRow, {
      props: { task },
    })

    expect(wrapper.text()).toContain('Test Task')
  })

  it('should render status badge', () => {
    const task = {
      id: 'task-1',
      title: 'Test Task',
      status: 'in_progress',
      priority: 'p2',
    }
    const wrapper = mount(TaskRow, {
      props: { task },
    })

    expect(wrapper.find('.status-badge').exists()).toBe(true)
  })

  it('should emit click event', async () => {
    const task = {
      id: 'task-1',
      title: 'Test Task',
      status: 'todo',
      priority: 'p1',
    }
    const wrapper = mount(TaskRow, {
      props: { task },
    })

    await wrapper.trigger('click')
    expect(wrapper.emitted('click')).toBeTruthy()
  })
})
