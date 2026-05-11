<script setup lang="ts">
import { ref, reactive, onMounted, computed, h } from 'vue'
import { Tabs, Card, Table, Button, Tag, Descriptions, Form, Input, Modal, DatePicker, message, Spin, Statistic, Row, Col, Progress, Timeline, Select } from 'ant-design-vue'
import { PlusOutlined, ArrowLeftOutlined, EditOutlined } from '@ant-design/icons-vue'
import { useRoute, useRouter } from 'vue-router'
import { useProjectsStore } from '@/stores/projects'
import { projectsApi } from '@/apis/modules/projects'
import type { ProjectDTO, ProjectMemberDTO, ProjectMilestoneDTO, WeeklyReportDTO } from '@/types/business'
import dayjs from 'dayjs'

const route = useRoute()
const router = useRouter()
const projectsStore = useProjectsStore()
const activeTab = ref('overview')
const loading = ref(false)
const project = ref<ProjectDTO | null>(null)
const health = ref<{ health: number; risk_count: number; overdue_milestones: number } | null>(null)
const members = ref<ProjectMemberDTO[]>([])
const milestones = ref<ProjectMilestoneDTO[]>([])
const risks = ref<Array<{ id: number; title: string; level: string; mitigation: string; status: string }>>([])
const weeklyReports = ref<WeeklyReportDTO[]>([])

// Edit project
const showEditProject = ref(false)
const savingProject = ref(false) // 防止重复提交
const editForm = reactive({
  name: '',
  phase: '',
  start_at: undefined as dayjs.Dayjs | undefined, // 统一使用 dayjs 类型
  end_at: undefined as dayjs.Dayjs | undefined,
})

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
  deadline: undefined as dayjs.Dayjs | undefined,
})

// Add risk
const showAddRisk = ref(false)
const addRiskForm = reactive({
  title: '',
  description: '',
  level: 'medium',
})

const projectId = computed(() => Number(route.params.id))

const handleGenerateReport = async () => {
  try {
    await projectsApi.generateWeeklyReport(projectId.value)
    message.success('已生成')
    await loadData()
  } catch {
    message.error('生成失败')
  }
}

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


const loadData = async () => {
  loading.value = true
  const id = projectId.value
  try {
    const [proj, healthRes, membersRes, risksRes, reportsRes] = await Promise.all([
      projectsApi.get(id),
      projectsApi.getHealth(id),
      projectsApi.getMembers(id),
      projectsApi.listRisks?.(id) || Promise.resolve([]),
      projectsApi.weeklyReports(id),
    ])
    project.value = proj
    health.value = healthRes
    members.value = membersRes
    risks.value = (proj as { risks?: typeof risks.value }).risks || []
    weeklyReports.value = reportsRes
    milestones.value = (proj as { milestones?: typeof milestones.value }).milestones || []
  } catch (e) {
    console.error('Failed to load project data', e)
  } finally {
    loading.value = false
  }
}

const handleEditProject = () => {
  if (!project.value) return
  
  // 填充表单数据
  editForm.name = project.value.name
  editForm.phase = project.value.phase
  // 将字符串转换为 dayjs 对象
  editForm.start_at = project.value.start_at ? dayjs(project.value.start_at) : undefined
  editForm.end_at = project.value.end_at ? dayjs(project.value.end_at) : undefined
  
  showEditProject.value = true
}

const handleSaveProject = async () => {
  // 表单验证
  if (!editForm.name.trim()) {
    message.warning('请输入项目名称')
    return
  }
  
  // 防止重复提交
  if (savingProject.value) return
  
  // 日期合法性校验
  if (editForm.start_at && editForm.end_at) {
    if (editForm.end_at.isBefore(editForm.start_at)) {
      message.warning('结束日期不能早于开始日期')
      return
    }
  }
  
  savingProject.value = true
  try {
    await projectsApi.update(projectId.value, {
      name: editForm.name,
      startDate: editForm.start_at?.format('YYYY-MM-DD'),
      endDate: editForm.end_at?.format('YYYY-MM-DD'),
    })
    message.success('项目信息已更新')
    showEditProject.value = false
    resetEditForm()
    await loadData()
  } catch (e) {
    console.error('更新失败', e)
    message.error('更新失败')
  } finally {
    savingProject.value = false
  }
}

