<script setup lang="ts">
interface Props {
  title?: string
  description?: string
  icon?: string
}

const props = withDefaults(defineProps<Props>(), {
  title: '暂无数据',
  description: '',
  icon: 'inbox',
})
</script>

<template>
  <div class="empty-state">
    <div class="empty-state-icon">
      <slot name="icon">
        <!-- Default icon placeholder -->
        <span class="empty-state-icon-default">{{ icon }}</span>
      </slot>
    </div>
    <div class="empty-state-title">{{ title }}</div>
    <div v-if="description" class="empty-state-description">{{ description }}</div>
    <slot name="action" />
  </div>
</template>

<style scoped>
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 32px;
  text-align: center;
}

.empty-state-icon {
  font-size: 48px;
  color: var(--color-text-secondary);
  margin-bottom: 16px;
}

.empty-state-icon-default {
  opacity: 0.5;
}

.empty-state-title {
  font-size: 16px;
  color: var(--color-text);
  margin-bottom: 8px;
}

.empty-state-description {
  font-size: 14px;
  color: var(--color-text-secondary);
}
</style>