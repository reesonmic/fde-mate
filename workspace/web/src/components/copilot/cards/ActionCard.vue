<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { Button, Tag } from 'ant-design-vue'
import { useCopilotStore } from '@/stores/copilot'

interface Props {
  action: {
    actionId: string
    toolName: string
    params: Record<string, unknown>
    preview: string
    severity?: 'low' | 'medium' | 'high'
    expiresAt?: string
  }
  assistantType: string
}

const props = withDefaults(defineProps<Props>(), {
  action: () => ({
    actionId: '',
    toolName: '',
    params: {},
    preview: '',
    severity: 'low',
  }),
})

const copilotStore = useCopilotStore()

const loading = ref(false)
const status = ref<'pending' | 'confirmed' | 'cancelled' | 'expired'>('pending')
const timeLeft = ref(60)
let timer: ReturnType<typeof setInterval> | null = null

const severityTagColor = computed(() => {
  const map = { low: 'green', medium: 'orange', high: 'red' }
  return map[props.action.severity ?? 'low'] || 'blue'
})

const severityText = computed(() => {
  const map = { low: '低影响', medium: '中等影响', high: '高影响' }
  return map[props.action.severity ?? 'low'] || '低影响'
})

const startCountdown = () => {
  timer = setInterval(() => {
    timeLeft.value--
    if (timeLeft.value <= 0) {
      status.value = 'expired'
      stopCountdown()
    }
  }, 1000)
}

const stopCountdown = () => {
  if (timer) {
    clearInterval(timer)
    timer = null
  }
}

const handleConfirm = async () => {
  loading.value = true
  try {
    await copilotStore.executeAction(props.action.actionId, props.action.toolName)
    status.value = 'confirmed'
  } finally {
    loading.value = false
    stopCountdown()
  }
}

const handleCancel = () => {
  copilotStore.cancelAction(props.action.actionId)
  status.value = 'cancelled'
  stopCountdown()
}

onMounted(() => {
  startCountdown()
})

onUnmounted(() => {
  stopCountdown()
})
</script>

<template>
  <div class="action-card" :class="`action-card--${status}`">
    <!-- Pending state -->
    <template v-if="status === 'pending'">
      <div class="action-card-header">
        <div class="action-card-header-left">
          <Tag :color="severityTagColor">{{ severityText }}</Tag>
          <Tag color="blue">{{ action.toolName }}</Tag>
        </div>
        <span class="action-card-timer" :class="{ 'action-card-timer--urgent': timeLeft <= 10 }">
          {{ timeLeft }}s
        </span>
      </div>
      <div class="action-card-preview">{{ action.preview }}</div>
      <div class="action-card-params">
        <pre>{{ JSON.stringify(action.params, null, 2) }}</pre>
      </div>
      <div class="action-card-actions">
        <Button type="primary" :loading="loading" @click="handleConfirm">
          确认执行
        </Button>
        <Button @click="handleCancel">取消</Button>
      </div>
    </template>

    <!-- Confirmed state -->
    <div v-else-if="status === 'confirmed'" class="action-card-result action-card-result--success">
      <span class="result-icon">&#10003;</span>
      <span>操作已执行: {{ action.toolName }}</span>
    </div>

    <!-- Cancelled state -->
    <div v-else-if="status === 'cancelled'" class="action-card-result action-card-result--cancelled">
      <span>&#10007;</span>
      <span>操作已取消</span>
    </div>

    <!-- Expired state -->
    <div v-else-if="status === 'expired'" class="action-card-result action-card-result--expired">
      <span>&#9201;</span>
      <span>操作已过期 (60s)，请重新发起</span>
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

.action-card-header-left {
  display: flex;
  gap: 4px;
}

.action-card-timer {
  font-size: 12px;
  color: var(--color-warning);
  font-variant-numeric: tabular-nums;
}

.action-card-timer--urgent {
  color: var(--color-error, #ff4d4f);
  font-weight: 600;
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
  overflow-x: auto;
}

.action-card-params pre {
  margin: 0;
}

.action-card-actions {
  display: flex;
  gap: 8px;
}

.action-card-result {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 0;
  font-size: 14px;
}

.action-card-result--success {
  color: var(--color-success, #52c41a);
}

.action-card-result--cancelled {
  color: var(--color-warning);
}

.action-card-result--expired {
  color: var(--color-text-secondary, #999);
}
</style>
