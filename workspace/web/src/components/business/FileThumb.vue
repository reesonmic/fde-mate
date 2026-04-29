<script setup lang="ts">
interface Props {
  file: {
    id: string
    name: string
    type: string
    size?: number
    thumbnail?: string
  }
}

const props = defineProps<Props>()

const formatSize = (size?: number) => {
  if (!size) return ''
  if (size < 1024) return `${size}B`
  if (size < 1024 * 1024) return `${(size / 1024).toFixed(1)}KB`
  return `${(size / 1024 / 1024).toFixed(1)}MB`
}

const typeIcon = computed(() => {
  const icons: Record<string, string> = {
    pdf: '📄',
    doc: '📝',
    xls: '📊',
    ppt: '📽️',
    image: '🖼️',
    default: '📁',
  }
  return icons[props.file.type] || icons.default
})
</script>

<template>
  <div class="file-thumb">
    <div class="file-thumb-icon">
      <img v-if="file.thumbnail" :src="file.thumbnail" :alt="file.name" />
      <span v-else>{{ typeIcon }}</span>
    </div>
    <div class="file-thumb-info">
      <span class="file-thumb-name">{{ file.name }}</span>
      <span class="file-thumb-size">{{ formatSize(file.size) }}</span>
    </div>
  </div>
</template>

<script lang="ts">
import { computed } from 'vue'
export default {
  name: 'FileThumb',
}
</script>

<style scoped>
.file-thumb {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px;
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border);
  border-radius: 8px;
}

.file-thumb-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-fill-secondary);
  border-radius: 4px;
  font-size: 24px;
}

.file-thumb-icon img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 4px;
}

.file-thumb-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.file-thumb-name {
  font-size: 14px;
}

.file-thumb-size {
  font-size: 12px;
  color: var(--color-text-secondary);
}
</style>