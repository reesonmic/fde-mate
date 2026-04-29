<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Row, Col, Input, Spin, Empty, Tag, Card, Select } from 'ant-design-vue'
import { SearchOutlined } from '@ant-design/icons-vue'
import { useRouter } from 'vue-router'
import { coachApi } from '@apis/modules/coach'
import BestPracticeCard from '@/components/business/BestPracticeCard.vue'

const router = useRouter()
const practices = ref<any[]>([])
const searchQuery = ref('')
const categoryFilter = ref('')
const loading = ref(false)

const filteredPractices = computed(() => {
  let items = practices.value
  if (searchQuery.value) {
    const kw = searchQuery.value.toLowerCase()
    items = items.filter((p) => p.title?.toLowerCase().includes(kw) || p.summary?.toLowerCase().includes(kw))
  }
  if (categoryFilter.value) {
    items = items.filter((p) => p.category === categoryFilter.value)
  }
  return items
})

const categories = computed(() => {
  const cats = new Set(practices.value.map((p) => p.category).filter(Boolean))
  return Array.from(cats)
})

onMounted(async () => {
  loading.value = true
  try {
    const response = await coachApi.listPractices({})
    practices.value = response.items
  } catch (e) {
    console.error('Failed to load best practices', e)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="best-practices-page">
    <div class="page-header">
      <h2>最佳实践</h2>
      <span class="result-count">共 {{ practices.length }} 篇</span>
    </div>

    <div class="filters-bar">
      <Input
        v-model:value="searchQuery"
        placeholder="搜索案例..."
        class="search-input"
      >
        <template #prefix><SearchOutlined /></template>
      </Input>

      <Select
        v-model:value="categoryFilter"
        placeholder="类别筛选"
        class="filter-select"
        allow-clear
      >
        <Select.Option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</Select.Option>
      </Select>
    </div>

    <Spin :spinning="loading">
      <Row :gutter="16">
        <Col v-for="practice in filteredPractices" :key="practice.id" :span="8">
          <BestPracticeCard
            :practice="practice"
            @click="router.push(`/coach/best-practices/${practice.id}`)"
          />
        </Col>
        <Col v-if="filteredPractices.length === 0 && !loading" :span="24">
          <Empty description="暂无最佳实践" />
        </Col>
      </Row>
    </Spin>
  </div>
</template>

<style scoped>
.best-practices-page {
  padding: 24px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.page-header h2 {
  margin: 0;
}

.result-count {
  color: var(--color-text-secondary, #666);
}

.filters-bar {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
}

.search-input {
  width: 240px;
}

.filter-select {
  width: 140px;
}
</style>
