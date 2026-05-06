import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { TaskDTO } from '@/types/business'
import { tasksApi } from '@/apis/modules/tasks'

export const useTasksStore = defineStore('tasks', () => {
  const tasks = ref<TaskDTO[]>([])
  const kanbanData = ref<Record<string, TaskDTO[]>>({})
  const loading = ref(false)
  const error = ref<Error | null>(null)
  const total = ref(0)

  const totalTasks = computed(() => tasks.value.length)
  const completedTasks = computed(() =>
    tasks.value.filter((t) => t.status === 'done').length
  )

  const loadTasks = async (params?: Record<string, unknown>) => {
    loading.value = true
    error.value = null
    try {
      const response = await tasksApi.list(params || {})
      tasks.value = response.items
      total.value = response.total
    } catch (err) {
      error.value = err as Error
    } finally {
      loading.value = false
    }
  }

  const loadKanban = async (_projectId?: string) => {
    loading.value = true
    try {
      // Fetch all tasks and group by status for kanban view
      const response = await tasksApi.list({})
      const grouped: Record<string, TaskDTO[]> = {}
      response.items.forEach((task) => {
        const status = task.status || 'todo'
        if (!grouped[status]) grouped[status] = []
        grouped[status].push(task)
      })
      kanbanData.value = grouped
    } catch (err) {
      error.value = err as Error
    } finally {
      loading.value = false
    }
  }

  const createTask = async (data: Record<string, unknown>) => {
    const task = await tasksApi.create(data)
    tasks.value.push(task)
    return task
  }

  const updateTask = async (id: number, data: Partial<TaskDTO>) => {
    const task = await tasksApi.update(id, data)
    const index = tasks.value.findIndex((t) => t.id === id)
    if (index !== -1) {
      tasks.value[index] = task
    }
    return task
  }

  const deleteTask = async (id: number) => {
    await tasksApi.delete(id)
    tasks.value = tasks.value.filter((t) => t.id !== id)
  }

  return {
    tasks,
    kanbanData,
    loading,
    error,
    total,
    totalTasks,
    completedTasks,
    loadTasks,
    loadKanban,
    createTask,
    updateTask,
    deleteTask,
  }
})