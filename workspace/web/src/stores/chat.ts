import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { CopilotMessage } from '@/types/copilot'

export const useChatStore = defineStore('chat', () => {
  // Global chat messages
  const messages = ref<CopilotMessage[]>([])

  // Active mode (free, task, report)
  const mode = ref<'free' | 'task' | 'report'>('free')

  // Current session ID
  const sessionId = ref<string>(`chat-global-${Date.now()}`)

  // Referenced objects
  const references = ref<any[]>([])

  const addMessage = (message: CopilotMessage) => {
    messages.value.push(message)
  }

  const setMode = (newMode: 'free' | 'task' | 'report') => {
    mode.value = newMode
  }

  const addReference = (item: any) => {
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
    sessionId.value = `chat-global-${Date.now()}`
  }

  return {
    messages,
    mode,
    sessionId,
    references,
    addMessage,
    setMode,
    addReference,
    removeReference,
    clearReferences,
    clearMessages,
  }
})