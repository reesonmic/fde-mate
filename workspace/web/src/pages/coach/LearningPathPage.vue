<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Card, Steps } from 'ant-design-vue'
import { coachApi } from '@/apis/modules/coach'
import type { LearningPathDTO } from '@/types/business'

const learningPaths = ref<LearningPathDTO[]>([])
const loading = ref(false)

onMounted(async () => {
  loading.value = true
  try {
    learningPaths.value = await coachApi.getLearningPaths()
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="learning-path-page">
    <h2>学习路径</h2>

    <Card v-for="path in learningPaths" :key="path.id" class="path-card">
      <h3>{{ path.name }}</h3>
      <p>{{ path.description }}</p>
      <Steps :current="path.currentStep" :items="path.steps" />
    </Card>

    <p v-if="learningPaths.length === 0" class="empty-message">暂无学习路径</p>
  </div>
</template>

<style scoped>
.learning-path-page h2 {
  margin-bottom: 24px;
}

.path-card {
  margin-bottom: 24px;
}

.path-card h3 {
  margin-bottom: 8px;
}

.path-card p {
  color: var(--color-text-secondary);
  margin-bottom: 16px;
}

.empty-message {
  text-align: center;
  color: var(--color-text-secondary);
  padding: 48px;
}
</style>