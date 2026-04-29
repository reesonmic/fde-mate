<script setup lang="ts">
interface Props {
  steps: Array<{
    action: string
    description: string
    relatedObjectId?: string
    relatedObjectType?: string
  }>
}

const props = defineProps<Props>()
</script>

<template>
  <div class="next-steps-card">
    <div class="next-steps-header">
      <h4>建议的下一步操作</h4>
    </div>
    <div class="next-steps-list">
      <div v-for="(step, index) in steps" :key="index" class="next-steps-item">
        <div class="next-steps-index">{{ index + 1 }}</div>
        <div class="next-steps-content">
          <div class="next-steps-action">{{ step.action }}</div>
          <div class="next-steps-description">{{ step.description }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.next-steps-card {
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  padding: 12px;
}

.next-steps-header {
  margin-bottom: 12px;
}

.next-steps-header h4 {
  margin: 0;
  font-size: 14px;
  color: var(--color-primary);
}

.next-steps-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.next-steps-item {
  display: flex;
  gap: 12px;
}

.next-steps-index {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-primary);
  color: white;
  border-radius: 12px;
  font-size: 12px;
}

.next-steps-content {
  flex: 1;
}

.next-steps-action {
  font-size: 14px;
  font-weight: 500;
}

.next-steps-description {
  font-size: 12px;
  color: var(--color-text-secondary);
  margin-top: 4px;
}
</style>