import { http } from '../http'
import type { ProjectCreateRequest, ProjectUpdateRequest } from '@types/api'
import type { ProjectDTO, ProjectMemberDTO, WeeklyReportDTO } from '@types/business'

export const projectsApi = {
  list: (params = {}) => http.get<unknown, { items: ProjectDTO[]; total: number }>('/projects', { params }),
  get: (id: number) => http.get<unknown, ProjectDTO>(`/projects/${id}`),
  create: (data: ProjectCreateRequest) => http.post<unknown, ProjectDTO>('/projects', data),
  update: (id: number, data: ProjectUpdateRequest) => http.put<unknown, ProjectDTO>(`/projects/${id}`, data),
  delete: (id: number) => http.delete<unknown, void>(`/projects/${id}`),
  getMembers: (id: number) => http.get<unknown, ProjectMemberDTO[]>(`/projects/${id}/members`),
  addMember: (id: number, data: { userId: number; role: string }) => http.post<unknown, ProjectMemberDTO>(`/projects/${id}/members`, data),
  removeMember: (id: number, userId: number) => http.delete<unknown, void>(`/projects/${id}/members/${userId}`),
  getHealth: (id: number) => http.get<unknown, { health: number; risk_count: number; overdue_milestones: number }>(`/projects/${id}/health`),
  addRisk: (id: number, data: { title: string; level: string; mitigation?: string }) => http.post<unknown, { id: number; title: string; level: string; mitigation: string; status: string }>(`/projects/${id}/risks`, data),
  listRisks: (id: number) => http.get<unknown, Array<{ id: number; title: string; level: string; mitigation: string; status: string }>>(`/projects/${id}/risks`),
  weeklyReports: (id: number) => http.get<unknown, WeeklyReportDTO[]>(`/projects/${id}/weekly-reports`),
  generateWeeklyReport: (id: number) => http.post<unknown, { status: string }>(`/projects/${id}/weekly-reports`),
}
