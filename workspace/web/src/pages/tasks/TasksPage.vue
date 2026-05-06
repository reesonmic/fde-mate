<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { Tabs, Button, Input, Select, Space, Modal, Form, Tag, DatePicker, message, Spin, Dropdown, Menu, Checkbox } from 'ant-design-vue'
import { PlusOutlined, SearchOutlined, FilterOutlined, MoreOutlined } from '@ant-design/icons-vue'
import KanbanBoard from '@/components/business/KanbanBoard.vue'
import TaskRow from '@/components/business/TaskRow.vue'
import { useTasksStore } from '@/stores/tasks'
import { tasksApi } from '@/apis/modules/tasks'
import type { TaskDTO } from '@/types/business'
import dayjs from 'dayjs'

const tasksStore = useTasksStore()
const activeTab = ref('list')
const searchKeyword = ref('')
const showCreateModal = ref(false)
const createLoading = ref(false)

const filters = reactive({
  status: [] as string[],
  priority: [] as string[],
})

const createForm = reactive({
  title: '',
  description: '',
  priority: 'p2' as string,
  deadline: undefined as dayjs.Dayjs | undefined,
  project_id: undefined as number | undefined,
})

const pagination = reactive({
  current: 1,
  pageSize: 20,
  total: 0,
})

const filteredTasks = computed(() => {
  let items = tasksStore.tasks

  if (searchKeyword.value) {
    const kw = searchKeyword.value.toLowerCase()
    items = items.filter((t) => t.title.toLowerCase().includes(kw))
  }

  if (filters.status.length > 0) {
    items = items.filter((t) => filters.status.includes(t.status))
  }

  if (filters.priority.length > 0) {
    items = items.filter((t) => filters.priority.includes(t.priority))
  }

  return items
})

const statusOptions = [
  { label: '待办', value: 'todo' },
  { label: '进行中', value: 'in_progress' },
  { label: '审核中', value: 'review' },
  { label: '已阻塞', value: 'blocked' },
  { label: '已完成', value: 'done' },
]

const priorityOptions = [
  { label: 'P0', value: 'p0' },
  { label: 'P1', value: 'p1' },
  { label: 'P2', value: 'p2' },
  { label: 'P3', value: 'p3' },
]

const statusColor = (status: string) => {
  const map: Record<string, string> = {
    todo: 'default',
    in_progress: 'processing',
    review: 'cyan',
    blocked: 'error',
    done: 'success',
  }
  return map[status] || 'default'
}

const statusLabel = (status: string) => {
  const map: Record<string, string> = {
    todo: '待办',
    in_progress: '进行中',
    review: '审核中',
    blocked: '已阻塞',
    done: '已完成',
  }
  return map[status] || status
}

const priorityColor = (priority: string) => {
  const map: Record<string, string> = {
    p0: 'red',
    p1: 'orange',
    p2: 'blue',
    p3: 'default',
  }
  return map[priority] || 'default'
}

const priorityLabel = (priority: string) => {
  const map: Record<string, string> = {
    p0: 'P0',
    p1: 'P1',
    p2: 'P2',
    p3: 'P3',
  }
  return map[priority] || priority
}

const kanbanColumns = computed(() => {
  return [
    { key: 'todo', title: '待办' },
    { key: 'in_progress', title: '进行中' },
    { key: 'review', title: '审核中' },
    { key: 'blocked', title: '已阻塞' },
    { key: 'done', title: '已完成' },
  ]
})

const handleCreateTask = async () => {
  if (!createForm.title.trim()) {
    message.warning('请输入任务标题')
    return
  }
  createLoading.value = true
  try {
    await tasksApi.create({
      title: createForm.title,
      description: createForm.description,
      priority: createForm.priority,
      dueAt: createForm.deadline?.toISOString?.() ?? createForm.deadline,
      project_id: createForm.project_id,
    })
    message.success('创建成功')
    showCreateModal.value = false
    Object.assign(createForm, { title: '', description: '', priority: 'p2', deadline: undefined, project_id: undefined })
    await tasksStore.loadTasks()
  } catch {
    message.error('创建失败')
  } finally {
    createLoading.value = false
  }
}

const handleDeleteTask = async (id: number) => {
  Modal.confirm({
    title: '确认删除',
    content: '确定要删除此任务吗？',
    okText: '删除',
    okType: 'danger',
    cancelText: '取消',
    onOk: async () => {
      try {
        await tasksApi.delete(id)
        message.success('删除成功')
        await tasksStore.loadTasks()
      } catch {
        message.error('删除失败')
      }
    },
  })
}

const handleStatusChange = async (task: TaskDTO, newStatus: string) => {
  try {
    await tasksApi.update(Number(task.id), { status: newStatus })
    message.success('状态已更新')
    await tasksStore.loadTasks()
  } catch {
    message.error('更新失败')
  }
}

