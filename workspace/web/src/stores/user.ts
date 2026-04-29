import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUserStore = defineStore('user', () => {
  const preferences = ref({
    language: 'zh-CN',
    timezone: 'Asia/Shanghai',
    dateFormat: 'YYYY-MM-DD',
    notifications: {
      email: true,
      sms: false,
      push: true,
    },
  })

  const settings = ref({
    theme: 'light',
    sidebarCollapsed: false,
    copilotVisible: true,
  })

  const updatePreferences = (newPreferences: Partial<typeof preferences.value>) => {
    preferences.value = { ...preferences.value, ...newPreferences }
  }

  const updateSettings = (newSettings: Partial<typeof settings.value>) => {
    settings.value = { ...settings.value, ...newSettings }
  }

  return {
    preferences,
    settings,
    updatePreferences,
    updateSettings,
  }
})