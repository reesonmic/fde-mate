import { http } from '../http'

export const filesApi = {
  list: (params = {}) => http.get<unknown, { items: any[]; total: number }>('/files', { params }),
  get: (id: number) => http.get<unknown, any>(`/files/${id}`),
  getTree: () => http.get<unknown, any[]>('/files/tree'),
  getQuota: () => http.get<unknown, { used_bytes: number; total_bytes: number; used_percent: number }>('/files/quota'),
  getUploadToken: (data: { file_name: string; file_size: number; scope?: string; scope_id?: number }) =>
    http.post<unknown, { uploadToken: string; ossKey: string; endpoint: string; bucket: string }>('/files/upload-token', data),
  finalizeUpload: (data: { ossKey: string; file_name: string; file_size: number; scope?: string; scope_id?: number }) =>
    http.post<unknown, any>('/files/finalize-upload', data),
  delete: (id: number) => http.delete<unknown, void>(`/files/${id}`),
  batchDelete: (ids: number[]) => http.post<unknown, { deleted: number }>('/files/batch-delete', { ids }),
  getDownloadUrl: (id: number) => http.get<unknown, { url: string }>(`/files/${id}/download`),
}
