<script setup lang="ts">
import { computed } from 'vue'
import type { MentionSearchResult } from '@/types/api'
import type { TaskDTO, ProjectDTO, CustomerDTO, FileDTO, UserDTO } from '@/types/business'

type MentionedItem = (TaskDTO | ProjectDTO | CustomerDTO | FileDTO | UserDTO) & { type: string }

interface Props {
  results: MentionSearchResult
}

const props = defineProps<Props>()
const emit = defineEmits<{
  select: [item: MentionedItem]
  close: []
}>()

const allItems = computed(() => {
  return [
    ...props.results.tasks.map(t => ({ ...t, type: 'task' })),
    ...props.results.projects.map(p => ({ ...p, type: 'project' })),
    ...props.results.customers.map(c => ({ ...c, type: 'customer' })),
    ...props.results.files.map(f => ({ ...f, type: 'file' })),
    ...props.results.users.map(u => ({ ...u, type: 'user' })),
  ]
})

const typeIcons: Record<string, string> = {
  task: '📋',
  project: '📁',
  customer: '👥',
  file: '📄',
  user: '👤',
}

const handleSelect = (item: MentionedItem) => {
  emit('select', item)
}
</script>

<template>
  <div class="mention-picker">
    <div class="mention-picker-header">
      <span>选择引用对象</span>
      <button @click="emit('close')">×</button>
    </div>
    <div class="mention-picker-list">
      <div
        v-for="item in allItems"
        :key="`${item.type}-${item.id}`"
        class="mention-picker-item"
        @click="handleSelect(item)"
      >
        <span class="mention-picker-icon">{{ typeIcons[item.type] }}</span>
        <span class="mention-picker-name">{{ item.name }}</span>
        <span class="mention-picker-type">{{ item.type }}</span>
      </div>
      <div v-if="allItems.length === 0" class="mention-picker-empty">
        无匹配结果
      </div>
    </div>
  </div>
</template>

<style scoped>
.mention-picker {
  position: absolute;
  bottom: 100%;
  left: 0;
  width: 280px;
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  box-shadow: var(--shadow-lg);
  z-index: 100;
}

.mention-picker-header {
  display: flex;
  justify-content: space-between;
  padding: 8px 12px;
  border-bottom: 1px solid var(--color-border);
  font-size: 12px;
}

.mention-picker-list {
  max-height: 200px;
  overflow-y: auto;
}

.mention-picker-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  cursor: pointer;
}

.mention-picker-item:hover {
  background: var(--color-fill-secondary);
}

.mention-picker-icon {
  font-size: 14px;
}

.mention-picker-name {
  flex: 1;
  font-size: 14px;
}

.mention-picker-type {
  font-size: 12px;
  color: var(--color-text-secondary);
}

.mention-picker-empty {
  padding: 12px;
  text-align: center;
  color: var(--color-text-secondary);
  font-size: 14px;
}
</style>