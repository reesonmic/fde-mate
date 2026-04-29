import { http } from '../http'

export const coachApi = {
  listPractices: (params = {}) => http.get<unknown, { items: any[]; total: number }>('/coach/best-practices', { params }),
  getPractice: (id: number) => http.get<unknown, any>(`/coach/best-practices/${id}`),
  listSops: (params = {}) => http.get<unknown, { items: any[]; total: number }>('/coach/sops', { params }),
  getSop: (id: number) => http.get<unknown, any>(`/coach/sops/${id}`),
  listLearningPaths: (page = 1, size = 20) => http.get<unknown, { items: any[]; total: number }>('/coach/learning-paths', { params: { page, size } }),
  getLearningPath: (id: number) => http.get<unknown, any>(`/coach/learning-paths/${id}`),
  updateProgress: (pathId: number, data: { chapter_id: number; progress: number; completed: boolean }) =>
    http.post<unknown, { updated: boolean }>(`/coach/learning-paths/${pathId}/progress`, data),
  getRecommendations: () => http.get<unknown, any>('/coach/recommendations'),
}
