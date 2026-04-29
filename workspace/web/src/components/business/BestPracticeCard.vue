<script setup lang="ts">
import { computed } from 'vue'
import { Card, Tag } from 'ant-design-vue'
import type { BestPracticeDTO } from '@/types/api'

interface Props {
  practice: BestPracticeDTO
}

const props = defineProps<Props>()

const categoryTag = computed(() => {
  return props.practice.category || '通用'
})
</script>

<template>
  <div class="best-practice-card">
    <Card>
      <div class="best-practice-card-header">
        <h4>{{ practice.title }}</h4>
        <Tag>{{ categoryTag }}</Tag>
      </div>
      <div class="best-practice-card-summary">
        {{ practice.summary }}
      </div>
      <div class="best-practice-card-footer">
        <span class="best-practice-card-meta">
          {{ practice.author }} · {{ practice.createdAt }}
        </span>
      </div>
    </Card>
  </div>
</template>

<style scoped>
.best-practice-card {
  cursor: pointer;
}

.best-practice-card:hover {
  box-shadow: var(--shadow-lg);
}

.best-practice-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.best-practice-card-header h4 {
  margin: 0;
  font-size: 16px;
}

.best-practice-card-summary {
  font-size: 14px;
  color: var(--color-text-secondary);
  margin-bottom: 12px;
}

.best-practice-card-footer {
  font-size: 12px;
  color: var(--color-text-secondary);
}
</style>