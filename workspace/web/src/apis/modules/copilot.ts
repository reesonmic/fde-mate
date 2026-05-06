import { http } from '../http'
import { openSse } from '../sse'
import type { CopilotRequest } from '@types/api'

interface SessionDTO {
  id: number
  title: string
  assistant_type: string
  created_at: string
}

export const copilotApi = {
  chat: (data: CopilotRequest, onChunk: (chunk: unknown) => void, onDone?: () => void, onError?: (err: Error) => void) =>
    openSse({
      url: '/copilot/chat',
      body: data,
      onMessage: onChunk,
      onDone,
      onError,
    }),

  listSessions: () => http.get<unknown, SessionDTO[]>('/copilot/sessions'),

  getSession: (id: number) => http.get<unknown, SessionDTO>(`/copilot/sessions/${id}`),

  deleteSession: (id: number) => http.delete<unknown, void>(`/copilot/sessions/${id}`),

  previewAction: (data: { toolName: string; args: Record<string, unknown> }) =>
    http.post<unknown, { actionId: string; title: string; severity: string; preview: Record<string, unknown> }>('/copilot/preview-action', data),

  executeAction: (data: { actionId: string }) =>
    http.post<unknown, { success: boolean; result: Record<string, unknown> }>('/copilot/execute-action', data),

  cancelAction: (data: { actionId: string }) =>
    http.post<unknown, { cancelled: boolean }>('/copilot/cancel-action', data),

  feedback: (data: { messageId: number; rating: string }) =>
    http.post<unknown, { submitted: boolean }>('/copilot/feedback', data),
}
