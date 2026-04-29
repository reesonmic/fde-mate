<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useUiStore } from '@/stores/ui'
import { Dropdown, Avatar, Button } from 'ant-design-vue'

const router = useRouter()
const authStore = useAuthStore()
const uiStore = useUiStore()

const userName = computed(() => authStore.user?.name || 'User')

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

const toggleCopilot = () => {
  uiStore.toggleCopilot()
}
</script>

<template>
  <header class="app-header">
    <div class="app-header-logo">
      <h1>FDE Workbench</h1>
    </div>

    <div class="app-header-center">
      <!-- Search placeholder -->
    </div>

    <div class="app-header-right">
      <!-- Copilot toggle -->
      <Button @click="toggleCopilot" :type="uiStore.copilotVisible ? 'primary' : 'default'">
        AI助手
      </Button>

      <!-- User dropdown -->
      <Dropdown>
        <div class="app-header-user">
          <Avatar :src="authStore.user?.avatar" :size="32">
            {{ userName.charAt(0) }}
          </Avatar>
          <span class="app-header-user-name">{{ userName }}</span>
        </div>
        <template #overlay>
          <div class="app-header-dropdown">
            <Button block @click="router.push('/settings')">设置</Button>
            <Button block @click="handleLogout">退出登录</Button>
          </div>
        </template>
      </Dropdown>
    </div>
  </header>
</template>

<style scoped>
.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  height: 60px;
}

.app-header-logo h1 {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
}

.app-header-center {
  flex: 1;
  display: flex;
  justify-content: center;
}

.app-header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.app-header-user {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.app-header-user-name {
  font-size: 14px;
}

.app-header-dropdown {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 8px;
  background: var(--color-bg-elevated);
  border-radius: 8px;
}
</style>