import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { CopilotMessage } from '@/types/copilot'
import { copilotApi } from '@/apis/modules/copilot'

// Session IDs for each assistant
const SESSION_IDS = {
  task: 'task-session',
  project: 'project-session',
  coach: 'coach-session',
  file: 'file-session',
  chat: 'chat-session',
}

export const useCopilotStore = defineStore('copilot', () => {
  // Messages for each assistant
  const messages = ref<Record<string, CopilotMessage[]>>({
    task: [],
    project: [],
    coach: [],
    file: [],
    chat: [],
  })

  // Session IDs
  const sessionIds = ref<Record<string, string>>(SESSION_IDS)

  // Current pending action for confirmation
  const pendingAction = ref<Record<string, unknown> | null>(null)

  const getMessages = (assistantType: string) => {
    return messages.value[assistantType] || []
  }

  const getSessionId = (assistantType: string) => {
    return sessionIds.value[assistantType] || `session-${assistantType}-${Date.now()}`
  }

  const addMessage = (assistantType: string, message: CopilotMessage) => {
    if (!messages.value[assistantType]) {
      messages.value[assistantType] = []
    }
    messages.value[assistantType].push(message)
  }

  const streamingMsgIds = ref<Record<string, string>>({})

  const sendMessage = async (
    assistantType: string,
    content: string,
    mentions?: Array<{ type: string; id: string; label: string }>,
    pageContext?: Record<string, unknown> // 新增：页面上下文数据
  ) => {
    // Add user message
    addMessage(assistantType, {
      id: `msg-${Date.now()}`,
      content,
      role: 'user',
      timestamp: new Date().toISOString(),
      type: 'text',
      metadata: { mentions },
    })

    // Prepare assistant message slot for streaming
    const assistantMsgId = `msg-ai-${Date.now()}-${assistantType}`
    addMessage(assistantType, {
      id: assistantMsgId,
      content: '',
      role: 'assistant',
      timestamp: new Date().toISOString(),
      type: 'text',
    })
    streamingMsgIds.value[assistantType] = assistantMsgId

    // Map frontend assistant type to backend assistantId
    const assistantIdMap: Record<string, string> = {
      task: 'tasks',
      project: 'project',
      coach: 'coach',
      file: 'files',
      chat: 'chat',
    }

    // 构建上下文：合并 assistantType 和页面上下文
    const context = {
      assistantType,
      ...pageContext, // 传入页面的实际数据
    }

    copilotApi.chat(
      {
        assistantId: assistantIdMap[assistantType] || 'chat',
        message: content,
        sessionId: getSessionId(assistantType),
        mode: 'smart',
        context, // 使用完整的上下文
      },
      (chunk) => {
        const msg = messages.value[assistantType]?.find(
          (m) => m.id === streamingMsgIds.value[assistantType],
        )
        if (!msg) return

        if (typeof chunk === 'string') {
          msg.content += chunk
        } else if (chunk.type === 'token') {
          msg.content += chunk.delta || ''
        } else if (chunk.type === 'action') {
          msg.type = 'action'
          msg.metadata = chunk
          pendingAction.value = chunk
        } else if (chunk.type === 'report') {
          msg.type = 'report'
          msg.metadata = chunk
        } else if (chunk.type === 'searchResults') {
          msg.type = 'searchResults'
          msg.metadata = chunk
        } else if (chunk.type === 'nextSteps') {
          msg.type = 'nextSteps'
          msg.metadata = chunk
        }
      },
      () => {
        // Stream done
        const msg = messages.value[assistantType]?.find(
          (m) => m.id === streamingMsgIds.value[assistantType],
        )
        if (msg && !msg.content) {
          msg.content = '抱歉，未收到有效回复。'
        }
        delete streamingMsgIds.value[assistantType]
      },
      () => {
        // Error
        const msg = messages.value[assistantType]?.find(
          (m) => m.id === streamingMsgIds.value[assistantType],
        )
        if (msg) {
          msg.content = '抱歉，发生了一个错误。请稍后重试。'
        }
        delete streamingMsgIds.value[assistantType]
      },
    )
  }

  const executeAction = async (actionId: string, toolName: string) => {
    try {
      const result = await copilotApi.executeAction({
        actionId,
        toolName,
      })

      // Add success message to all relevant assistants
      addMessage('task', {
        id: `msg-action-${Date.now()}`,
        content: `操作已成功执行: ${toolName}`,
        role: 'assistant',
        timestamp: new Date().toISOString(),
        type: 'text',
        metadata: { result },
      })

      pendingAction.value = null
    } catch (error) {
      // Handle error
      throw error
    }
  }

  const cancelAction = (actionId: string) => {
    pendingAction.value = null
  }

  const clearSession = (assistantType: string) => {
    messages.value[assistantType] = []
    sessionIds.value[assistantType] = `session-${assistantType}-${Date.now()}`
  }

  return {
    messages,
    sessionIds,
    pendingAction,
    getMessages,
    getSessionId,
    addMessage,
    sendMessage,
    executeAction,
    cancelAction,
    clearSession,
  }
})