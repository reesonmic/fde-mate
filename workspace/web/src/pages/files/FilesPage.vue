<script setup lang="ts">
import { ref, computed, onMounted, h } from 'vue'
import { Card, Button, Upload, Table, Tag, Modal, message, Spin, Popconfirm, Progress, Space, Input } from 'ant-design-vue'
import {
  UploadOutlined,
  DeleteOutlined,
  DownloadOutlined,
  FolderOutlined,
  FileOutlined,
  SearchOutlined,
} from '@ant-design/icons-vue'
import { filesApi } from '@apis/modules/files'

const loading = ref(false)
const fileList = ref<any[]>([])
const treeData = ref<any[]>([])
const quota = ref<any>(null)
const searchKeyword = ref('')
const selectedRowKeys = ref<number[]>([])

const quotaPercent = computed(() => {
  if (!quota.value) return 0
  return Math.round((quota.value.used_bytes / quota.value.total_bytes) * 100)
})

const quotaUsed = computed(() => {
  if (!quota.value) return '0 B'
  return formatBytes(quota.value.used_bytes)
})

const quotaTotal = computed(() => {
  if (!quota.value) return '0 B'
  return formatBytes(quota.value.total_bytes)
})

function formatBytes(bytes: number): string {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
}

const filteredFiles = computed(() => {
  if (!searchKeyword.value) return fileList.value
  const kw = searchKeyword.value.toLowerCase()
  return fileList.value.filter((f) => f.file_name?.toLowerCase().includes(kw))
})

const columns = [
  {
    title: '文件名',
    dataIndex: 'file_name',
    key: 'file_name',
    render: (text: string, record: any) => {
      const icon = record.scope === 'project' ? FolderOutlined : FileOutlined
      return h('span', { class: 'file-name-cell' }, [
        h(icon, { style: { marginRight: '8px', color: '#1677ff' } }),
        text,
      ])
    },
  },
  {
    title: '类型',
    dataIndex: 'file_type',
    key: 'file_type',
    width: 100,
    render: (t: string) => h(Tag, {}, () => t),
  },
  {
    title: '大小',
    dataIndex: 'file_size',
    key: 'file_size',
    width: 100,
    render: (s: number) => formatBytes(s),
  },
  {
    title: '范围',
    dataIndex: 'scope',
    key: 'scope',
    width: 80,
    render: (s: string) => {
      const labels: Record<string, string> = { project: '项目', customer: '客户', personal: '个人' }
      return h(Tag, { color: s === 'project' ? 'blue' : s === 'customer' ? 'green' : 'default' }, () => labels[s] || s)
    },
  },
  {
    title: '上传时间',
    dataIndex: 'created_at',
    key: 'created_at',
    width: 180,
  },
  {
    title: '操作',
    key: 'action',
    width: 120,
    render: (_: unknown, record: any) => h('div', { class: 'action-cell' }, [
      h(DownloadOutlined, {
        style: { marginRight: '8px', cursor: 'pointer' },
        onClick: () => handleDownload(record),
      }),
      h(Popconfirm, {
        title: '确定删除？',
        onConfirm: () => handleDelete(record.id),
      }, {
        default: () => h(DeleteOutlined, { style: { color: '#ff4d4f', cursor: 'pointer' } }),
      }),
    ]),
  },
]

const loadData = async () => {
  loading.value = true
  try {
    const [filesRes, treeRes, quotaRes] = await Promise.all([
      filesApi.list({}),
      filesApi.getTree(),
      filesApi.getQuota(),
    ])
    fileList.value = filesRes.items
    treeData.value = treeRes
    quota.value = quotaRes
  } catch (e) {
    console.error('Failed to load files', e)
  } finally {
    loading.value = false
  }
}

const handleDownload = async (file: any) => {
  try {
    const res = await filesApi.getDownloadUrl(file.id)
    window.open(res.url, '_blank')
  } catch {
    message.error('获取下载链接失败')
  }
}

