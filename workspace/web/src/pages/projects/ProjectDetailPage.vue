<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { Tabs, Card, Table, Button, Tag, Descriptions, Form, Input, Modal, DatePicker, message, Spin, Statistic, Row, Col, Progress, Timeline, Select } from 'ant-design-vue'
import { PlusOutlined, ArrowLeftOutlined } from '@ant-design/icons-vue'
import { useRoute, useRouter } from 'vue-router'
import { useProjectsStore } from '@/stores/projects'
import { projectsApi } from '@/apis/modules/projects'

const route = useRoute()
const router = useRouter()
const projectsStore = useProjectsStore()
const activeTab = ref('overview')
const loading = ref(false)
const project = ref<any>(null)
const health = ref<any>(null)
const members = ref<any[]>([])
const milestones = ref<any[]>([])
const risks = ref<any[]>([])
const weeklyReports = ref<any[]>([])

// Add member
const showAddMember = ref(false)
const addMemberForm = reactive({
  user_id: 0,
  role: 'member',
})

// Add milestone
const showAddMilestone = ref(false)
const addMilestoneForm = reactive({
  name: '',
  description: '',
  deadline: undefined as any,
})

// Add risk
const showAddRisk = ref(false)
const addRiskForm = reactive({
  title: '',
  description: '',
  level: 'medium',
})

const projectId = computed(() => Number(route.params.id))

const healthLevel = computed(() => {
  if (!health.value) return 'unknown'
  const score = health.value.health ?? 100
  if (score >= 80) return 'good'
  if (score >= 60) return 'warning'
  return 'danger'
})

const healthColor = computed(() => {
  const map: Record<string, string> = {
    good: '#52c41a',
    warning: '#faad14',
    danger: '#ff4d4f',
  }
  return map[healthLevel.value] || '#d9d9d9'
})

const healthLabel = computed(() => {
  const map: Record<string, string> = {
    good: '健康',
    warning: '警告',
    danger: '危险',
  }
  return map[healthLevel.value] || '未知'
})

const riskLevelColor = (level: string) => {
  const map: Record<string, string> = {
    low: 'blue',
    medium: 'orange',
    high: 'red',
  }
  return map[level] || 'default'
}

const riskLevelLabel = (level: string) => {
  const map: Record<string, string> = {
    low: '低',
    medium: '中',
    high: '高',
  }
  return map[level] || level
}

const milestoneStatusColor = (status: string) => {
  const map: Record<string, string> = {
    pending: 'default',
    in_progress: 'processing',
    completed: 'success',
  }
  return map[status] || 'default'
}

const milestoneStatusLabel = (status: string) => {
  const map: Record<string, string> = {
    pending: '未开始',
    in_progress: '进行中',
    completed: '已完成',
  }
  return map[status] || status
}

const loadData = async () => {
  loading.value = true
  const id = projectId.value
  try {
    const [proj, healthRes, membersRes, risksRes, reportsRes] = await Promise.all([
      projectsApi.get(id),
      projectsApi.getHealth(id),
      projectsApi.getMembers(id),
      projectsApi.list ? Promise.resolve([]) : Promise.resolve([]),
      projectsApi.weeklyReports(id),
    ])
    project.value = proj
    health.value = healthRes
    members.value = membersRes
    risks.value = (proj as any).risks || []
    weeklyReports.value = reportsRes
    milestones.value = (proj as any).milestones || []
  } catch (e) {
    console.error('Failed to load project data', e)
  } finally {
    loading.value = false
  }
}

const handleAddMember = async () => {
  if (!addMemberForm.user_id) {
    message.warning('请输入用户ID')
    return
  }
  try {
    await projectsApi.addMember(projectId.value, {
      userId: addMemberForm.user_id,
      role: addMemberForm.role,
    })
    message.success('添加成功')
    showAddMember.value = false
    await loadData()
  } catch {
    message.error('添加失败')
  }
}

const handleRemoveMember = async (userId: number) => {
  try {
    await projectsApi.removeMember(projectId.value, userId)
    message.success('移除成功')
    await loadData()
  } catch {
    message.error('移除失败')
  }
}

const handleAddMilestone = async () => {
  if (!addMilestoneForm.name) {
    message.warning('请输入里程碑名称')
    return
  }
  message.info('里程碑功能开发中')
  showAddMilestone.value = false
}

const handleAddRisk = async () => {
  if (!addRiskForm.title) {
    message.warning('请输入风险标题')
    return
  }
  try {
    await projectsApi.addRisk(projectId.value, {
      title: addRiskForm.title,
      description: addRiskForm.description,
      level: addRiskForm.level,
    })
    message.success('添加成功')
    showAddRisk.value = false
    Object.assign(addRiskForm, { title: '', description: '', level: 'medium' })
    await loadData()
  } catch {
    message.error('添加失败')
  }
}

