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
  const pendingAction = ref<any>(null)

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

  const sendMessage = async (
    assistantType: string,
    content: string,
    mentions?: any[]
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

    // Send to API and handle response
    try {
      const response = await copilotApi.chat({
        assistantType,
        message: content,
        mentions,
        sessionId: getSessionId(assistantType),
      })

      // Add assistant response
      addMessage(assistantType, response)

      // Check if response has pending action
      if (response.type === 'action') {
        pendingAction.value = response.metadata
      }
    } catch (error) {
      // Add error message
      addMessage(assistantType, {
        id: `msg-err-${Date.now()}`,
        content: '抱歉，发生了一个错误。请稍后重试。',
        role: 'assistant',
        timestamp: new Date().toISOString(),
        type: 'text',
      })
    }
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