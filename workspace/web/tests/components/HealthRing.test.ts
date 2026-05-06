"""Tests for HealthRing component."""
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import HealthRing from '@/components/common/HealthRing.vue'

describe('HealthRing Component', () => {
  it('should render with value', () => {
    const wrapper = mount(HealthRing, {
      props: { value: 80 },
    })

    expect(wrapper.text()).toContain('80')
  })

  it('should render with size', () => {
    const wrapper = mount(HealthRing, {
      props: { value: 60, size: 64 },
    })

    expect(wrapper.exists()).toBe(true)
  })

  it('should clamp value to 0-100', () => {
    const wrapper = mount(HealthRing, {
      props: { value: 150 },
    })

    expect(wrapper.text()).toContain('100')
  })
})
