<script setup lang="ts">
import { computed } from 'vue'
import ActionCard from './cards/ActionCard.vue'
import ReportCard from './cards/ReportCard.vue'
import NextStepsCard from './cards/NextStepsCard.vue'
import SearchResultsCard from './cards/SearchResultsCard.vue'
import type { CopilotMessage } from '@/types/copilot'

interface Props {
  message: CopilotMessage
  assistantType: string
}

const props = defineProps<Props>()

const isUser = computed(() => props.message.role === 'user')

const messageClass = computed(() => {
  return isUser.value ? 'message-renderer--user' : 'message-renderer--assistant'
})
</script>

<template>
  <div class="message-renderer" :class="messageClass">
    <!-- User message -->
    <div v-if="isUser" class="message-content message-content--user">
      {{ message.content }}
    </div>

    <!-- Assistant message -->
    <div v-else class="message-content message-content--assistant">
      <!-- Plain text response -->
      <div v-if="message.type === 'text'" class="message-text">
        {{ message.content }}
      </div>

      <!-- Action card (requires confirmation) -->
      <ActionCard
        v-else-if="message.type === 'action'"
        :action="message.metadata"
        :assistantType="assistantType"
      />

      <!-- Report card -->
      <ReportCard
        v-else-if="message.type === 'report'"
        :report="message.metadata"
      />

      <!-- Next steps card -->
      <NextStepsCard
        v-else-if="message.type === 'nextSteps'"
        :steps="message.metadata?.steps || []"
      />

      <!-- Search results card -->
      <SearchResultsCard
        v-else-if="message.type === 'searchResults'"
        :results="message.metadata?.results || []"
      />

      <!-- Fallback to text -->
      <div v-else class="message-text">
        {{ message.content }}
      </div>
    </div>
  </div>
</template>

<style scoped>
.message-renderer {
  max-width: 90%;
}

.message-renderer--user {
  align-self: flex-end;
}

.message-renderer--assistant {
  align-self: flex-start;
}

.message-content {
  padding: 12px 16px;
  border-radius: 8px;
}

.message-content--user {
  background: var(--color-primary);
  color: white;
}

.message-content--assistant {
  background: var(--color-bg-elevated);
  color: var(--color-text);
}

.message-text {
  font-size: 14px;
  line-height: 1.5;
}
</style>