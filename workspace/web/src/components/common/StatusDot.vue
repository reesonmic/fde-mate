<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  status: 'success' | 'warning' | 'error' | 'info' | 'default'
  size?: 'small' | 'medium' | 'large'
}

const props = withDefaults(defineProps<Props>(), {
  size: 'medium',
})

const statusColor = computed(() => {
  const colors: Record<string, string> = {
    success: 'var(--color-success)',
    warning: 'var(--color-warning)',
    error: 'var(--color-error)',
    info: 'var(--color-info)',
    default: 'var(--color-text-secondary)',
  }
  return colors[props.status]
})

const dotSize = computed(() => {
  const sizes: Record<string, number> = {
    small: 6,
    medium: 8,
    large: 10,
  }
  return sizes[props.size]
})
</script>

<template>
  <span
    class="status-dot"
    :style="{
      width: `${dotSize}px`,
      height: `${dotSize}px`,
      backgroundColor: statusColor,
    }"
  />
</template>

<style scoped>
.status-dot {
  display: inline-block;
  border-radius: 50%;
}
</style>