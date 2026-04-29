import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useUiStore = defineStore('ui', () => {
  // Theme
  const theme = ref<'light' | 'dark'>('light')

  // Sidebar state
  const sidebarCollapsed = ref(false)

  // Copilot panel visibility
  const copilotVisible = ref(true)

  // Loading states
  const globalLoading = ref(false)

  // Notifications
  const notifications = ref<any[]>([])

  const setTheme = (newTheme: 'light' | 'dark') => {
    theme.value = newTheme
  }

  const toggleSidebar = () => {
    sidebarCollapsed.value = !sidebarCollapsed.value
  }

  const setSidebarCollapsed = (collapsed: boolean) => {
    sidebarCollapsed.value = collapsed
  }

  const toggleCopilot = () => {
    copilotVisible.value = !copilotVisible.value
  }

  const setCopilotVisible = (visible: boolean) => {
    copilotVisible.value = visible
  }

  const setGlobalLoading = (loading: boolean) => {
    globalLoading.value = loading
  }

  const addNotification = (notification: any) => {
    notifications.value.push({
      id: Date.now(),
      ...notification,
    })
  }

  const removeNotification = (id: number) => {
    notifications.value = notifications.value.filter((n) => n.id !== id)
  }

  const clearNotifications = () => {
    notifications.value = []
  }

  const copilotOpen = computed(() => copilotVisible.value)

  return {
    theme,
    sidebarCollapsed: sidebarCollapsed,
    copilotVisible,
    copilotOpen,
    globalLoading,
    notifications,
    setTheme,
    toggleSidebar,
    setSidebarCollapsed,
    toggleCopilot,
    setCopilotVisible,
    setGlobalLoading,
    addNotification,
    removeNotification,
    clearNotifications,
  }
})