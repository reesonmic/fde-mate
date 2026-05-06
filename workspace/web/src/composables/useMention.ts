import { ref, computed } from 'vue'
import { mentionsApi } from '@/apis/modules/mentions'
import debounce from 'lodash-es/debounce'
import type { TaskDTO, ProjectDTO, CustomerDTO, FileDTO, UserDTO } from '@/types/business'
import type { MentionSearchResult } from '@/types/api'

type MentionItem = TaskDTO | ProjectDTO | CustomerDTO | FileDTO | UserDTO

/**
 * Mention composable for @ reference functionality
 */
export function useMention() {
  const results = ref<MentionSearchResult>({
    tasks: [],
    projects: [],
    customers: [],
    files: [],
    users: [],
  })

  const loading = ref(false)
  const selectedMentions = ref<MentionItem[]>([])

  const search = debounce(async (query: string) => {
    loading.value = true
    try {
      const response = await mentionsApi.search(query)
      results.value = response
    } finally {
      loading.value = false
    }
  }, 300)

  const addMention = (item: MentionItem) => {
    // Check if already added
    if (!selectedMentions.value.find((m) => m.id === item.id)) {
      selectedMentions.value.push(item)
    }
  }

  const removeMention = (id: string) => {
    selectedMentions.value = selectedMentions.value.filter((m) => m.id !== id)
  }

  const getMentions = () => {
    return selectedMentions.value
  }

  const clearMentions = () => {
    selectedMentions.value = []
  }

  return {
    results,
    loading,
    selectedMentions,
    search,
    addMention,
    removeMention,
    getMentions,
    clearMentions,
  }
}