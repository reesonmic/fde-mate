import { http } from '../http'
import { openSse } from '../sse'

export const copilotApi = {
  chat: (data: any, onChunk: (chunk: any) => void, onDone?: () => void) =>
    openSse({
      url: '/copilot/chat',
      body: data,
      onMessage: onChunk,
      onDone,
    }),

  listSessions: () => http.get<unknown, any[]>('/copilot/sessions'),

  getSession: (id: number) => http.get<unknown, any>(`/copilot/sessions/${id}`),

  deleteSession: (id: number) => http.delete<unknown, void>(`/copilot/sessions/${id}`),

  previewAction: (data: { toolName: string; args: Record<string, unknown>; sessionId: string }) =>
    http.post<unknown, any>('/copilot/preview-action', data),

  executeAction: (data: { actionId: string }) =>
    http.post<unknown, { success: boolean; result: Record<string, unknown> }>('/copilot/execute-action', data),

  cancelAction: (data: { actionId: string }) =>
    http.post<unknown, { cancelled: boolean }>('/copilot/cancel-action', data),

  feedback: (data: { messageId: number; rating: string }) =>
    http.post<unknown, { submitted: boolean }>('/copilot/feedback', data),
}
