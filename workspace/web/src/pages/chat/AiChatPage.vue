<script setup lang="ts">
import { ref } from 'vue'
import { Tabs, Card, Input, Button, Mention } from 'ant-design-vue'
import { useChatStore } from '@/stores/chat'
import { useMention } from '@/composables/useMention'

const chatStore = useChatStore()
const mention = useMention()

const inputValue = ref('')
const activeTab = ref('free')
const loading = ref(false)

const handleSend = async () => {
  if (!inputValue.value.trim()) return

  chatStore.addMessage({
    id: `msg-${Date.now()}`,
    content: inputValue.value,
    role: 'user',
    timestamp: new Date().toISOString(),
    type: 'text',
  })

  loading.value = true
  try {
    // Send to API
    // const response = await chatApi.send(inputValue.value)
    // chatStore.addMessage(response)
  } finally {
    loading.value = false
    inputValue.value = ''
  }
}
</script>

<template>
  <div class="ai-chat-page">
    <h2>AI对话中心</h2>

    <Tabs v-model:activeKey="activeTab">
      <Tabs.TabPane key="free" tab="自由对话">
        <Card class="chat-card">
          <div class="chat-messages">
            <div v-for="msg in chatStore.messages" :key="msg.id" class="chat-message">
              {{ msg.content }}
            </div>
          </div>
          <div class="chat-input-area">
            <Input
              v-model:value="inputValue"
              placeholder="输入问题..."
              @pressEnter="handleSend"
            />
            <Button type="primary" :loading="loading" @click="handleSend">发送</Button>
          </div>
        </Card>
      </Tabs.TabPane>
      <Tabs.TabPane key="task" tab="任务对话">
        <Card>
          <p>任务关联模式</p>
        </Card>
      </Tabs.TabPane>
      <Tabs.TabPane key="report" tab="报告生成">
        <Card>
          <p>报告生成模式</p>
        </Card>
      </Tabs.TabPane>
    </Tabs>
  </div>
</template>

<style scoped>
.ai-chat-page h2 {
  margin-bottom: 24px;
}

.chat-card {
  height: 600px;
  display: flex;
  flex-direction: column;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

.chat-message {
  padding: 8px 12px;
  margin-bottom: 8px;
  background: var(--color-fill-secondary);
  border-radius: 4px;
}

.chat-input-area {
  display: flex;
  gap: 8px;
  padding: 16px;
  border-top: 1px solid var(--color-border);
}
</style>