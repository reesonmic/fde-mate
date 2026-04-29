<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Card, Row, Col, Button, Input, Select, Tabs, Modal, Form, message, Tag, Avatar, Spin, Descriptions } from 'ant-design-vue'
import { PlusOutlined, SearchOutlined } from '@ant-design/icons-vue'
import { customersApi } from '@apis/modules/customers'
import CustomerCard from '@/components/business/CustomerCard.vue'

const loading = ref(false)
const customers = ref<any[]>([])
const searchKeyword = ref('')
const statusFilter = ref<string[]>([])
const activeTab = ref('all')
const showCreateModal = ref(false)
const createLoading = ref(false)

const createForm = ref({
  name: '',
  description: '',
  industry: '',
  contact_name: '',
  contact_email: '',
})

const selectedCustomer = ref<any>(null)
const customerDetail = ref<any>(null)
const contacts = ref<any[]>([])
const opportunities = ref<any[]>([])

const statusOptions = [
  { label: '活跃', value: 'active' },
  { label: '未活跃', value: 'inactive' },
  { label: '流失', value: 'churned' },
]

const statusColor = (status: string) => {
  const map: Record<string, string> = {
    active: 'success',
    inactive: 'default',
    churned: 'error',
  }
  return map[status] || 'default'
}

const statusLabel = (status: string) => {
  const map: Record<string, string> = {
    active: '活跃',
    inactive: '未活跃',
    churned: '流失',
  }
  return map[status] || status
}

const healthColor = (score: number) => {
  if (score >= 80) return '#52c41a'
  if (score >= 60) return '#faad14'
  return '#ff4d4f'
}

const filteredCustomers = computed(() => {
  let items = customers.value

  if (searchKeyword.value) {
    const kw = searchKeyword.value.toLowerCase()
    items = items.filter((c) => c.name.toLowerCase().includes(kw))
  }

  if (statusFilter.value.length > 0) {
    items = items.filter((c) => statusFilter.value.includes(c.status))
  }

  if (activeTab.value !== 'all') {
    items = items.filter((c) => c.status === activeTab.value)
  }

  return items
})

const loadData = async () => {
  loading.value = true
  try {
    const res = await customersApi.list({})
    customers.value = res.items
  } catch (e) {
    console.error('Failed to load customers', e)
  } finally {
    loading.value = false
  }
}

const handleSelectCustomer = async (customer: any) => {
  selectedCustomer.value = customer
  try {
    const [detail, contactsRes, opportunitiesRes] = await Promise.all([
      customersApi.get(Number(customer.id)),
      customersApi.listContacts(Number(customer.id)),
      customersApi.listOpportunities(Number(customer.id)),
    ])
    customerDetail.value = detail
    contacts.value = contactsRes.items || []
    opportunities.value = opportunitiesRes.items || []
  } catch (e) {
    console.error('Failed to load customer details', e)
  }
}

const handleCreate = async () => {
  if (!createForm.value.name.trim()) {
    message.warning('请输入客户名称')
    return
  }
  createLoading.value = true
  try {
    await customersApi.create(createForm.value)
    message.success('创建成功')
    showCreateModal.value = false
    createForm.value = { name: '', description: '', industry: '', contact_name: '', contact_email: '' }
    await loadData()
  } catch {
    message.error('创建失败')
  } finally {
    createLoading.value = false
  }
}

