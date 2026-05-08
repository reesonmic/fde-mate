<script setup lang="ts">
import { computed, watch } from 'vue'
import { Button } from 'ant-design-vue'
import MessageList from './MessageList.vue'
import ChatInput from './ChatInput.vue'
import { useCopilotStore } from '@/stores/copilot'
import type { TaskDTO, ProjectDTO, CustomerDTO, FileDTO, UserDTO } from '@/types/business'
import { getAssistantConfig } from '@/config/assistants'

type MentionItem = TaskDTO | ProjectDTO | CustomerDTO | FileDTO | UserDTO

const props = defineProps<{
  assistantKey: string
}>()

const copilotStore = useCopilotStore()

// 当前助手配置
const assistantConfig = computed(() => getAssistantConfig(props.assistantKey))

// 当前助手的消息
const currentMessages = computed(() => {
  return copilotStore.getMessages(props.assistantKey)
})

const handleSend = (content: string, mentions?: MentionItem[]) => {
  copilotStore.sendMessage(props.assistantKey, content, mentions)
}

const handleClear = () => {
  copilotStore.clearSession(props.assistantKey)
}
</script>

<template>
  <div class="copilot-panel">
    <!-- Header -->
    <div class="copilot-panel-header">
      <div class="copilot-header-info">
        <div class="copilot-header-icon">{{ assistantConfig?.icon }}</div>
        <div class="copilot-header-content">
          <div class="copilot-header-name">{{ assistantConfig?.name }}</div>
          <div class="copilot-header-desc">{{ assistantConfig?.description }}</div>
        </div>
      </div>
      <Button size="small" @click="handleClear">清空</Button>
    </div>

    <!-- Messages -->
    <div class="copilot-panel-body">
      <MessageList :messages="currentMessages" :assistantType="assistantKey" />
    </div>

    <!-- Input -->
    <div class="copilot-panel-footer">
      <ChatInput
        :assistantType="assistantKey"
        @send="handleSend"
      />
    </div>
  </div>
</template>

<style scoped>
.copilot-panel {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.copilot-panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid var(--color-border);
  background: var(--color-fill-secondary);
}

.copilot-header-info {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1;
}

.copilot-header-icon {
  font-size: 24px;
  line-height: 1;
}

.copilot-header-content {
  flex: 1;
  min-width: 0;
}

.copilot-header-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text);
  line-height: 1.4;
}

.copilot-header-desc {
  font-size: 11px;
  color: var(--color-text-secondary);
  line-height: 1.4;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.copilot-panel-body {
  flex: 1;
  overflow-y: auto;
  padding: 12px;
}

.copilot-panel-footer {
  padding: 12px;
  border-top: 1px solid var(--color-border);
}
</style>