const handlePageChange = (page: number) => {
  pagination.current = page
  loadData()
}

const resetFilters = () => {
  searchKeyword.value = ''
  filters.status = []
  filters.priority = []
  loadData()
}

const loadData = async () => {
  await tasksStore.loadTasks({
    keyword: searchKeyword.value || undefined,
    status: filters.status,
    priority: filters.priority,
    page: pagination.current,
    size: pagination.pageSize,
  })
}

onMounted(async () => {
  await loadData()
  await tasksStore.loadKanban()
})
</script>

<template>
  <div class="tasks-page">
    <div class="tasks-header">
      <h2>任务管理</h2>
      <Button type="primary" @click="showCreateModal = true">
        <PlusOutlined />
        新建任务
      </Button>
    </div>

    <!-- Filters -->
    <div class="filters-bar">
      <Input
        v-model:value="searchKeyword"
        placeholder="搜索任务..."
        class="search-input"
        @pressEnter="loadData"
      >
        <template #prefix><SearchOutlined /></template>
      </Input>

      <Select
        v-model:value="filters.status"
        mode="multiple"
        placeholder="状态筛选"
        class="filter-select"
        allow-clear
      >
        <Select.Option v-for="opt in statusOptions" :key="opt.value" :value="opt.value">
          {{ opt.label }}
        </Select.Option>
      </Select>

      <Select
        v-model:value="filters.priority"
        mode="multiple"
        placeholder="优先级筛选"
        class="filter-select"
        allow-clear
      >
        <Select.Option v-for="opt in priorityOptions" :key="opt.value" :value="opt.value">
          {{ opt.label }}
        </Select.Option>
      </Select>

      <Button @click="resetFilters">重置</Button>
    </div>

    <!-- Tabs: List / Kanban -->
    <Tabs v-model:activeKey="activeTab">
      <Tabs.TabPane key="list" tab="列表视图">
        <Spin :spinning="tasksStore.loading">
          <div class="task-list">
            <TaskRow
              v-for="task in filteredTasks"
              :key="task.id"
              :task="task"
              @click="() => {}"
              @delete="(id: number) => handleDeleteTask(id)"
              @status-change="(newStatus: string) => handleStatusChange(task, newStatus)"
            />
            <div v-if="filteredTasks.length === 0" class="empty-text">
              暂无任务
            </div>
          </div>

          <div class="pagination-bar">
            <Space>
              <Button
                :disabled="pagination.current <= 1"
                @click="handlePageChange(pagination.current - 1)"
              >
                上一页
              </Button>
              <span>第 {{ pagination.current }} 页</span>
              <Button
                @click="handlePageChange(pagination.current + 1)"
              >
                下一页
              </Button>
            </Space>
          </div>
        </Spin>
      </Tabs.TabPane>

      <Tabs.TabPane key="kanban" tab="看板视图">
        <Spin :spinning="tasksStore.loading">
          <KanbanBoard
            :tasks-by-status="tasksStore.kanbanData"
            @status-change="handleStatusChange"
          />
        </Spin>
      </Tabs.TabPane>
    </Tabs>

    <!-- Create Task Modal -->
    <Modal
      v-model:visible="showCreateModal"
      title="新建任务"
      @ok="handleCreateTask"
      :confirmLoading="createLoading"
    >
      <Form :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
        <Form.Item label="标题" required>
          <Input v-model:value="createForm.title" placeholder="输入任务标题" />
        </Form.Item>
        <Form.Item label="描述">
          <Input.TextArea v-model:value="createForm.description" :rows="3" placeholder="输入任务描述" />
        </Form.Item>
        <Form.Item label="优先级">
          <Select v-model:value="createForm.priority">
            <Select.Option value="p0">P0</Select.Option>
            <Select.Option value="p1">P1</Select.Option>
            <Select.Option value="p2">P2</Select.Option>
            <Select.Option value="p3">P3</Select.Option>
          </Select>
        </Form.Item>
        <Form.Item label="截止日期">
          <DatePicker v-model:value="createForm.deadline" style="width: 100%" />
        </Form.Item>
      </Form>
    </Modal>
  </div>
</template>

<style scoped>
.tasks-page {
  padding: 24px;
}

.tasks-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.tasks-header h2 {
  margin: 0;
}

.filters-bar {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.search-input {
  width: 240px;
}

.filter-select {
  width: 160px;
}

.task-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  min-height: 200px;
}

.empty-text {
  text-align: center;
  color: var(--color-text-secondary, #666);
  padding: 48px;
}

.pagination-bar {
  margin-top: 16px;
  display: flex;
  justify-content: center;
}

:deep(.ant-tabs-content) {
  padding-top: 8px;
}
</style>
