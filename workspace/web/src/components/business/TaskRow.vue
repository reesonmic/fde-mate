<script setup lang="ts">
import { computed } from 'vue'
import { Tag, Avatar, Checkbox } from 'ant-design-vue'
import StatusDot from '@/components/common/StatusDot.vue'
import type { TaskDTO } from '@/types/business'

interface Props {
  task: TaskDTO
  selected?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  selected: false,
})

const emit = defineEmits<{
  select: [id: number]
  click: [id: number]
}>()

const priorityLabel = computed(() => {
  const labels: Record<string, string> = {
    p0: 'P0',
    p1: 'P1',
    p2: 'P2',
    p3: 'P3',
  }
  return labels[props.task.priority] || props.task.priority
})

const priorityColor = computed(() => {
  const colors: Record<string, string> = {
    p0: 'red',
    p1: 'orange',
    p2: 'blue',
    p3: 'default',
  }
  return colors[props.task.priority] || 'default'
})

const statusColor = computed(() => {
  const colors: Record<string, 'success' | 'warning' | 'error' | 'info' | 'default'> = {
    done: 'success',
    in_progress: 'info',
    review: 'cyan',
    todo: 'default',
    blocked: 'error',
  }
  return colors[props.task.status] || 'default'
})

const handleSelect = (checked: boolean) => {
  emit('select', props.task.id)
}

const handleClick = () => {
  emit('click', props.task.id)
}
</script>

<template>
  <div class="task-row" :class="{ 'task-row--selected': selected }" @click="handleClick">
    <Checkbox :checked="selected" @change="handleSelect" />
    <StatusDot :status="statusColor" />
    <span class="task-row-title">{{ task.title }}</span>
    <div class="task-row-meta">
      <Tag :color="priorityColor">{{ priorityLabel }}</Tag>
      <span v-if="task.dueAt" class="task-row-deadline">{{ task.dueAt }}</span>
    </div>
  </div>
</template>

<style scoped>
.task-row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border);
  border-radius: 4px;
  cursor: pointer;
}

.task-row:hover {
  border-color: var(--color-primary);
}

.task-row--selected {
  background: var(--color-primary-bg);
  border-color: var(--color-primary);
}

.task-row-title {
  flex: 1;
  font-size: 14px;
}

.task-row-meta {
  display: flex;
  align-items: center;
  gap: 8px;
}

.task-row-deadline {
  font-size: 12px;
  color: var(--color-text-secondary);
}
</style>