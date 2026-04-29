<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  value: number // 0-100
  size?: 'small' | 'medium' | 'large'
  color?: 'green' | 'yellow' | 'red' | 'blue'
}

const props = withDefaults(defineProps<Props>(), {
  size: 'medium',
  color: 'green',
})

const strokeWidth = computed(() => {
  const widths = { small: 4, medium: 6, large: 8 }
  return widths[props.size]
})

const radius = computed(() => {
  const radii = { small: 40, medium: 60, large: 80 }
  return radii[props.size]
})

const circumference = computed(() => 2 * Math.PI * radius.value)

const progressOffset = computed(() => {
  return circumference.value - (props.value / 100) * circumference.value
})

const colorClass = computed(() => `health-ring--${props.color}`)
</script>

<template>
  <div class="health-ring" :class="[`health-ring--${size}`, colorClass]">
    <svg :width="radius * 2 + strokeWidth" :height="radius * 2 + strokeWidth">
      <!-- Background circle -->
      <circle
        :cx="radius + strokeWidth / 2"
        :cy="radius + strokeWidth / 2"
        :r="radius"
        :stroke-width="strokeWidth"
        fill="none"
        class="health-ring-bg"
      />
      <!-- Progress circle -->
      <circle
        :cx="radius + strokeWidth / 2"
        :cy="radius + strokeWidth / 2"
        :r="radius"
        :stroke-width="strokeWidth"
        fill="none"
        :stroke-dasharray="circumference"
        :stroke-dashoffset="progressOffset"
        stroke-linecap="round"
        class="health-ring-progress"
      />
    </svg>
    <span class="health-ring-value">{{ value }}%</span>
  </div>
</template>

<style scoped>
.health-ring {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.health-ring-bg {
  stroke: var(--color-border);
}

.health-ring-progress {
  transform: rotate(-90deg);
  transform-origin: center;
  transition: stroke-dashoffset 0.3s ease;
}

.health-ring-value {
  position: absolute;
  font-weight: 600;
}

.health-ring--green .health-ring-progress {
  stroke: var(--color-success);
}

.health-ring--yellow .health-ring-progress {
  stroke: var(--color-warning);
}

.health-ring--red .health-ring-progress {
  stroke: var(--color-error);
}

.health-ring--blue .health-ring-progress {
  stroke: var(--color-primary);
}

.health-ring--small .health-ring-value {
  font-size: 12px;
}

.health-ring--medium .health-ring-value {
  font-size: 16px;
}

.health-ring--large .health-ring-value {
  font-size: 20px;
}
</style>