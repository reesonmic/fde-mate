<script setup lang="ts">
import { computed } from 'vue'
import MessageRenderer from './MessageRenderer.vue'
import type { CopilotMessage } from '@/types/copilot'

interface Props {
  messages: CopilotMessage[]
  assistantType: string
}

const props = defineProps<Props>()

const sortedMessages = computed(() => {
  return [...props.messages].sort((a, b) => {
    return new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()
  })
})
</script>

<template>
  <div class="message-list">
    <div v-if="messages.length === 0" class="message-list-empty">
      <p>开始与助手对话...</p>
    </div>
    <div v-else class="message-list-items">
      <div
        v-for="message in sortedMessages"
        :key="message.id"
        class="message-item"
        :class="`message-item--${message.role}`"
      >
        <MessageRenderer :message="message" :assistantType="assistantType" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.message-list {
  height: 100%;
}

.message-list-empty {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: var(--color-text-secondary);
  font-size: 14px;
}

.message-list-items {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.message-item {
  display: flex;
}

.message-item--user {
  justify-content: flex-end;
}

.message-item--assistant {
  justify-content: flex-start;
}
</style>