<script setup lang="ts">
import { computed } from 'vue'
import { Tag, Progress, Button } from 'ant-design-vue'
import StatusDot from '@/components/common/StatusDot.vue'
import type { ProjectDTO } from '@/types/api'

interface Props {
  project: ProjectDTO
}

const props = defineProps<Props>()

const statusColor = computed(() => {
  const colors: Record<string, 'success' | 'warning' | 'error' | 'info' | 'default'> = {
    active: 'info',
    completed: 'success',
    paused: 'warning',
    archived: 'default',
  }
  return colors[props.project.status] || 'default'
})
</script>

<template>
  <div class="project-header">
    <div class="project-header-main">
      <StatusDot :status="statusColor" />
      <h3 class="project-header-title">{{ project.name }}</h3>
      <Tag>{{ project.status }}</Tag>
    </div>
    <div class="project-header-progress">
      <Progress :percent="project.progress" :size="120" />
    </div>
    <div class="project-header-actions">
      <Button type="primary">编辑</Button>
      <Button>更多</Button>
    </div>
  </div>
</template>

<style scoped>
.project-header {
  display: flex;
  align-items: center;
  gap: 24px;
  padding: 24px;
  background: var(--color-bg-elevated);
  border-radius: 8px;
}

.project-header-main {
  display: flex;
  align-items: center;
  gap: 12px;
}

.project-header-title {
  margin: 0;
  font-size: 20px;
}

.project-header-progress {
  flex: 1;
}

.project-header-actions {
  display: flex;
  gap: 8px;
}
</style>