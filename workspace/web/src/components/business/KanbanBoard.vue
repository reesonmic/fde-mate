<script setup lang="ts">
import { ref } from 'vue'
import type { TaskDTO } from '@/types/api'

interface Props {
  tasksByStatus: Record<string, TaskDTO[]>
}

const props = defineProps<Props>()

const emit = defineEmits<{
  statusChange: [taskId: number, newStatus: string]
}>()

const columns = [
  { key: 'todo', title: '待办' },
  { key: 'in_progress', title: '进行中' },
  { key: 'review', title: '审核中' },
  { key: 'blocked', title: '阻塞' },
  { key: 'done', title: '完成' },
]

const draggedTask = ref<TaskDTO | null>(null)

const handleDragStart = (task: TaskDTO) => {
  draggedTask.value = task
}

const handleDrop = (status: string) => {
  if (draggedTask.value) {
    emit('statusChange', draggedTask.value.id, status)
    draggedTask.value = null
  }
}
</script>

<template>
  <div class="kanban-board">
    <div class="kanban-columns">
      <div v-for="column in columns" :key="column.key" class="kanban-column">
        <div class="kanban-column-header">
          <h4>{{ column.title }}</h4>
          <span class="kanban-column-count">{{ tasksByStatus[column.key]?.length || 0 }}</span>
        </div>
        <div
          class="kanban-column-body"
          @dragover.prevent
          @drop="handleDrop(column.key)"
        >
          <div
            v-for="task in tasksByStatus[column.key]"
            :key="task.id"
            draggable="true"
            @dragstart="handleDragStart(task)"
          >
            <KanbanCard :task="task" />
          </div>
          <div v-if="!tasksByStatus[column.key]?.length" class="kanban-column-empty">
            暂无任务
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.kanban-board {
  height: 100%;
}

.kanban-columns {
  display: flex;
  gap: 16px;
  height: 100%;
}

.kanban-column {
  flex: 1;
  min-width: 280px;
  background: var(--color-fill-secondary);
  border-radius: 8px;
  overflow: hidden;
}

.kanban-column-header {
  display: flex;
  justify-content: space-between;
  padding: 12px 16px;
  background: var(--color-bg-elevated);
  border-bottom: 1px solid var(--color-border);
}

.kanban-column-header h4 {
  margin: 0;
  font-size: 14px;
}

.kanban-column-count {
  font-size: 12px;
  color: var(--color-text-secondary);
}

.kanban-column-body {
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  min-height: 200px;
}

.kanban-column-empty {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  color: var(--color-text-secondary);
  font-size: 14px;
}
</style>