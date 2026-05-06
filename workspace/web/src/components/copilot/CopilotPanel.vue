<script setup lang="ts">
import { ref, computed } from 'vue'
import { Tabs, Button } from 'ant-design-vue'
import MessageList from './MessageList.vue'
import ChatInput from './ChatInput.vue'
import { useCopilotStore } from '@/stores/copilot'
import type { TaskDTO, ProjectDTO, CustomerDTO, FileDTO, UserDTO } from '@/types/business'

type MentionItem = TaskDTO | ProjectDTO | CustomerDTO | FileDTO | UserDTO

const copilotStore = useCopilotStore()
const activeTab = ref('task')

const assistants = [
  { key: 'task', name: 'T助手', description: '任务管理助手' },
  { key: 'project', name: 'P助手', description: '项目助手' },
  { key: 'coach', name: 'C助手', description: '教练助手' },
  { key: 'file', name: 'F助手', description: '文件助手' },
]

const currentMessages = computed(() => {
  return copilotStore.getMessages(activeTab.value)
})

const handleSend = (content: string, mentions?: MentionItem[]) => {
  copilotStore.sendMessage(activeTab.value, content, mentions)
}

const handleClear = () => {
  copilotStore.clearSession(activeTab.value)
}
</script>

<template>
  <div class="copilot-panel">
    <!-- Header -->
    <div class="copilot-panel-header">
      <Tabs v-model:activeKey="activeTab" size="small">
        <Tabs.TabPane v-for="assistant in assistants" :key="assistant.key">
          <template #tab>
            <span class="copilot-tab">{{ assistant.name }}</span>
          </template>
        </Tabs.TabPane>
      </Tabs>
      <Button size="small" @click="handleClear">清空</Button>
    </div>

    <!-- Messages -->
    <div class="copilot-panel-body">
      <MessageList :messages="currentMessages" :assistantType="activeTab" />
    </div>

    <!-- Input -->
    <div class="copilot-panel-footer">
      <ChatInput
        :assistantType="activeTab"
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
  padding: 8px 12px;
  border-bottom: 1px solid var(--color-border);
}

.copilot-tab {
  font-size: 12px;
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