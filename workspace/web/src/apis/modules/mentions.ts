import http from '@/apis/http'
import type { MentionSearchResult } from '@/types/api'

export const mentionsApi = {
  /**
   * Search for mentionable objects (tasks, projects, customers, files, users)
   */
  search(query: string, types?: string[]): Promise<MentionSearchResult> {
    return http.get('/v1/mentions/search', {
      params: { query, types: types?.join(',') },
    }).then((res) => res.data)
  },
}