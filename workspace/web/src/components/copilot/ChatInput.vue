<script setup lang="ts">
import { ref } from 'vue'
import { Input, Button } from 'ant-design-vue'
import MentionPicker from './MentionPicker.vue'
import { useMention } from '@/composables/useMention'
import type { TaskDTO, ProjectDTO, CustomerDTO, FileDTO, UserDTO } from '@/types/business'

type MentionItem = TaskDTO | ProjectDTO | CustomerDTO | FileDTO | UserDTO

const emit = defineEmits<{
  send: [content: string, mentions: MentionItem[]]
}>()

const inputValue = ref('')
const showMentionPicker = ref(false)
const mention = useMention()

const handleInput = (e: InputEvent) => {
  const target = e.target as HTMLInputElement
  const value = target.value

  // Check for @ trigger
  if (value.endsWith('@')) {
    showMentionPicker.value = true
    mention.search('')
  } else if (value.includes('@')) {
    // Extract the query after @
    const atIndex = value.lastIndexOf('@')
    const query = value.slice(atIndex + 1)
    if (query && !query.includes(' ')) {
      showMentionPicker.value = true
      mention.search(query)
    } else {
      showMentionPicker.value = false
    }
  } else {
    showMentionPicker.value = false
  }

  inputValue.value = value
}

const handleSelectMention = (item: MentionItem) => {
  // Replace @query with @name
  const atIndex = inputValue.value.lastIndexOf('@')
  inputValue.value = inputValue.value.slice(0, atIndex) + `@${item.name} `
  showMentionPicker.value = false
  mention.addMention(item)
}

const handleSend = () => {
  if (!inputValue.value.trim()) return

  emit('send', inputValue.value, mention.getMentions())
  inputValue.value = ''
  mention.clearMentions()
}

const handleKeyDown = (e: KeyboardEvent) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    handleSend()
  }
}
</script>

<template>
  <div class="chat-input">
    <div class="chat-input-wrapper">
      <Input.TextArea
        v-model:value="inputValue"
        placeholder="输入消息... (@ 提引用)"
        :autoSize="{ minRows: 1, maxRows: 4 }"
        @input="handleInput"
        @keydown="handleKeyDown"
        class="chat-input-field"
      />
      <MentionPicker
        v-if="showMentionPicker"
        :results="mention.results"
        @select="handleSelectMention"
        @close="showMentionPicker = false"
      />
    </div>
    <Button type="primary" @click="handleSend" class="chat-input-send">
      发送
    </Button>
  </div>
</template>

<style scoped>
.chat-input {
  display: flex;
  gap: 8px;
  align-items: flex-end;
}

.chat-input-wrapper {
  flex: 1;
  position: relative;
}

.chat-input-field {
  resize: none;
}

.chat-input-send {
  height: 32px;
}
</style>