const handleDelete = async (id: number) => {
  Modal.confirm({
    title: '确认删除',
    content: '确定要删除此客户吗？',
    okText: '删除',
    okType: 'danger',
    cancelText: '取消',
    onOk: async () => {
      try {
        await customersApi.delete(id)
        message.success('删除成功')
        selectedCustomer.value = null
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
  <div class="customers-page">
    <div class="page-header">
      <h2>客户空间</h2>
      <Button type="primary" @click="showCreateModal = true">
        <PlusOutlined />
        新建客户
      </Button>
    </div>

    <div class="filters-bar">
      <Input
        v-model:value="searchKeyword"
        placeholder="搜索客户..."
        class="search-input"
      >
        <template #prefix><SearchOutlined /></template>
      </Input>

      <Select
        v-model:value="statusFilter"
        mode="multiple"
        placeholder="状态筛选"
        class="filter-select"
        allow-clear
      >
        <Select.Option v-for="opt in statusOptions" :key="opt.value" :value="opt.value">
          {{ opt.label }}
        </Select.Option>
      </Select>
    </div>

    <!-- Dual-pane layout -->
    <Row :gutter="16">
      <!-- Left: Customer list -->
      <Col :span="selectedCustomer ? 8 : 24">
        <Tabs v-model:activeKey="activeTab">
          <Tabs.TabPane key="all" tab="全部" />
          <Tabs.TabPane key="active" tab="活跃" />
          <Tabs.TabPane key="inactive" tab="未活跃" />
          <Tabs.TabPane key="churned" tab="流失" />
        </Tabs>

        <Spin :spinning="loading">
          <Row :gutter="[12, 12]">
            <Col
              v-for="customer in filteredCustomers"
              :key="customer.id"
              :span="selectedCustomer ? 24 : 6"
            >
              <CustomerCard
                :customer="customer"
                :selected="selectedCustomer?.id === customer.id"
                @click="handleSelectCustomer(customer)"
              />
            </Col>
          </Row>
          <div v-if="filteredCustomers.length === 0 && !loading" class="empty-text">
            暂无客户数据
          </div>
        </Spin>
      </Col>

      <!-- Right: Customer detail -->
      <Col v-if="selectedCustomer" :span="16">
        <Card class="detail-panel">
          <template #title>
            <div class="detail-header">
              <Avatar :size="48">{{ selectedCustomer.name?.[0] }}</Avatar>
              <div class="detail-title-text">
                <h3>{{ selectedCustomer.name }}</h3>
                <Tag :color="statusColor(selectedCustomer.status)">
                  {{ statusLabel(selectedCustomer.status) }}
                </Tag>
                <span v-if="selectedCustomer.health_score" class="health-score">
                  健康度: <span :style="{ color: healthColor(selectedCustomer.health_score) }">
                    {{ selectedCustomer.health_score }}
                  </span>
                </span>
              </div>
              <Button type="link" danger @click="handleDelete(Number(selectedCustomer.id))">
                删除
              </Button>
            </div>
          </template>

          <Descriptions :column="2" size="small">
            <Descriptions.Item label="描述">{{ selectedCustomer.description || '-' }}</Descriptions.Item>
            <Descriptions.Item label="行业">{{ selectedCustomer.industry || '-' }}</Descriptions.Item>
            <Descriptions.Item label="创建时间">{{ selectedCustomer.created_at || '-' }}</Descriptions.Item>
            <Descriptions.Item label="更新时间">{{ selectedCustomer.updated_at || '-' }}</Descriptions.Item>
          </Descriptions>

          <Tabs class="detail-tabs" type="card">
            <Tabs.TabPane key="contacts" :tab="`联系人 (${contacts.length})`">
              <div v-for="contact in contacts" :key="contact.id" class="contact-item">
                <Avatar>{{ contact.name?.[0] }}</Avatar>
                <div class="contact-info">
                  <div class="contact-name">{{ contact.name }}</div>
                  <div class="contact-email">{{ contact.email }}</div>
                </div>
              </div>
              <div v-if="contacts.length === 0" class="empty-text">暂无联系人</div>
            </Tabs.TabPane>

            <Tabs.TabPane key="opportunities" :tab="`商机 (${opportunities.length})`">
              <div v-for="opp in opportunities" :key="opp.id" class="opportunity-item">
                <div class="opp-name">{{ opp.name }}</div>
                <Tag>{{ opp.stage }}</Tag>
                <span class="opp-amount">{{ opp.amount }}</span>
              </div>
              <div v-if="opportunities.length === 0" class="empty-text">暂无商机</div>
            </Tabs.TabPane>
          </Tabs>
        </Card>
      </Col>
    </Row>

    <!-- Create Modal -->
    <Modal
      v-model:visible="showCreateModal"
      title="新建客户"
      @ok="handleCreate"
      :confirmLoading="createLoading"
    >
      <Form :label-col="{ span: 6 }" :wrapper-col="{ span: 18 }">
        <Form.Item label="名称" required>
          <Input v-model:value="createForm.name" placeholder="输入客户名称" />
        </Form.Item>
        <Form.Item label="描述">
          <Input.TextArea v-model:value="createForm.description" :rows="2" />
        </Form.Item>
        <Form.Item label="行业">
          <Input v-model:value="createForm.industry" placeholder="输入行业" />
        </Form.Item>
      </Form>
    </Modal>
  </div>
</template>

<style scoped>
.customers-page {
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
  width: 160px;
}

.detail-panel {
  position: sticky;
  top: 0;
}

.detail-header {
  display: flex;
  align-items: center;
  gap: 16px;
}

.detail-title-text h3 {
  margin: 0 0 4px;
}

.health-score {
  margin-left: 12px;
  font-size: 14px;
}

.detail-tabs {
  margin-top: 16px;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}

.contact-info {
  flex: 1;
}

.contact-name {
  font-weight: 500;
}

.contact-email {
  color: var(--color-text-secondary, #666);
  font-size: 13px;
}

.opportunity-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}

.opp-name {
  font-weight: 500;
  flex: 1;
}

.opp-amount {
  font-weight: 600;
  color: #1677ff;
}

.empty-text {
  text-align: center;
  color: var(--color-text-secondary, #666);
  padding: 24px;
}
</style>
