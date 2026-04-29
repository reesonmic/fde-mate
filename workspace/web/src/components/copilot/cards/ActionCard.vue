<script setup lang="ts">
import { ref } from 'vue'
import { Button, Tag } from 'ant-design-vue'
import { useCopilotStore } from '@/stores/copilot'

interface Props {
  action: {
    actionId: string
    toolName: string
    params: any
    preview: string
    expiresAt: string
  }
  assistantType: string
}

const props = defineProps<Props>()
const copilotStore = useCopilotStore()

const loading = ref(false)

const handleConfirm = async () => {
  loading.value = true
  try {
    await copilotStore.executeAction(props.action.actionId, props.action.toolName)
  } finally {
    loading.value = false
  }
}

const handleCancel = () => {
  copilotStore.cancelAction(props.action.actionId)
}
</script>

<template>
  <div class="action-card">
    <div class="action-card-header">
      <Tag color="blue">{{ action.toolName }}</Tag>
      <span class="action-card-timer">60s</span>
    </div>
    <div class="action-card-preview">
      {{ action.preview }}
    </div>
    <div class="action-card-params">
      <pre>{{ JSON.stringify(action.params, null, 2) }}</pre>
    </div>
    <div class="action-card-actions">
      <Button type="primary" :loading="loading" @click="handleConfirm">
        确认执行
      </Button>
      <Button @click="handleCancel">取消</Button>
    </div>
  </div>
</template>

<style scoped>
.action-card {
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  padding: 12px;
}

.action-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.action-card-timer {
  font-size: 12px;
  color: var(--color-warning);
}

.action-card-preview {
  font-size: 14px;
  margin-bottom: 12px;
}

.action-card-params {
  background: var(--color-fill-secondary);
  padding: 8px;
  border-radius: 4px;
  margin-bottom: 12px;
  font-size: 12px;
}

.action-card-actions {
  display: flex;
  gap: 8px;
}
</style>