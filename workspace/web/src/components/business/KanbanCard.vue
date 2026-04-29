<script setup lang="ts">
import { computed } from 'vue'
import { Tag, Avatar } from 'ant-design-vue'
import StatusDot from '@/components/common/StatusDot.vue'
import type { TaskDTO } from '@/types/api'

interface Props {
  task: TaskDTO
}

const props = defineProps<Props>()

const priorityColor = computed(() => {
  const colors: Record<string, string> = {
    high: 'red',
    medium: 'orange',
    low: 'blue',
  }
  return colors[props.task.priority] || 'default'
})

const statusColor = computed(() => {
  const colors: Record<string, 'success' | 'warning' | 'error' | 'info' | 'default'> = {
    done: 'success',
    in_progress: 'info',
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
      <Tag :color="priorityColor">{{ task.priority }}</Tag>
      <Avatar v-if="task.assignee" :src="task.assignee?.avatar" :size="24">
        {{ task.assignee?.name?.charAt(0) }}
      </Avatar>
    </div>
    <div class="kanban-card-footer">
      <span v-if="task.deadline" class="kanban-card-deadline">{{ task.deadline }}</span>
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