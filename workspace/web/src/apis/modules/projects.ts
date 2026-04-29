import { http } from '../http'
import type { Project } from '@types/business'

export const projectsApi = {
  list: (params = {}) => http.get<unknown, { items: Project[]; total: number }>('/projects', { params }),
  get: (id: number) => http.get<unknown, Project>(`/projects/${id}`),
  create: (data: any) => http.post<unknown, Project>('/projects', data),
  update: (id: number, data: any) => http.put<unknown, Project>(`/projects/${id}`, data),
  delete: (id: number) => http.delete<unknown, void>(`/projects/${id}`),
  getMembers: (id: number) => http.get<unknown, any[]>(`/projects/${id}/members`),
  addMember: (id: number, data: { userId: number; role: string }) => http.post<unknown, any>(`/projects/${id}/members`, data),
  removeMember: (id: number, userId: number) => http.delete<unknown, void>(`/projects/${id}/members/${userId}`),
  getHealth: (id: number) => http.get<unknown, { health: number; risk_count: number; overdue_milestones: number }>(`/projects/${id}/health`),
  addRisk: (id: number, data: any) => http.post<unknown, any>(`/projects/${id}/risks`, data),
  weeklyReports: (id: number) => http.get<unknown, any[]>(`/projects/${id}/weekly-reports`),
  generateWeeklyReport: (id: number) => http.post<unknown, any>(`/projects/${id}/weekly-reports`),
}
