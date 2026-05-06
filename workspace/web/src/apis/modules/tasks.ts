import { http } from '../http'
import type { TaskDTO } from '@types/business'

export interface TaskListParams {
  keyword?: string
  status?: string[]
  assigneeId?: number
  projectId?: number
  priority?: string[]
  page?: number
  size?: number
}

export interface TaskHistoryEntry {
  id: number
  task_id: number
  action: string
  actor_name: string
  old_status: string | null
  new_status: string
  gmt_create: string
}

export const tasksApi = {
  list: (params: TaskListParams = {}) =>
    http.get<unknown, { items: TaskDTO[]; total: number; page: number; size: number }>('/tasks', { params }),

  get: (id: number) => http.get<unknown, TaskDTO>(`/tasks/${id}`),

  create: (data: { title: string; description?: string; priority?: string; project_id?: number; deadline?: string }) => http.post<unknown, TaskDTO>('/tasks', data),

  update: (id: number, data: Partial<{ title: string; description: string; status: string; priority: string; deadline: string }>) => http.put<unknown, TaskDTO>(`/tasks/${id}`, data),

  delete: (id: number) => http.delete<unknown, void>(`/tasks/${id}`),

  batchUpdateStatus: (ids: number[], status: string, actionId?: string) =>
    http.post<unknown, { updated: number }>('/tasks/batch-update-status', { ids, status, actionId }),

  batchAssign: (ids: number[], assigneeId: number) =>
    http.post<unknown, { updated: number }>('/tasks/batch-assign', { ids, assigneeId }),

  getHistory: (id: number) => http.get<unknown, TaskHistoryEntry[]>(`/tasks/${id}/history`),
}