const memberColumns = [
  { title: '用户ID', dataIndex: 'user_id', key: 'user_id' },
  { title: '角色', dataIndex: 'role', key: 'role' },
  { title: '加入时间', dataIndex: 'joined_at', key: 'joined_at' },
  {
    title: '操作',
    key: 'action',
    render: (_: unknown, record: any) => (
      <Button type="link" danger size="small" onClick={() => handleRemoveMember(record.user_id)}>
        移除
      </Button>
    ),
  },
]

const milestoneColumns = [
  { title: '名称', dataIndex: 'name', key: 'name' },
  {
    title: '状态',
    dataIndex: 'status',
    key: 'status',
    render: (s: string) => <Tag color={milestoneStatusColor(s)}>{milestoneStatusLabel(s)}</Tag>,
  },
  { title: '截止日期', dataIndex: 'deadline', key: 'deadline' },
]

const riskColumns = [
  { title: '标题', dataIndex: 'title', key: 'title' },
  {
    title: '等级',
    dataIndex: 'level',
    key: 'level',
    render: (l: string) => <Tag color={riskLevelColor(l)}>{riskLevelLabel(l)}</Tag>,
  },
  { title: '描述', dataIndex: 'description', key: 'description' },
  { title: '创建时间', dataIndex: 'created_at', key: 'created_at' },
]

onMounted(async () => {
  await loadData()
})
</script>

