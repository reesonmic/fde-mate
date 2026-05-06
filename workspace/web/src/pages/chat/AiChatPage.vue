<script setup lang="ts">
import { ref, computed, nextTick, watch } from 'vue'
import { Tabs, Card, Input, Button, Select } from 'ant-design-vue'
import MessageRenderer from '@/components/copilot/MessageRenderer.vue'
import { useChatStore } from '@/stores/chat'

const chatStore = useChatStore()
const inputValue = ref('')
const activeTab = ref('free')
const sending = ref(false)
const messageContainer = ref<HTMLElement>()

const modeMap: Record<string, 'free' | 'task' | 'report'> = {
  free: 'free',
  task: 'task',
  report: 'report',
}

const currentMessages = computed(() => chatStore.messages)

const handleSend = async () => {
  if (!inputValue.value.trim() || sending.value) return
  sending.value = true
  try {
    chatStore.mode = modeMap[activeTab.value] || 'free'
    await chatStore.sendMessage(inputValue.value)
    inputValue.value = ''
  } finally {
    sending.value = false
    await nextTick()
    scrollToBottom()
  }
}

const handleClear = () => {
  chatStore.clearMessages()
}

const scrollToBottom = async () => {
  await nextTick()
  if (messageContainer.value) {
    messageContainer.value.scrollTop = messageContainer.value.scrollHeight
  }
}

// Watch for message changes to auto-scroll
watch(
  () => currentMessages.value.length,
  async () => {
    await scrollToBottom()
  },
)

// Also scroll when streaming content updates
watch(
  () => currentMessages.value.map((m) => m.content).join(''),
  async () => {
    if (chatStore.isStreaming) {
      await scrollToBottom()
    }
  },
)
</script>

<template>
  <div class="ai-chat-page">
    <div class="ai-chat-header">
      <h2>AI 对话中心</h2>
      <Button size="small" @click="handleClear">清空对话</Button>
    </div>

    <Tabs v-model:activeKey="activeTab">
      <Tabs.TabPane key="free" tab="自由对话">
        <Card class="chat-card">
          <div ref="messageContainer" class="chat-messages">
            <template v-if="currentMessages.length === 0">
              <div class="chat-welcome">
                <h3>欢迎使用 AI 对话</h3>
                <p>我可以帮你解答问题、提供建议和分析数据</p>
                <div class="chat-suggestions">
                  <Button size="small" @click="inputValue = '今天的工作总结怎么写？'">
                    今天的工作总结怎么写？
                  </Button>
                  <Button size="small" @click="inputValue = '帮我分析一下当前任务的风险'">
                    帮我分析一下当前任务的风险
                  </Button>
                  <Button size="small" @click="inputValue = 'FDE 最佳实践有哪些？'">
                    FDE 最佳实践有哪些？
                  </Button>
                </div>
              </div>
            </template>
            <template v-else>
              <div
                v-for="msg in currentMessages"
                :key="msg.id"
                class="chat-message"
                :class="{ 'chat-message--user': msg.role === 'user' }"
              >
                <MessageRenderer :message="msg" assistantType="chat" />
              </div>
              <div v-if="chatStore.isStreaming" class="chat-loading">
                <span>思考中...</span>
              </div>
            </template>
          </div>
          <div class="chat-input-area">
            <Input.TextArea
              v-model:value="inputValue"
              placeholder="输入你的问题..."
              :auto-size="{ minRows: 1, maxRows: 4 }"
              @pressEnter="handleSend"
              :disabled="sending"
            />
            <Button
              type="primary"
              :loading="sending"
              :disabled="!inputValue.trim()"
              @click="handleSend"
            >
              发送
            </Button>
          </div>
        </Card>
      </Tabs.TabPane>
      <Tabs.TabPane key="task" tab="任务对话">
        <Card class="chat-card">
          <template v-if="currentMessages.length === 0">
            <div class="chat-welcome">
              <h3>任务关联模式</h3>
              <p>结合当前任务上下文，提供针对性的分析和建议</p>
            </div>
          </template>
          <template v-else>
            <div ref="messageContainer" class="chat-messages">
              <div
                v-for="msg in currentMessages"
                :key="msg.id"
                class="chat-message"
                :class="{ 'chat-message--user': msg.role === 'user' }"
              >
                <MessageRenderer :message="msg" assistantType="task" />
              </div>
            </div>
          </template>
          <div class="chat-input-area">
            <Input.TextArea
              v-model:value="inputValue"
              placeholder="针对当前任务提问..."
              :auto-size="{ minRows: 1, maxRows: 4 }"
              @pressEnter="handleSend"
              :disabled="sending"
            />
            <Button
              type="primary"
              :loading="sending"
              :disabled="!inputValue.trim()"
              @click="handleSend"
            >
              发送
            </Button>
          </div>
        </Card>
      </Tabs.TabPane>
      <Tabs.TabPane key="report" tab="报告生成">
        <Card class="chat-card">
          <template v-if="currentMessages.length === 0">
            <div class="chat-welcome">
              <h3>报告生成模式</h3>
              <p>基于工作数据自动生成周报、月报等报告</p>
              <div class="chat-suggestions">
                <Button size="small" @click="inputValue = '帮我生成这周的周报'">
                  生成周报
                </Button>
                <Button size="small" @click="inputValue = '帮我总结一下本月的项目进展'">
                  生成月报
                </Button>
              </div>
            </div>
          </template>
          <template v-else>
            <div ref="messageContainer" class="chat-messages">
              <div
                v-for="msg in currentMessages"
                :key="msg.id"
                class="chat-message"
                :class="{ 'chat-message--user': msg.role === 'user' }"
              >
                <MessageRenderer :message="msg" assistantType="chat" />
              </div>
            </div>
          </template>
          <div class="chat-input-area">
            <Input.TextArea
              v-model:value="inputValue"
              placeholder="描述你想要生成的报告..."
              :auto-size="{ minRows: 1, maxRows: 4 }"
              @pressEnter="handleSend"
              :disabled="sending"
            />
            <Button
              type="primary"
              :loading="sending"
              :disabled="!inputValue.trim()"
              @click="handleSend"
            >
              生成
            </Button>
          </div>
        </Card>
      </Tabs.TabPane>
    </Tabs>
  </div>
</template>

<style scoped>
.ai-chat-page {
  max-width: 900px;
  margin: 0 auto;
  padding: 24px;
}

.ai-chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.ai-chat-header h2 {
  margin: 0;
}

.chat-card {
  min-height: 600px;
  display: flex;
  flex-direction: column;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  min-height: 400px;
  max-height: 600px;
}

.chat-message {
  margin-bottom: 12px;
}

.chat-message--user {
  display: flex;
  justify-content: flex-end;
}

.chat-welcome {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
}

.chat-welcome h3 {
  margin-bottom: 8px;
}

.chat-welcome p {
  color: var(--color-text-secondary, #666);
  margin-bottom: 24px;
}

.chat-suggestions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  justify-content: center;
}

.chat-input-area {
  display: flex;
  gap: 8px;
  padding: 12px 16px;
  border-top: 1px solid var(--color-border);
  align-items: flex-end;
}

.chat-input-area :deep(.ant-input-textarea) {
  flex: 1;
}

.chat-loading {
  text-align: center;
  padding: 8px;
  color: var(--color-text-secondary, #666);
  font-size: 12px;
}
</style>
