<script setup lang="ts">
interface Props {
  report: {
    title: string
    summary: string
    sections: Array<{
      title: string
      content: string
    }>
    generatedAt: string
  }
}

const props = defineProps<Props>()
</script>

<template>
  <div class="report-card">
    <div class="report-card-header">
      <h4>{{ report.title }}</h4>
      <span class="report-card-time">{{ report.generatedAt }}</span>
    </div>
    <div class="report-card-summary">
      {{ report.summary }}
    </div>
    <div class="report-card-sections">
      <div v-for="section in report.sections" :key="section.title" class="report-card-section">
        <h5>{{ section.title }}</h5>
        <p>{{ section.content }}</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.report-card {
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  padding: 16px;
}

.report-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.report-card-header h4 {
  margin: 0;
  font-size: 16px;
}

.report-card-time {
  font-size: 12px;
  color: var(--color-text-secondary);
}

.report-card-summary {
  font-size: 14px;
  margin-bottom: 16px;
  color: var(--color-text);
}

.report-card-sections {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.report-card-section h5 {
  margin: 0;
  font-size: 14px;
  color: var(--color-primary);
}

.report-card-section p {
  margin: 4px 0 0;
  font-size: 13px;
  color: var(--color-text-secondary);
}
</style>