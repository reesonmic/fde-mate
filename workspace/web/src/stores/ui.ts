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
  interface UINotification {
    id: number
    title: string
    message?: string
    type?: 'info' | 'success' | 'warning' | 'error'
    timestamp?: number
  }

  const notifications = ref<UINotification[]>([])

  // Page context for copilot
  const pageContext = ref<Record<string, unknown>>({})

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

  const addNotification = (notification: Partial<UINotification> & { title: string }) => {
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

  const setPageContext = (context: Record<string, unknown>) => {
    pageContext.value = { ...pageContext.value, ...context }
  }

  const clearPageContext = () => {
    pageContext.value = {}
  }

  const copilotOpen = computed(() => copilotVisible.value)

  return {
    theme,
    sidebarCollapsed: sidebarCollapsed,
    copilotVisible,
    copilotOpen,
    globalLoading,
    notifications,
    pageContext,
    setTheme,
    toggleSidebar,
    setSidebarCollapsed,
    toggleCopilot,
    setCopilotVisible,
    setGlobalLoading,
    addNotification,
    removeNotification,
    clearNotifications,
    setPageContext,
    clearPageContext,
  }
})