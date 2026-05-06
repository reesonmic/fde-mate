import { http } from '@/apis/http'
import type { MentionSearchResult } from '@/types/api'

export const mentionsApi = {
  search: (query: string, types?: string[]) =>
    http.get<unknown, MentionSearchResult>('/mentions/search', { params: { query, types: types?.join(',') } }),
}