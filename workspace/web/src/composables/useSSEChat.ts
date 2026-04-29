import { ref } from 'vue'
import { SSEClient } from '@/apis/sse'
import { copilotApi } from '@/apis/modules/copilot'
import type { CopilotMessage } from '@/types/copilot'

/**
 * SSE Chat composable for streaming AI responses
 */
export function useSSEChat(sessionId: string) {
  const messages = ref<CopilotMessage[]>([])
  const isConnected = ref(false)
  const isStreaming = ref(false)
  const error = ref<Error | null>(null)

  let client: SSEClient | null = null

  const connect = () => {
    client = copilotApi.createChatStream(sessionId)

    client.connect({
      onMessage: (data) => {
        try {
          const parsed = JSON.parse(data)
          messages.value.push(parsed)
        } catch {
          // Plain text message
          messages.value.push({
            id: `msg-${Date.now()}`,
            content: data,
            role: 'assistant',
            timestamp: new Date().toISOString(),
            type: 'text',
          })
        }
      },
      onError: (err) => {
        error.value = err
        isConnected.value = false
      },
      onComplete: () => {
        isStreaming.value = false
      },
    })

    isConnected.value = client.isConnected()
  }

  const disconnect = () => {
    if (client) {
      client.disconnect()
      client = null
    }
    isConnected.value = false
  }

  const sendMessage = async (content: string) => {
    // Add user message
    messages.value.push({
      id: `msg-${Date.now()}`,
      content,
      role: 'user',
      timestamp: new Date().toISOString(),
      type: 'text',
    })

    isStreaming.value = true

    // Start streaming
    if (!isConnected.value) {
      connect()
    }
  }

  return {
    messages,
    isConnected,
    isStreaming,
    error,
    connect,
    disconnect,
    sendMessage,
  }
}