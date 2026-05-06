<script setup lang="ts">
import { computed } from 'vue'
import { Tag } from 'ant-design-vue'
import StatusDot from '@/components/common/StatusDot.vue'
import type { TaskDTO } from '@/types/business'

interface Props {
  task: TaskDTO
}

const props = defineProps<Props>()

const priorityColor = computed(() => {
  const colors: Record<string, string> = {
    p0: 'red',
    p1: 'orange',
    p2: 'blue',
    p3: 'default',
  }
  return colors[props.task.priority] || 'default'
})

const priorityLabel = computed(() => {
  const labels: Record<string, string> = {
    p0: 'P0',
    p1: 'P1',
    p2: 'P2',
    p3: 'P3',
  }
  return labels[props.task.priority] || props.task.priority
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
</script>

<template>
  <div class="kanban-card">
    <div class="kanban-card-header">
      <StatusDot :status="statusColor" />
      <span class="kanban-card-title">{{ task.title }}</span>
    </div>
    <div class="kanban-card-meta">
      <Tag :color="priorityColor">{{ priorityLabel }}</Tag>
    </div>
    <div class="kanban-card-footer">
      <span v-if="task.dueAt" class="kanban-card-deadline">{{ task.dueAt?.substring(0, 10) }}</span>
    </div>
  </div>
</template>

<style scoped>
.kanban-card {
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  padding: 12px;
  cursor: pointer;
}

.kanban-card:hover {
  border-color: var(--color-primary);
}

.kanban-card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.kanban-card-title {
  font-size: 14px;
  font-weight: 500;
}

.kanban-card-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.kanban-card-footer {
  font-size: 12px;
  color: var(--color-text-secondary);
}

.kanban-card-deadline {
  color: var(--color-warning);
}
</style>