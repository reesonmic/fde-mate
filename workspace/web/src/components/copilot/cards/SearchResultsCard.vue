<script setup lang="ts">
interface Props {
  results: Array<{
    id: string
    type: string
    name: string
    score: number
    snippet: string
    metadata?: Record<string, unknown>
  }>
}

const props = defineProps<Props>()
</script>

<template>
  <div class="search-results-card">
    <div class="search-results-header">
      <h4>搜索结果</h4>
      <span class="search-results-count">共 {{ results.length }} 条</span>
    </div>
    <div class="search-results-list">
      <div v-for="result in results" :key="result.id" class="search-results-item">
        <div class="search-results-meta">
          <span class="search-results-type">{{ result.type }}</span>
          <span class="search-results-score">相关度: {{ result.score.toFixed(2) }}</span>
        </div>
        <div class="search-results-name">{{ result.name }}</div>
        <div class="search-results-snippet">{{ result.snippet }}</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.search-results-card {
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  padding: 12px;
}

.search-results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.search-results-header h4 {
  margin: 0;
  font-size: 14px;
}

.search-results-count {
  font-size: 12px;
  color: var(--color-text-secondary);
}

.search-results-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.search-results-item {
  padding: 8px;
  background: var(--color-fill-secondary);
  border-radius: 4px;
}

.search-results-meta {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  margin-bottom: 4px;
}

.search-results-type {
  color: var(--color-primary);
}

.search-results-score {
  color: var(--color-text-secondary);
}

.search-results-name {
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 4px;
}

.search-results-snippet {
  font-size: 13px;
  color: var(--color-text-secondary);
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}
</style>