<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Card, Statistic, Row, Col, Spin, List, Tag, Timeline } from 'ant-design-vue'
import {
  CheckCircleOutlined,
  ClockCircleOutlined,
  FolderOutlined,
  FileTextOutlined,
} from '@ant-design/icons-vue'
import { dashboardApi } from '@apis/modules/dashboard'
import type { DashboardSummary, DashboardKeyEvent } from '@apis/modules/dashboard'
import { useRouter } from 'vue-router'

const router = useRouter()
const loading = ref(false)
const summary = ref<DashboardSummary | null>(null)
const recentTasks = ref<Array<{ id: number; title: string; status: string; priority: string; gmt_create: string }>>([])
const recentProjects = ref<Array<{ id: number; name: string; phase: string; health: number }>>([])
const notifications = ref<Array<{ id: number; title: string; read: boolean }>>([])
const keyEvents = ref<DashboardKeyEvent[]>([])

const taskCompletionRate = computed(() => {
  if (!summary.value) return 0
  const { task_count, pending_tasks } = summary.value
  return task_count ? Math.round(((task_count - pending_tasks) / task_count) * 100) : 0
})

onMounted(async () => {
  loading.value = true
  try {
    const [summaryRes, tasksRes, projectsRes, notificationsRes, eventsRes] = await Promise.all([
      dashboardApi.summary(),
      dashboardApi.recentTasks(5),
      dashboardApi.recentProjects(5),
      dashboardApi.notifications(1, 5),
      dashboardApi.keyEvents(7),
    ])
    summary.value = summaryRes
    recentTasks.value = tasksRes
    recentProjects.value = projectsRes
    notifications.value = notificationsRes.items || []
    keyEvents.value = eventsRes
  } catch (e) {
    console.error('Failed to load dashboard data', e)
  } finally {
    loading.value = false
  }
})

const statusColor = (status: string) => {
  const map: Record<string, string> = {
    todo: 'default',
    in_progress: 'processing',
    blocked: 'error',
    done: 'success',
  }
  return map[status] || 'default'
}

const statusLabel = (status: string) => {
  const map: Record<string, string> = {
    todo: '待办',
    in_progress: '进行中',
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
</script>

<template>
  <div class="dashboard-page">
    <Spin :spinning="loading">
      <div class="dashboard-header">
        <h2>仪表盘</h2>
        <span class="date-text">今日概览</span>
      </div>

      <!-- Stats Cards -->
      <Row :gutter="16" class="stats-row">
        <Col :span="6">
          <Card :bordered="false">
            <Statistic
              title="总任务数"
              :value="summary?.task_count ?? 0"
            >
              <template #prefix>
                <ClockCircleOutlined />
              </template>
            </Statistic>
          </Card>
        </Col>
        <Col :span="6">
          <Card :bordered="false">
            <Statistic
              title="已完成"
              :value="(summary?.task_count ?? 0) - (summary?.pending_tasks ?? 0)"
              :value-style="{ color: '#52c41a' }"
            >
              <template #prefix>
                <CheckCircleOutlined />
              </template>
            </Statistic>
          </Card>
        </Col>
        <Col :span="6">
          <Card :bordered="false">
            <Statistic
              title="活跃项目"
              :value="summary?.project_count ?? 0"
            >
              <template #prefix>
                <FolderOutlined />
              </template>
            </Statistic>
          </Card>
        </Col>
        <Col :span="6">
          <Card :bordered="false">
            <Statistic
              title="任务完成率"
              :value="taskCompletionRate"
              suffix="%"
            >
              <template #prefix>
                <FileTextOutlined />
              </template>
            </Statistic>
          </Card>
        </Col>
      </Row>

      <!-- Recent Tasks & Notifications -->
      <Row :gutter="16" class="content-row">
        <Col :span="16">
          <Card title="最近任务" :bordered="false">
            <List
              v-for="task in recentTasks"
              :key="task.id"
              :data-source="[task]"
            >
              <template #renderItem="{ item }">
                <List.Item class="task-item" @click="router.push(`/tasks`)">
                  <div class="task-info">
                    <span class="task-title">{{ item.title }}</span>
                    <Tag :color="priorityColor(item.priority)">{{ priorityLabel(item.priority) }}</Tag>
                    <Tag :color="statusColor(item.status)">{{ statusLabel(item.status) }}</Tag>
                  </div>
                </List.Item>
              </template>
            </List>
            <div v-if="recentTasks.length === 0" class="empty-text">暂无任务</div>
          </Card>
        </Col>
        <Col :span="8">
          <Card title="通知" :bordered="false">
            <List
              v-for="notif in notifications"
              :key="notif.id"
              :data-source="[notif]"
            >
              <template #renderItem="{ item }">
                <List.Item class="notification-item">
                  <div>
                    <div class="notif-title">{{ item.title || '系统通知' }}</div>
                    <div class="notif-content">{{ item.content }}</div>
                  </div>
                </List.Item>
              </template>
            </List>
            <div v-if="notifications.length === 0" class="empty-text">暂无通知</div>
          </Card>
        </Col>
      </Row>

      <!-- Key Events Timeline -->
      <Card title="近期事件" :bordered="false" class="events-card">
        <Timeline>
          <Timeline.Item
            v-for="event in keyEvents"
            :key="event.id"
            :color="event.type === 'create' ? 'green' : event.type === 'update' ? 'blue' : 'gray'"
          >
            <div class="event-content">
              <span class="event-title">{{ event.title }}</span>
              <span class="event-time">{{ event.gmt_create }}</span>
            </div>
          </Timeline.Item>
        </Timeline>
        <div v-if="keyEvents.length === 0" class="empty-text">暂无事件</div>
      </Card>
    </Spin>
  </div>
</template>

<style scoped>
.dashboard-page {
  padding: 24px;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.dashboard-header h2 {
  margin: 0;
}

.date-text {
  color: var(--color-text-secondary, #666);
  font-size: 14px;
}

.stats-row {
  margin-bottom: 24px;
}

.content-row {
  margin-bottom: 24px;
}

.task-item {
  cursor: pointer;
}

.task-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.task-title {
  font-weight: 500;
}

.notification-item {
  padding: 8px 0;
}

.notif-title {
  font-weight: 500;
  font-size: 14px;
}

.notif-content {
  color: var(--color-text-secondary, #666);
  font-size: 12px;
  margin-top: 4px;
}

.events-card {
  margin-bottom: 24px;
}

.event-content {
  display: flex;
  justify-content: space-between;
}

.event-title {
  font-weight: 500;
}

.event-time {
  color: var(--color-text-secondary, #666);
  font-size: 12px;
}

.empty-text {
  text-align: center;
  color: var(--color-text-secondary, #666);
  padding: 24px;
}
</style>
