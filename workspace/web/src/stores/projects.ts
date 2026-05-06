import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { ProjectDTO, ProjectMemberDTO, ProjectMilestoneDTO } from '@/types/business'
import { projectsApi } from '@/apis/modules/projects'

export const useProjectsStore = defineStore('projects', () => {
  const projects = ref<ProjectDTO[]>([])
  const currentProject = ref<ProjectDTO | null>(null)
  const members = ref<ProjectMemberDTO[]>([])
  const milestones = ref<ProjectMilestoneDTO[]>([])
  const loading = ref(false)
  const error = ref<Error | null>(null)

  const activeProjects = computed(() =>
    projects.value.filter((p) => p.phase === 'delivery' || p.phase === 'discovery')
  )

  const loadProjects = async (params?: Record<string, unknown>) => {
    loading.value = true
    error.value = null
    try {
      const response = await projectsApi.list(params || {})
      projects.value = response.items
    } catch (err) {
      error.value = err as Error
    } finally {
      loading.value = false
    }
  }

  const loadProject = async (id: number) => {
    loading.value = true
    try {
      currentProject.value = await projectsApi.get(id)
    } catch (err) {
      error.value = err as Error
    } finally {
      loading.value = false
    }
  }

  const loadMembers = async (projectId: number) => {
    try {
      members.value = await projectsApi.getMembers(projectId)
    } catch (err) {
      error.value = err as Error
    }
  }

  const loadMilestones = async (projectId: number) => {
    // Use the project detail which includes milestones
    try {
      const project = await projectsApi.get(projectId)
      milestones.value = (project as { milestones?: ProjectMilestoneDTO[] }).milestones || []
    } catch (err) {
      error.value = err as Error
    }
  }

  const createProject = async (data: Record<string, unknown>) => {
    const project = await projectsApi.create(data)
    projects.value.push(project)
    return project
  }

  const updateProject = async (id: number, data: Record<string, unknown>) => {
    const project = await projectsApi.update(id, data)
    const index = projects.value.findIndex((p) => p.id === id)
    if (index !== -1) {
      projects.value[index] = project
    }
    if (currentProject.value?.id === id) {
      currentProject.value = project
    }
    return project
  }

  const deleteProject = async (id: number) => {
    await projectsApi.delete(id)
    projects.value = projects.value.filter((p) => p.id !== id)
    if (currentProject.value?.id === id) {
      currentProject.value = null
    }
  }

  return {
    projects,
    currentProject,
    members,
    milestones,
    loading,
    error,
    activeProjects,
    loadProjects,
    loadProject,
    loadMembers,
    loadMilestones,
    createProject,
    updateProject,
    deleteProject,
  }
})