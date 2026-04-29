import { ref, watch } from 'vue'
import { useUiStore } from '@/stores/ui'

/**
 * Theme composable for managing UI theme
 */
export function useTheme() {
  const uiStore = useUiStore()

  const theme = ref<'light' | 'dark'>(uiStore.theme)

  watch(
    () => uiStore.theme,
    (newTheme) => {
      theme.value = newTheme
      applyTheme(newTheme)
    }
  )

  const applyTheme = (theme: 'light' | 'dark') => {
    document.documentElement.setAttribute('data-theme', theme)
    // Store in localStorage for persistence
    localStorage.setItem('theme', theme)
  }

  const setTheme = (newTheme: 'light' | 'dark') => {
    uiStore.setTheme(newTheme)
    applyTheme(newTheme)
  }

  const toggleTheme = () => {
    const newTheme = theme.value === 'light' ? 'dark' : 'light'
    setTheme(newTheme)
  }

  // Apply initial theme
  const initTheme = () => {
    const stored = localStorage.getItem('theme') as 'light' | 'dark' | null
    const initialTheme = stored || 'light'
    setTheme(initialTheme)
  }

  return {
    theme,
    setTheme,
    toggleTheme,
    initTheme,
  }
}