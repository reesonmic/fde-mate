/**
 * SSE Client for streaming AI responses
 */

interface OpenSseOptions {
  url: string
  body?: Record<string, unknown>
  onMessage: (data: unknown) => void
  onDone?: () => void
  onError?: (error: Error) => void
}

/**
 * POST-based SSE client using fetch + ReadableStream.
 * Required because EventSource only supports GET requests.
 * Uses Authorization header (not URL params) for secure authentication.
 */
export function openSse(options: OpenSseOptions): AbortController {
  const { url, body, onMessage, onDone, onError } = options
  const controller = new AbortController()

  // 设置 120 秒超时（与后端 ai_orchestrator_timeout 一致）
  const timeoutId = setTimeout(() => {
    controller.abort()
    onError?.(new Error('SSE connection timeout after 120 seconds'))
  }, 120000)

  const token = localStorage.getItem('access_token')

  fetch(`/api/v1${url}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: body ? JSON.stringify(body) : undefined,
    signal: controller.signal,
  })
    .then(async (response) => {
      if (!response.ok) {
        throw new Error(`SSE error: ${response.status} ${response.statusText}`)
      }
      if (!response.body) {
        throw new Error('SSE error: no response body')
      }

      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop() || ''

        for (const line of lines) {
          const trimmed = line.trim()
          if (!trimmed || !trimmed.startsWith('data: ')) continue

          const data = trimmed.slice(6)
          if (data === '[DONE]') {
            clearTimeout(timeoutId)
            onDone?.()
            return
          }

          try {
            onMessage(JSON.parse(data))
          } catch {
            onMessage(data)
          }
        }
      }
      clearTimeout(timeoutId)
      onDone?.()
    })
    .catch((err: Error) => {
      clearTimeout(timeoutId)
      if (err.name !== 'AbortError') {
        onError?.(err)
      }
    })

  return controller
}