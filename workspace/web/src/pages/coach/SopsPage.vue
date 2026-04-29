<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Row, Col, Input, Spin, Empty, Tag, Select } from 'ant-design-vue'
import { SearchOutlined } from '@ant-design/icons-vue'
import { useRouter } from 'vue-router'
import { coachApi } from '@apis/modules/coach'
import SopCard from '@/components/business/SopCard.vue'

const router = useRouter()
const sops = ref<any[]>([])
const searchQuery = ref('')
const statusFilter = ref('')
const loading = ref(false)

const filteredSops = computed(() => {
  let items = sops.value
  if (searchQuery.value) {
    const kw = searchQuery.value.toLowerCase()
    items = items.filter((s) => s.title?.toLowerCase().includes(kw))
  }
  if (statusFilter.value) {
    items = items.filter((s) => s.status === statusFilter.value)
  }
  return items
})

const statusOptions = ['active', 'draft', 'archived']

const statusLabel = (s: string) => {
  const map: Record<string, string> = { active: '生效', draft: '草稿', archived: '归档' }
  return map[s] || s
}

const statusColor = (s: string) => {
  const map: Record<string, string> = { active: 'success', draft: 'default', archived: 'error' }
  return map[s] || 'default'
}

onMounted(async () => {
  loading.value = true
  try {
    const response = await coachApi.listSops({})
    sops.value = response.items
  } catch (e) {
    console.error('Failed to load SOPs', e)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="sops-page">
    <div class="page-header">
      <h2>SOP库</h2>
      <span class="result-count">共 {{ sops.length }} 个</span>
    </div>

    <div class="filters-bar">
      <Input
        v-model:value="searchQuery"
        placeholder="搜索SOP..."
        class="search-input"
      >
        <template #prefix><SearchOutlined /></template>
      </Input>

      <Select
        v-model:value="statusFilter"
        placeholder="状态筛选"
        class="filter-select"
        allow-clear
      >
        <Select.Option v-for="s in statusOptions" :key="s" :value="s">
          <Tag :color="statusColor(s)">{{ statusLabel(s) }}</Tag>
        </Select.Option>
      </Select>
    </div>

    <Spin :spinning="loading">
      <Row :gutter="16">
        <Col v-for="sop in filteredSops" :key="sop.id" :span="8">
          <SopCard :sop="sop" @click="router.push(`/coach/sops/${sop.id}`)" />
        </Col>
        <Col v-if="filteredSops.length === 0 && !loading" :span="24">
          <Empty description="暂无SOP" />
        </Col>
      </Row>
    </Spin>
  </div>
</template>

<style scoped>
.sops-page {
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
