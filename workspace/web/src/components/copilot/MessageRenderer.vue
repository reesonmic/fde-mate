<script setup lang="ts">
import { computed } from 'vue'
import { marked } from 'marked'
import DOMPurify from 'dompurify'
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

const renderedContent = computed(() => {
  if (isUser.value || props.message.type === 'text') {
    const text = props.message.content || ''
    let html: string
    // Basic code block detection
    if (text.includes('```')) {
      html = marked.parse(text, { async: false }) as string
    } else {
      // Escape HTML for plain text
      html = text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/\n/g, '<br>')
    }
    return DOMPurify.sanitize(html)
  }
  // Fallback: sanitize any non-text/unknown message types
  return DOMPurify.sanitize(props.message.content || '')
})

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
      <div
        v-if="message.type === 'text'"
        class="message-text"
        v-html="renderedContent"
      ></div>

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
      <div v-else class="message-text" v-html="renderedContent"></div>
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
  line-height: 1.6;
}

.message-text :deep(pre) {
  background: var(--color-fill-tertiary);
  padding: 12px;
  border-radius: 6px;
  overflow-x: auto;
  font-size: 13px;
}

.message-text :deep(code) {
  background: var(--color-fill-secondary);
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 13px;
  font-family: 'SF Mono', 'Fira Code', monospace;
}

.message-text :deep(pre code) {
  background: none;
  padding: 0;
}

.message-text :deep(p) {
  margin: 8px 0;
}

.message-text :deep(p:first-child) {
  margin-top: 0;
}

.message-text :deep(p:last-child) {
  margin-bottom: 0;
}

.message-text :deep(ul),
.message-text :deep(ol) {
  padding-left: 20px;
  margin: 8px 0;
}

.message-text :deep(li) {
  margin: 4px 0;
}

.message-text :deep(strong) {
  font-weight: 600;
}

.message-text :deep(table) {
  border-collapse: collapse;
  width: 100%;
  margin: 8px 0;
  font-size: 13px;
}

.message-text :deep(th),
.message-text :deep(td) {
  border: 1px solid var(--color-border);
  padding: 6px 12px;
  text-align: left;
}

.message-text :deep(th) {
  background: var(--color-fill-tertiary);
  font-weight: 600;
}
</style>
