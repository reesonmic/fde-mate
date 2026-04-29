/**
 * SSE Client for streaming AI responses
 */

interface SSEOptions {
  onMessage: (data: string) => void
  onError?: (error: Error) => void
  onComplete?: () => void
}

interface SSEMessageEvent {
  data: string
}

export class SSEClient {
  private eventSource: EventSource | null = null
  private url: string

  constructor(url: string) {
    this.url = url
  }

  connect(options: SSEOptions): void {
    const authStore = useAuthStore()
    const headers: Record<string, string> = {}

    if (authStore.token) {
      headers['Authorization'] = `Bearer ${authStore.token}`
    }

    // EventSource doesn't support custom headers, so we use URL params for auth
    const urlWithAuth = authStore.token
      ? `${this.url}?token=${encodeURIComponent(authStore.token)}`
      : this.url

    this.eventSource = new EventSource(urlWithAuth)

    this.eventSource.onmessage = (event: SSEMessageEvent) => {
      if (event.data === '[DONE]') {
        this.disconnect()
        options.onComplete?.()
        return
      }
      options.onMessage(event.data)
    }

    this.eventSource.onerror = (error: Event) => {
      this.disconnect()
      options.onError?.(new Error('SSE connection error'))
    }
  }

  disconnect(): void {
    if (this.eventSource) {
      this.eventSource.close()
      this.eventSource = null
    }
  }

  isConnected(): boolean {
    return this.eventSource !== null && this.eventSource.readyState === EventSource.OPEN
  }
}

// Import at the top level due to module resolution
import { useAuthStore } from '@/stores/auth'

export function createSSEClient(url: string): SSEClient {
  return new SSEClient(url)
}