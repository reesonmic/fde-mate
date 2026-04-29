import { http } from '../http'

export const dashboardApi = {
  summary: () => http.get<unknown, any>('/dashboard/summary'),
  recentTasks: (limit = 10) => http.get<unknown, any[]>('/dashboard/recent-tasks', { params: { limit } }),
  recentProjects: (limit = 5) => http.get<unknown, any[]>('/dashboard/recent-projects', { params: { limit } }),
  notifications: (page = 1, size = 10) => http.get<unknown, any>('/dashboard/notifications', { params: { page, size } }),
  keyEvents: (days = 7) => http.get<unknown, any[]>('/dashboard/key-events', { params: { days } }),
}
