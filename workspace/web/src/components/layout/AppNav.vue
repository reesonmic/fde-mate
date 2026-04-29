<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Menu } from 'ant-design-vue'
import {
  DashboardOutlined,
  ProjectOutlined,
  TeamOutlined,
  FileOutlined,
  BookOutlined,
  MessageOutlined,
  SettingOutlined,
} from '@ant-design/icons-vue'

const route = useRoute()
const router = useRouter()

const menuItems = [
  { key: '/dashboard', icon: DashboardOutlined, title: '仪表盘' },
  { key: '/tasks', icon: ProjectOutlined, title: '任务管理' },
  { key: '/projects', icon: ProjectOutlined, title: '项目空间' },
  { key: '/customers', icon: TeamOutlined, title: '客户空间' },
  { key: '/files', icon: FileOutlined, title: '文件中心' },
  { key: '/coach', icon: BookOutlined, title: 'FDE教练' },
  { key: '/chat', icon: MessageOutlined, title: 'AI对话中心' },
  { key: '/settings', icon: SettingOutlined, title: '系统设置' },
]

const selectedKey = computed(() => {
  // Match the closest route path
  for (const item of menuItems) {
    if (route.path.startsWith(item.key)) {
      return item.key
    }
  }
  return '/dashboard'
})

const handleMenuClick = ({ key }: { key: string }) => {
  router.push(key)
}
</script>

<template>
  <nav class="app-nav">
    <Menu
      mode="inline"
      :selectedKeys="[selectedKey]"
      @click="handleMenuClick"
      class="app-nav-menu"
    >
      <Menu.Item v-for="item in menuItems" :key="item.key">
        <component :is="item.icon" />
        <span>{{ item.title }}</span>
      </Menu.Item>
    </Menu>
  </nav>
</template>

<style scoped>
.app-nav {
  height: 100%;
  padding: 8px 0;
}

.app-nav-menu {
  border: none;
  background: transparent;
}
</style>