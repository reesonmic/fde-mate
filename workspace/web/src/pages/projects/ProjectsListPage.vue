<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { Card, Row, Col, Button, Select, Input, Modal, Form, message, Tag, Spin } from 'ant-design-vue'
import { PlusOutlined, SearchOutlined } from '@ant-design/icons-vue'
import { useRouter } from 'vue-router'
import { useProjectsStore } from '@/stores/projects'
import { projectsApi } from '@/apis/modules/projects'
import type { ProjectDTO } from '@/types/business'

const router = useRouter()
const projectsStore = useProjectsStore()
const showCreateModal = ref(false)
const createLoading = ref(false)
const searchKeyword = ref('')
const phaseFilter = ref<string[]>([])

const createForm = reactive({
  name: '',
})

const phaseOptions = [
  { label: '初始化', value: 'init' },
  { label: '探索', value: 'discovery' },
  { label: '交付', value: 'delivery' },
  { label: '审核', value: 'review' },
  { label: '关闭', value: 'closed' },
]

const phaseColor = (phase: string) => {
  const map: Record<string, string> = {
    init: 'default',
    discovery: 'processing',
    delivery: 'blue',
    review: 'cyan',
    closed: 'default',
  }
  return map[phase] || 'default'
}

const phaseLabel = (phase: string) => {
  const map: Record<string, string> = {
    init: '初始化',
    discovery: '探索',
    delivery: '交付',
    review: '审核',
    closed: '关闭',
  }
  return map[phase] || phase
}

const filteredProjects = ref<ProjectDTO[]>([])

const loadData = async () => {
  await projectsStore.loadProjects({})
  filteredProjects.value = projectsStore.projects
}

const handleSearch = () => {
  let items = projectsStore.projects

  if (searchKeyword.value) {
    const kw = searchKeyword.value.toLowerCase()
    items = items.filter((p) => p.name.toLowerCase().includes(kw) || p.owner_name?.toLowerCase().includes(kw))
  }

  if (phaseFilter.value.length > 0) {
    items = items.filter((p) => phaseFilter.value.includes(p.phase))
  }

  filteredProjects.value = items
}

const handleCreate = async () => {
  if (!createForm.name.trim()) {
    message.warning('请输入项目名称')
    return
  }
  createLoading.value = true
  try {
    await projectsApi.create({
      name: createForm.name,
      description: createForm.description,
    })
    message.success('创建成功')
    showCreateModal.value = false
    Object.assign(createForm, { name: '' })
    await loadData()
  } catch {
    message.error('创建失败')
  } finally {
    createLoading.value = false
  }
}

const handleDelete = async (id: number, e: Event) => {
  e.stopPropagation()
  Modal.confirm({
    title: '确认删除',
    content: '确定要删除此项目吗？此操作不可撤销。',
    okText: '删除',
    okType: 'danger',
    cancelText: '取消',
    onOk: async () => {
      try {
        await projectsApi.delete(id)
        message.success('删除成功')
        await loadData()
      } catch {
        message.error('删除失败')
      }
    },
  })
}

onMounted(async () => {
  await loadData()
})
</script>

<template>
  <div class="projects-list-page">
    <div class="page-header">
      <h2>项目空间</h2>
      <Button type="primary" @click="showCreateModal = true">
        <PlusOutlined />
        创建项目
      </Button>
    </div>

    <!-- Filters -->
    <div class="filters-bar">
      <Input
        v-model:value="searchKeyword"
        placeholder="搜索项目..."
        class="search-input"
        @pressEnter="handleSearch"
      >
        <template #prefix><SearchOutlined /></template>
      </Input>

      <Select
        v-model:value="phaseFilter"
        mode="multiple"
        placeholder="阶段筛选"
        class="filter-select"
        allow-clear
        @change="handleSearch"
      >
        <Select.Option v-for="opt in phaseOptions" :key="opt.value" :value="opt.value">
          {{ opt.label }}
        </Select.Option>
      </Select>

      <span class="result-count">共 {{ filteredProjects.length }} 个项目</span>
    </div>

    <!-- Project Cards -->
    <Spin :spinning="projectsStore.loading">
      <Row :gutter="[16, 16]">
        <Col
          v-for="project in filteredProjects"
          :key="project.id"
          :xs="24"
          :sm="12"
          :md="8"
          :lg="6"
        >
          <Card hoverable class="project-card" @click="router.push(`/projects/${project.id}`)">
            <template #title>
              <div class="project-title">
                <span class="project-name">{{ project.name }}</span>
                <Tag :color="phaseColor(project.phase)">{{ phaseLabel(project.phase) }}</Tag>
              </div>
            </template>
            <template #extra>
              <Button
                type="text"
                danger
                size="small"
                @click="handleDelete(project.id, $event)"
              >
                删除
              </Button>
            </template>
            <p class="project-meta">负责人: {{ project.owner_name || '-' }}</p>
            <div class="project-health">
              <span>健康度</span>
              <span :class="project.health >= 80 ? 'health-good' : project.health >= 60 ? 'health-warning' : 'health-bad'">
                {{ project.health }}%
              </span>
            </div>
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: `${project.health}%` }"></div>
            </div>
          </Card>
        </Col>
      </Row>

      <div v-if="filteredProjects.length === 0 && !projectsStore.loading" class="empty-text">
        暂无项目数据
      </div>
    </Spin>

    <!-- Create Modal -->
    <Modal
      v-model:visible="showCreateModal"
      title="创建新项目"
      @ok="handleCreate"
      :confirmLoading="createLoading"
    >
      <Form :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
        <Form.Item label="名称" required>
          <Input v-model:value="createForm.name" placeholder="输入项目名称" />
        </Form.Item>
        <Form.Item label="描述">
          <Input.TextArea v-model:value="createForm.description" :rows="3" placeholder="输入项目描述" />
        </Form.Item>
      </Form>
    </Modal>
  </div>
</template>

<style scoped>
.projects-list-page {
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
  align-items: center;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.search-input {
  width: 240px;
}

.filter-select {
  width: 160px;
}

.result-count {
  color: var(--color-text-secondary, #666);
  font-size: 14px;
}

.project-card {
  height: 100%;
}

.project-card :deep(.ant-card-head-title) {
  white-space: normal;
}

.project-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
}

.project-name {
  font-weight: 500;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.project-desc {
  color: var(--color-text-secondary, #666);
  font-size: 13px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin: 8px 0;
}

.project-meta {
  font-size: 13px;
  color: var(--color-text-secondary, #666);
}

.project-health {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  margin-top: 8px;
  color: var(--color-text-secondary, #666);
}

.health-good { color: #52c41a; }
.health-warning { color: #faad14; }
.health-bad { color: #ff4d4f; }

.progress-bar {
  height: 4px;
  background: #f0f0f0;
  border-radius: 2px;
  margin-top: 12px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: #1677ff;
  border-radius: 2px;
  transition: width 0.3s;
}

.empty-text {
  text-align: center;
  color: var(--color-text-secondary, #666);
  padding: 48px;
}
</style>
