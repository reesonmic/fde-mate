import { http } from '../http'

interface FileMetaDTO {
  id: number
  name: string
  ext: string
  size: number
  scope: string
  scope_id: number | null
  owner_id: number
  oss_key: string
  rag_indexed: number
  gmt_create: string
  gmt_modified: string
}

interface FileTreeNode {
  key: string
  title: string
  is_leaf: boolean
  children?: FileTreeNode[]
}

export const filesApi = {
  list: (params = {}) => http.get<unknown, { items: FileMetaDTO[]; total: number }>('/files', { params }),
  get: (id: number) => http.get<unknown, FileMetaDTO>(`/files/${id}`),
  getTree: () => http.get<unknown, FileTreeNode[]>('/files/tree'),
  getQuota: () => http.get<unknown, { used_bytes: number; total_bytes: number; used_percent: number }>('/files/quota'),
  getUploadToken: (data: { file_name: string; file_size: number; scope?: string; scope_id?: number }) =>
    http.post<unknown, { upload_token: string; oss_key: string; endpoint: string; bucket: string }>('/files/upload-token', data),
  finalizeUpload: (data: { oss_key: string; file_name: string; file_size: number; scope?: string; scope_id?: number }) =>
    http.post<unknown, FileMetaDTO>('/files/finalize-upload', data),
  delete: (id: number) => http.delete<unknown, void>(`/files/${id}`),
  batchDelete: (ids: number[]) => http.post<unknown, { deleted: number }>('/files/batch-delete', { ids }),
  getDownloadUrl: (id: number) => http.get<unknown, { url: string }>(`/files/${id}/download`),
}
