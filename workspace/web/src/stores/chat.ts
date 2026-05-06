import { defineStore } from 'pinia'
import { ref } from 'vue'
import { copilotApi } from '@/apis/modules/copilot'
import type { CopilotMessage } from '@/types/copilot'

interface ReferenceItem {
  id: string
  title: string
  content?: string
  source?: string
}

export const useChatStore = defineStore('chat', () => {
  const messages = ref<CopilotMessage[]>([])
  const mode = ref<'free' | 'task' | 'report'>('free')
  const sessionId = ref<string>(`chat-session-${Date.now()}`)
  const references = ref<ReferenceItem[]>([])
  const isStreaming = ref(false)

  // Context for task/report modes
  const context = ref<Record<string, unknown>>({})

  const addMessage = (message: CopilotMessage) => {
    messages.value.push(message)
  }

  const setMode = (newMode: 'free' | 'task' | 'report') => {
    mode.value = newMode
  }

  const setContext = (ctx: Record<string, unknown>) => {
    context.value = ctx
  }

  const addReference = (item: ReferenceItem) => {
    if (!references.value.find((r) => r.id === item.id)) {
      references.value.push(item)
    }
  }

  const removeReference = (id: string) => {
    references.value = references.value.filter((r) => r.id !== id)
  }

  const clearReferences = () => {
    references.value = []
  }

  const clearMessages = () => {
    messages.value = []
    sessionId.value = `chat-session-${Date.now()}`
    isStreaming.value = false
  }

  const sendMessage = async (content: string) => {
    if (!content.trim()) return

    // Add user message
    addMessage({
      id: `msg-${Date.now()}`,
      content,
      role: 'user',
      timestamp: new Date().toISOString(),
      type: 'text',
    })

    // Prepare assistant message slot for streaming
    const assistantMsgId = `msg-ai-${Date.now()}`
    addMessage({
      id: assistantMsgId,
      content: '',
      role: 'assistant',
      timestamp: new Date().toISOString(),
      type: 'text',
    })

    isStreaming.value = true

    // Map frontend mode to backend assistantId
    const assistantIdMap: Record<string, string> = {
      free: 'chat',
      task: 'tasks',
      report: 'workspace',
    }

    copilotApi.chat(
      {
        assistantId: assistantIdMap[mode.value] || 'chat',
        message: content,
        sessionId: sessionId.value,
        mode: 'smart',
        context: context.value,
      },
      (chunk) => {
        const msg = messages.value.find((m) => m.id === assistantMsgId)
        if (!msg) return

        if (typeof chunk === 'string') {
          // Plain text chunk
          msg.content += chunk
        } else if (chunk.type === 'token') {
          // Streaming token from backend
          msg.content += chunk.delta || ''
        } else if (chunk.type === 'action') {
          msg.type = 'action'
          msg.metadata = chunk
        } else if (chunk.type === 'report') {
          msg.type = 'report'
          msg.metadata = chunk
        }
      },
      () => {
        // Stream done
        isStreaming.value = false
        const msg = messages.value.find((m) => m.id === assistantMsgId)
        if (msg && !msg.content) {
          msg.content = '抱歉，未收到有效回复。'
        }
      },
      (err: Error) => {
        isStreaming.value = false
        const msg = messages.value.find((m) => m.id === assistantMsgId)
        if (msg) {
          msg.content = '抱歉，发生了一个错误。请稍后重试。'
        }
      },
    )
  }

  return {
    messages,
    mode,
    sessionId,
    references,
    context,
    isStreaming,
    addMessage,
    setMode,
    setContext,
    addReference,
    removeReference,
    clearReferences,
    clearMessages,
    sendMessage,
  }
})
