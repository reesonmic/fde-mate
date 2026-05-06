<script setup lang="ts">
import { ref, watch, nextTick, computed } from 'vue'
import MessageRenderer from './MessageRenderer.vue'
import type { CopilotMessage } from '@/types/copilot'

interface Props {
  messages: CopilotMessage[]
  assistantType: string
}

const props = defineProps<Props>()

const containerRef = ref<HTMLElement>()
const showScrollBtn = ref(false)

const sortedMessages = computed(() => {
  return [...props.messages].sort((a, b) => {
    return new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()
  })
})

const scrollToBottom = async (smooth = false) => {
  await nextTick()
  if (containerRef.value) {
    containerRef.value.scrollTo({
      top: containerRef.value.scrollHeight,
      behavior: smooth ? 'smooth' : 'auto',
    })
  }
}

const checkScroll = () => {
  if (containerRef.value) {
    const { scrollTop, scrollHeight, clientHeight } = containerRef.value
    showScrollBtn.value = scrollHeight - scrollTop - clientHeight > 200
  }
}

// Auto-scroll on new messages
watch(
  () => props.messages.length,
  () => scrollToBottom(true),
)

// Auto-scroll on streaming content changes
watch(
  () => props.messages.map((m) => m.content).join(''),
  () => {
    // Only auto-scroll if near bottom
    if (containerRef.value) {
      const { scrollTop, scrollHeight, clientHeight } = containerRef.value
      if (scrollHeight - scrollTop - clientHeight < 300) {
        scrollToBottom(true)
      }
    }
  },
)
</script>

<template>
  <div class="message-list">
    <div ref="containerRef" class="message-list-items" @scroll="checkScroll">
      <!-- Empty state -->
      <div v-if="messages.length === 0" class="message-list-empty">
        <div class="message-list-empty-content">
          <h4>{{
            assistantType === 'task' ? 'T助手 - 任务管理' :
            assistantType === 'project' ? 'P助手 - 项目助手' :
            assistantType === 'coach' ? 'C助手 - 教练咨询' :
            assistantType === 'file' ? 'F助手 - 文件搜索' :
            'AI 对话'
          }}</h4>
          <p>{{
            assistantType === 'task' ? '可以问我: "本周有哪些待办任务？"' :
            assistantType === 'project' ? '可以问我: "帮我生成周报"' :
            assistantType === 'coach' ? '可以问我: "有哪些最佳实践？"' :
            assistantType === 'file' ? '可以问我: "搜索最近的文档"' :
            '输入消息开始对话...'
          }}</p>
        </div>
      </div>

      <!-- Messages -->
      <div
        v-for="message in sortedMessages"
        :key="message.id"
        class="message-item"
        :class="`message-item--${message.role}`"
      >
        <MessageRenderer :message="message" :assistantType="assistantType" />
      </div>
    </div>

    <!-- Scroll to bottom button -->
    <button
      v-if="showScrollBtn"
      class="scroll-bottom-btn"
      @click="scrollToBottom(true)"
    >
      &#8595; 回到底部
    </button>
  </div>
</template>

<style scoped>
.message-list {
  height: 100%;
  position: relative;
}

.message-list-empty {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: var(--color-text-secondary);
  font-size: 14px;
}

.message-list-empty-content {
  text-align: center;
}

.message-list-empty-content h4 {
  margin: 0 0 8px;
  color: var(--color-text);
}

.message-list-items {
  display: flex;
  flex-direction: column;
  gap: 16px;
  height: 100%;
  overflow-y: auto;
  padding: 12px;
  scroll-behavior: smooth;
}

.message-item {
  display: flex;
}

.message-item--user {
  justify-content: flex-end;
}

.message-item--assistant {
  justify-content: flex-start;
}

.scroll-bottom-btn {
  position: absolute;
  bottom: 16px;
  left: 50%;
  transform: translateX(-50%);
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border);
  border-radius: 20px;
  padding: 6px 16px;
  font-size: 12px;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: opacity 0.2s;
}

.scroll-bottom-btn:hover {
  background: var(--color-fill);
}
</style>