const resetEditForm = () => {
  editForm.name = ''
  editForm.phase = ''
  editForm.start_at = undefined
  editForm.end_at = undefined
}

const handleCancelEdit = () => {
  resetEditForm()
  showEditProject.value = false
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
      mitigation: addRiskForm.description,
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
  { title: '用户名', dataIndex: 'user_name', key: 'user_name' },
  { title: '角色', dataIndex: 'role', key: 'role' },
  {
    title: '操作',
    key: 'action',
    render: (_: unknown, record: ProjectMemberDTO) =>
      h(Button, { type: 'link', danger: true, size: 'small', onClick: () => handleRemoveMember(record.user_id) }, () => '移除'),
  },
]

const milestoneColumns = [
  { title: '名称', dataIndex: 'title', key: 'title' },
  {
    title: '状态',
    dataIndex: 'done',
    key: 'done',
    render: (done: boolean) =>
      h(Tag, { color: done ? 'success' : 'default' }, () => done ? '已完成' : '未完成'),
  },
  { title: '截止日期', dataIndex: 'dueAt', key: 'dueAt' },
]

const riskColumns = [
  { title: '标题', dataIndex: 'title', key: 'title' },
  {
    title: '等级',
    dataIndex: 'level',
    key: 'level',
    render: (l: string) =>
      h(Tag, { color: riskLevelColor(l) }, () => riskLevelLabel(l)),
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
          <p>阶段: {{ project?.phase }} | 负责人: {{ project?.owner_name || '-' }}</p>
        </div>
        <Button type="primary" @click="handleEditProject">
          <EditOutlined />
          编辑项目
        </Button>
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
                  <Descriptions.Item label="阶段">
                    <Tag>{{ project?.phase }}</Tag>
                  </Descriptions.Item>
                  <Descriptions.Item label="健康度">
                    {{ project?.health }}%
                  </Descriptions.Item>
                  <Descriptions.Item label="开始日期">{{ project?.start_at?.substring(0, 10) || '-' }}</Descriptions.Item>
                  <Descriptions.Item label="结束日期">{{ project?.end_at?.substring(0, 10) || '-' }}</Descriptions.Item>
                  <Descriptions.Item label="创建时间">{{ project?.gmtCreate?.substring(0, 19) || '-' }}</Descriptions.Item>
                  <Descriptions.Item label="更新时间">{{ project?.gmtModified?.substring(0, 19) || '-' }}</Descriptions.Item>
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
              <Button type="primary" size="small" @click="handleGenerateReport">
                生成周报
              </Button>
            </template>
            <Timeline>
              <Timeline.Item v-for="report in weeklyReports" :key="report.id">
                <div class="report-item">
                  <h4>周报 {{ report.week_start?.substring(0, 10) }} ~ {{ report.week_end?.substring(0, 10) }}</h4>
                  <p>{{ report.content }}</p>
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

    <!-- Edit Project Modal -->
    <Modal 
      v-model:visible="showEditProject" 
      title="编辑项目" 
      @ok="handleSaveProject"
      @cancel="handleCancelEdit"
      :confirmLoading="savingProject"
      ok-text="保存"
      cancel-text="取消"
      width="600px"
    >
      <Form :label-col="{ span: 6 }" :wrapper-col="{ span: 16 }">
        <Form.Item label="项目名称" required>
          <Input v-model:value="editForm.name" placeholder="输入项目名称" />
        </Form.Item>
        <Form.Item label="项目阶段">
          <!-- phase 字段仅用于展示，不参与提交（后端不允许修改阶段） -->
          <span>{{ editForm.phase }}</span>
        </Form.Item>
        <Form.Item label="开始日期">
          <DatePicker 
            v-model:value="editForm.start_at" 
            style="width: 100%"
            placeholder="选择开始日期" 
          />
        </Form.Item>
        <Form.Item label="结束日期">
          <DatePicker 
            v-model:value="editForm.end_at" 
            style="width: 100%"
            :disabled-date="(current: dayjs.Dayjs) => {
              if (!editForm.start_at || !current) return false
              return current.isBefore(editForm.start_at, 'day')
            }"
            placeholder="选择结束日期" 
          />
        </Form.Item>
      </Form>
    </Modal>

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
