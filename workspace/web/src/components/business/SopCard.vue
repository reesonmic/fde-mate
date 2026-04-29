<script setup lang="ts">
import { computed } from 'vue'
import { Card, Tag } from 'ant-design-vue'
import type { SopDTO } from '@/types/api'

interface Props {
  sop: SopDTO
}

const props = defineProps<Props>()

const statusColor = computed(() => {
  const colors: Record<string, string> = {
    active: 'green',
    draft: 'orange',
    archived: 'default',
  }
  return colors[props.sop.status] || 'default'
})
</script>

<template>
  <div class="sop-card">
    <Card>
      <div class="sop-card-header">
        <h4>{{ sop.title }}</h4>
        <Tag :color="statusColor">{{ sop.status }}</Tag>
      </div>
      <div class="sop-card-description">
        {{ sop.description }}
      </div>
      <div class="sop-card-footer">
        <span class="sop-card-version">v{{ sop.version }}</span>
        <span class="sop-card-meta">{{ sop.updatedAt }}</span>
      </div>
    </Card>
  </div>
</template>

<style scoped>
.sop-card {
  cursor: pointer;
}

.sop-card:hover {
  box-shadow: var(--shadow-lg);
}

.sop-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.sop-card-header h4 {
  margin: 0;
  font-size: 16px;
}

.sop-card-description {
  font-size: 14px;
  color: var(--color-text-secondary);
  margin-bottom: 12px;
}

.sop-card-footer {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: var(--color-text-secondary);
}

.sop-card-version {
  color: var(--color-primary);
}
</style>