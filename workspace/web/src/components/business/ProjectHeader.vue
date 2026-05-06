<script setup lang="ts">
import { computed } from 'vue'
import { Tag, Progress, Button } from 'ant-design-vue'
import type { ProjectDTO } from '@/types/business'

interface Props {
  project: ProjectDTO
}

const props = defineProps<Props>()

const phaseColor = computed(() => {
  const colors: Record<string, string> = {
    init: 'default',
    discovery: 'processing',
    delivery: 'blue',
    review: 'cyan',
    closed: 'default',
  }
  return colors[props.project.phase] || 'default'
})

const phaseLabel = computed(() => {
  const labels: Record<string, string> = {
    init: '初始化',
    discovery: '探索',
    delivery: '交付',
    review: '审核',
    closed: '关闭',
  }
  return labels[props.project.phase] || props.project.phase
})
</script>

<template>
  <div class="project-header">
    <div class="project-header-main">
      <h3 class="project-header-title">{{ project.name }}</h3>
      <Tag :color="phaseColor">{{ phaseLabel }}</Tag>
      <Tag v-if="project.owner_name">{{ project.owner_name }}</Tag>
    </div>
    <div class="project-header-health">
      <span>健康度</span>
      <span :style="{ color: project.health >= 80 ? '#52c41a' : project.health >= 60 ? '#faad14' : '#ff4d4f', fontWeight: 600 }">
        {{ project.health }}%
      </span>
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

.project-header-health {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: var(--color-text-secondary);
}

.project-header-actions {
  display: flex;
  gap: 8px;
}
</style>