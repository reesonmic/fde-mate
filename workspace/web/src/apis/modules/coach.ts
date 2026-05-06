import { http } from '../http'
import type { BestPracticeDTO, SopDTO, LearningPathDTO } from '@types/business'

export const coachApi = {
  listPractices: (params = {}) => http.get<unknown, { items: BestPracticeDTO[]; total: number }>('/coach/best-practices', { params }),
  getPractice: (id: number) => http.get<unknown, BestPracticeDTO>(`/coach/best-practices/${id}`),
  listSops: (params = {}) => http.get<unknown, { items: SopDTO[]; total: number }>('/coach/sops', { params }),
  getSop: (id: number) => http.get<unknown, SopDTO>(`/coach/sops/${id}`),
  listLearningPaths: (page = 1, size = 20) => http.get<unknown, { items: LearningPathDTO[]; total: number }>('/coach/learning-paths', { params: { page, size } }),
  getLearningPath: (id: number) => http.get<unknown, LearningPathDTO>(`/coach/learning-paths/${id}`),
  updateProgress: (pathId: number, data: { chapter_id: number; progress: number; completed: boolean }) =>
    http.post<unknown, { updated: boolean }>(`/coach/learning-paths/${pathId}/progress`, data),
  getRecommendations: () => http.get<unknown, { items: Array<{ title: string; description: string }> }>('/coach/recommendations'),
}
