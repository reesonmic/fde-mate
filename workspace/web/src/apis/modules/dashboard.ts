import { http } from '../http'

export interface DashboardSummary {
  task_count: number
  project_count: number
  customer_count: number
  pending_tasks: number
}

export interface DashboardKeyEvent {
  id: number
  type: string
  title: string
  gmt_create: string
}

export const dashboardApi = {
  summary: () => http.get<unknown, DashboardSummary>('/dashboard/summary'),
  recentTasks: (limit = 10) => http.get<unknown, Array<{ id: number; title: string; status: string; priority: string; gmt_create: string }>>('/dashboard/recent-tasks', { params: { limit } }),
  recentProjects: (limit = 5) => http.get<unknown, Array<{ id: number; name: string; phase: string; health: number }>>('/dashboard/recent-projects', { params: { limit } }),
  notifications: (page = 1, size = 10) => http.get<unknown, { items: Array<{ id: number; title: string; read: boolean }>; total: number }>('/dashboard/notifications', { params: { page, size } }),
  keyEvents: (days = 7) => http.get<unknown, DashboardKeyEvent[]>('/dashboard/key-events', { params: { days } }),
}
