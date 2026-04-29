import { http } from '../http'
import type { Task, TaskStatus, TaskPriority } from '@types/business'

export interface TaskListParams {
  keyword?: string
  status?: TaskStatus[]
  assigneeId?: number
  projectId?: number
  priority?: TaskPriority[]
  page?: number
  size?: number
}

export const tasksApi = {
  list: (params: TaskListParams = {}) =>
    http.get<unknown, { items: Task[]; total: number; page: number; size: number }>('/tasks', { params }),

  get: (id: number) => http.get<unknown, Task>(`/tasks/${id}`),

  create: (data: Partial<Task>) => http.post<unknown, Task>('/tasks', data),

  update: (id: number, data: Partial<Task>) => http.put<unknown, Task>(`/tasks/${id}`, data),

  delete: (id: number) => http.delete<unknown, void>(`/tasks/${id}`),

  batchUpdateStatus: (ids: number[], status: TaskStatus, actionId?: string) =>
    http.post<unknown, { updated: number }>('/tasks/batch-update-status', { ids, status, actionId }),

  batchAssign: (ids: number[], assigneeId: number) =>
    http.post<unknown, { updated: number }>('/tasks/batch-assign', { ids, assigneeId }),

  getHistory: (id: number) => http.get<unknown, any[]>(`/tasks/${id}/history`),
}