<template>
  <div class="project-detail-page">
    <Spin :spinning="loading">
      <!-- Header -->
      <div class="detail-header">
        <Button type="text" @click="router.push('/projects')">
          <ArrowLeftOutlined />
          返回列表
        </Button>
        <div class="project-title-area">
          <h2>{{ project?.name || '项目详情' }}</h2>
          <p>{{ project?.description }}</p>
        </div>
        <div class="health-badge" v-if="health">
          <Statistic
            title="健康度"
            :value="health.health ?? 100"
            suffix="%"
            :value-style="{ color: healthColor }"
          />
          <Tag :color="healthColor">{{ healthLabel }}</Tag>
        </div>
      </div>

      <!-- Tabs -->
      <Tabs v-model:activeKey="activeTab">
        <Tabs.TabPane key="overview" tab="概览">
          <Row :gutter="16">
            <Col :span="16">
              <Card title="项目信息" :bordered="false">
                <Descriptions :column="2">
                  <Descriptions.Item label="状态">
                    <Tag>{{ project?.status }}</Tag>
                  </Descriptions.Item>
                  <Descriptions.Item label="进度">
                    <Progress :percent="project?.progress ?? 0" />
                  </Descriptions.Item>
                  <Descriptions.Item label="开始日期">{{ project?.start_date || '-' }}</Descriptions.Item>
                  <Descriptions.Item label="结束日期">{{ project?.end_date || '-' }}</Descriptions.Item>
                  <Descriptions.Item label="创建时间">{{ project?.created_at || '-' }}</Descriptions.Item>
                  <Descriptions.Item label="更新时间">{{ project?.updated_at || '-' }}</Descriptions.Item>
                </Descriptions>
              </Card>
            </Col>
            <Col :span="8">
              <Card title="风险概览" :bordered="false">
                <div v-if="risks.length === 0" class="empty-text">暂无风险</div>
                <div v-for="risk in risks" :key="risk.id" class="risk-item">
                  <Tag :color="riskLevelColor(risk.level)">{{ riskLevelLabel(risk.level) }}</Tag>
                  <span>{{ risk.title }}</span>
                </div>
              </Card>
            </Col>
          </Row>
        </Tabs.TabPane>

        <Tabs.TabPane key="members" tab="成员">
          <Card :bordered="false">
            <template #extra>
              <Button type="primary" size="small" @click="showAddMember = true">
                <PlusOutlined /> 添加成员
              </Button>
            </template>
            <Table
              :columns="memberColumns"
              :data-source="members"
              :pagination="false"
              row-key="user_id"
            />
          </Card>
        </Tabs.TabPane>

        <Tabs.TabPane key="milestones" tab="里程碑">
          <Card :bordered="false">
            <template #extra>
              <Button type="primary" size="small" @click="showAddMilestone = true">
                <PlusOutlined /> 添加里程碑
              </Button>
            </template>
            <Table
              :columns="milestoneColumns"
              :data-source="milestones"
              :pagination="false"
              row-key="id"
            />
            <div v-if="milestones.length === 0" class="empty-text">暂无里程碑</div>
          </Card>
        </Tabs.TabPane>

        <Tabs.TabPane key="risks" tab="风险">
          <Card :bordered="false">
            <template #extra>
              <Button type="primary" size="small" @click="showAddRisk = true">
                <PlusOutlined /> 添加风险
              </Button>
            </template>
            <Table
              :columns="riskColumns"
              :data-source="risks"
              :pagination="false"
              row-key="id"
            />
            <div v-if="risks.length === 0" class="empty-text">暂无风险</div>
          </Card>
        </Tabs.TabPane>

        <Tabs.TabPane key="tasks" tab="关联任务">
          <Card :bordered="false">
            <div class="empty-text">任务列表开发中...</div>
          </Card>
        </Tabs.TabPane>

        <Tabs.TabPane key="reports" tab="周报">
          <Card :bordered="false">
            <template #extra>
              <Button type="primary" size="small" @click="projectsApi.generateWeeklyReport(projectId.value).then(() => { message.success('已生成'); loadData() })">
                生成周报
              </Button>
            </template>
            <Timeline>
              <Timeline.Item v-for="report in weeklyReports" :key="report.id">
                <div class="report-item">
                  <h4>{{ report.title || '周报' }}</h4>
                  <p>{{ report.content || report.created_at }}</p>
                </div>
              </Timeline.Item>
            </Timeline>
            <div v-if="weeklyReports.length === 0" class="empty-text">暂无周报</div>
          </Card>
        </Tabs.TabPane>

        <Tabs.TabPane key="files" tab="文件">
          <Card :bordered="false">
            <div class="empty-text">文件管理开发中...</div>
          </Card>
        </Tabs.TabPane>
      </Tabs>
    </Spin>

    <!-- Add Member Modal -->
    <Modal v-model:visible="showAddMember" title="添加成员" @ok="handleAddMember">
      <Form :label-col="{ span: 6 }">
        <Form.Item label="用户ID">
          <Input v-model:value="addMemberForm.user_id" type="number" placeholder="输入用户ID" />
        </Form.Item>
        <Form.Item label="角色">
          <Select v-model:value="addMemberForm.role" style="width: 100%">
            <Select.Option value="admin">管理员</Select.Option>
            <Select.Option value="member">成员</Select.Option>
            <Select.Option value="viewer">观察者</Select.Option>
          </Select>
        </Form.Item>
      </Form>
    </Modal>

    <!-- Add Milestone Modal -->
    <Modal v-model:visible="showAddMilestone" title="添加里程碑" @ok="handleAddMilestone">
      <Form :label-col="{ span: 6 }">
        <Form.Item label="名称" required>
          <Input v-model:value="addMilestoneForm.name" placeholder="输入里程碑名称" />
        </Form.Item>
        <Form.Item label="描述">
          <Input.TextArea v-model:value="addMilestoneForm.description" :rows="2" />
        </Form.Item>
        <Form.Item label="截止日期">
          <DatePicker v-model:value="addMilestoneForm.deadline" style="width: 100%" />
        </Form.Item>
      </Form>
    </Modal>

    <!-- Add Risk Modal -->
    <Modal v-model:visible="showAddRisk" title="添加风险" @ok="handleAddRisk">
      <Form :label-col="{ span: 6 }">
        <Form.Item label="标题" required>
          <Input v-model:value="addRiskForm.title" placeholder="输入风险标题" />
        </Form.Item>
        <Form.Item label="描述">
          <Input.TextArea v-model:value="addRiskForm.description" :rows="2" />
        </Form.Item>
        <Form.Item label="等级">
          <Select v-model:value="addRiskForm.level" style="width: 100%">
            <Select.Option value="low">低</Select.Option>
            <Select.Option value="medium">中</Select.Option>
            <Select.Option value="high">高</Select.Option>
          </Select>
        </Form.Item>
      </Form>
    </Modal>
  </div>
</template>

<style scoped>
.project-detail-page {
  padding: 24px;
}

.detail-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.project-title-area {
  flex: 1;
}

.project-title-area h2 {
  margin: 0 0 4px;
}

.project-title-area p {
  margin: 0;
  color: var(--color-text-secondary, #666);
}

.health-badge {
  text-align: right;
}

.risk-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 0;
}

.report-item h4 {
  margin: 0 0 4px;
}

.report-item p {
  margin: 0;
  color: var(--color-text-secondary, #666);
  font-size: 13px;
}

.empty-text {
  text-align: center;
  color: var(--color-text-secondary, #666);
  padding: 24px;
}
</style>