const handleDelete = async (id: number) => {
  try {
    await filesApi.delete(id)
    message.success('删除成功')
    await loadData()
  } catch {
    message.error('删除失败')
  }
}

const handleBatchDelete = async () => {
  if (selectedRowKeys.value.length === 0) return
  try {
    await filesApi.batchDelete(selectedRowKeys.value)
    message.success(`已删除 ${selectedRowKeys.value.length} 个文件`)
    selectedRowKeys.value = []
    await loadData()
  } catch {
    message.error('批量删除失败')
  }
}

const customUpload = async (options: any) => {
  const { file, onSuccess, onError } = options
  try {
    // Step 1: Get upload token
    const tokenRes = await filesApi.getUploadToken({
      file_name: file.name,
      file_size: file.size,
    })

    // Step 2: Upload to OSS (mock - in production, upload directly to OSS endpoint)
    const formData = new FormData()
    formData.append('file', file)
    // In production: POST to tokenRes.endpoint with tokenRes.uploadToken

    // Step 3: Finalize upload
    await filesApi.finalizeUpload({
      ossKey: tokenRes.ossKey,
      file_name: file.name,
      file_size: file.size,
    })

    message.success(`${file.name} 上传成功`)
    onSuccess?.(null)
    await loadData()
  } catch (e: any) {
    message.error(`${file.name} 上传失败`)
    onError?.(e)
  }
}

onMounted(async () => {
  await loadData()
})
</script>

<template>
  <div class="files-page">
    <div class="page-header">
      <h2>文件中心</h2>
      <Upload
        :customRequest="customUpload"
        :showUploadList="false"
        :multiple="true"
      >
        <Button type="primary">
          <UploadOutlined />
          上传文件
        </Button>
      </Upload>
    </div>

    <!-- Quota -->
    <Card :bordered="false" class="quota-card">
      <div class="quota-info">
        <span>存储使用: {{ quotaUsed }} / {{ quotaTotal }}</span>
        <span>{{ quotaPercent }}%</span>
      </div>
      <Progress :percent="quotaPercent" :strokeColor="quotaPercent > 90 ? '#ff4d4f' : '#1677ff'" :showInfo="false" />
    </Card>

    <!-- Toolbar -->
    <div class="toolbar">
      <Input
        v-model:value="searchKeyword"
        placeholder="搜索文件..."
        class="search-input"
      >
        <template #prefix><SearchOutlined /></template>
      </Input>

      <Space v-if="selectedRowKeys.length > 0">
        <span>已选择 {{ selectedRowKeys.length }} 项</span>
        <Popconfirm title="确定删除选中的文件？" @confirm="handleBatchDelete">
          <Button danger>批量删除</Button>
        </Popconfirm>
      </Space>
    </div>

    <!-- File Table -->
    <Card :bordered="false">
      <Spin :spinning="loading">
        <Table
          :columns="columns"
          :data-source="filteredFiles"
          :row-selection="{
            selectedRowKeys: selectedRowKeys,
            onChange: (keys: any[]) => { selectedRowKeys = keys },
          }"
          row-key="id"
          :pagination="{ pageSize: 20 }"
        />
        <div v-if="filteredFiles.length === 0 && !loading" class="empty-text">
          暂无文件
        </div>
      </Spin>
    </Card>
  </div>
</template>

<style scoped>
.files-page {
  padding: 24px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.page-header h2 {
  margin: 0;
}

.quota-card {
  margin-bottom: 16px;
}

.quota-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 14px;
  color: var(--color-text-secondary, #666);
}

.toolbar {
  display: flex;
  gap: 12px;
  align-items: center;
  margin-bottom: 16px;
}

.search-input {
  width: 240px;
}

.file-name-cell {
  display: flex;
  align-items: center;
}

.action-cell {
  display: flex;
  gap: 8px;
}

.empty-text {
  text-align: center;
  color: var(--color-text-secondary, #666);
  padding: 48px;
}
</style>
