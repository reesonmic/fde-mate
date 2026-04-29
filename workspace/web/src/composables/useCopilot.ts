import { ref, computed } from 'vue'
import { copilotApi } from '@/apis/modules/copilot'
import { useCopilotStore } from '@/stores/copilot'
import type { CopilotMessage, ActionPreview } from '@/types/copilot'

/**
 * Copilot composable for managing assistant interactions
 */
export function useCopilot(assistantType: string) {
  const copilotStore = useCopilotStore()

  const messages = computed(() => copilotStore.getMessages(assistantType))

  const loading = ref(false)
  const error = ref<Error | null>(null)

  const sendMessage = async (content: string, mentions?: any[]) => {
    loading.value = true
    error.value = null

    try {
      // Add user message
      copilotStore.addMessage(assistantType, {
        id: `msg-${Date.now()}`,
        content,
        role: 'user',
        timestamp: new Date().toISOString(),
        type: 'text',
        metadata: { mentions },
      })

      // Send to API
      const response = await copilotApi.chat({
        assistantType,
        message: content,
        mentions,
        sessionId: copilotStore.getSessionId(assistantType),
      })

      // Add assistant response
      copilotStore.addMessage(assistantType, response)
    } catch (err) {
      error.value = err as Error
    } finally {
      loading.value = false
    }
  }

  const previewAction = async (toolName: string, params: any): Promise<ActionPreview | null> => {
    loading.value = true
    try {
      const preview = await copilotApi.previewAction({
        assistantType,
        toolName,
        params,
      })
      return preview
    } catch (err) {
      error.value = err as Error
      return null
    } finally {
      loading.value = false
    }
  }

  const executeAction = async (actionId: string, toolName: string) => {
    loading.value = true
    try {
      await copilotApi.executeAction({
        actionId,
        toolName,
      })
    } catch (err) {
      error.value = err as Error
    } finally {
      loading.value = false
    }
  }

  const clearSession = async () => {
    const sessionId = copilotStore.getSessionId(assistantType)
    if (sessionId) {
      await copilotApi.clearSession(sessionId)
    }
    copilotStore.clearSession(assistantType)
  }

  return {
    messages,
    loading,
    error,
    sendMessage,
    previewAction,
    executeAction,
    clearSession,
  }
}