// Business Entity Types

export interface UserDTO {
  id: string
  name: string
  email: string
  avatar?: string
  roles: string[]
  createdAt: string
}

export interface TaskDTO {
  id: string
  title: string
  description?: string
  status: 'todo' | 'in_progress' | 'blocked' | 'done'
  priority: 'low' | 'medium' | 'high'
  assignee?: UserDTO
  projectId?: string
  deadline?: string
  createdAt: string
  updatedAt: string
}

export interface ProjectDTO {
  id: string
  name: string
  description?: string
  status: 'active' | 'completed' | 'paused' | 'archived'
  progress: number
  startDate?: string
  endDate?: string
  createdAt: string
  updatedAt: string
}

export interface ProjectMemberDTO {
  userId: string
  userName: string
  role: string
  joinedAt: string
}

export interface ProjectMilestoneDTO {
  id: string
  name: string
  status: 'pending' | 'in_progress' | 'completed'
  deadline?: string
  description?: string
}

export interface CustomerDTO {
  id: string
  name: string
  description?: string
  healthScore?: number
  status: 'active' | 'inactive' | 'churned'
  createdAt: string
  updatedAt: string
}

export interface FileDTO {
  id: string
  name: string
  type: string
  size: number
  customerId?: string
  projectId?: string
  path: string
  thumbnail?: string
  createdAt: string
  updatedAt: string
}

export interface BestPracticeDTO {
  id: string
  title: string
  summary: string
  content: string
  category?: string
  author?: string
  tags?: string[]
  createdAt: string
  updatedAt: string
}

export interface SopDTO {
  id: string
  title: string
  description: string
  content: string
  status: 'active' | 'draft' | 'archived'
  version: number
  updatedAt: string
}

export interface LearningPathDTO {
  id: string
  name: string
  description?: string
  steps: Array<{
    title: string
    description?: string
    type: string
    resourceId?: string
  }>
  currentStep?: number
}