// API Request/Response Types

import type {
  UserDTO,
  TaskDTO,
  ProjectDTO,
  ProjectMemberDTO,
  ProjectMilestoneDTO,
  CustomerDTO,
  FileDTO,
  BestPracticeDTO,
  SopDTO,
  LearningPathDTO,
} from './business'

// Auth
export interface LoginRequest {
  username: string
  password: string
}

export interface LoginResponse {
  token: string
  user: UserDTO
}

export interface UserInfo extends UserDTO {}

// Pagination
export interface PageRequest {
  page?: number
  pageSize?: number
  sortBy?: string
  sortOrder?: 'asc' | 'desc'
}

export interface PageResponse<T> {
  items: T[]
  total: number
  page: number
  pageSize: number
}

// Dashboard
export interface DashboardStats {
  totalTasks: number
  completedTasks: number
  activeProjects: number
  pendingApprovals: number
}

export interface DashboardChartData {
  dates: string[]
  values: number[]
}

// Tasks
export interface TaskCreateRequest {
  title: string
  description?: string
  priority?: 'p0' | 'p1' | 'p2' | 'p3'
  assigneeId?: number
  projectId?: number
  dueAt?: string
  tags?: string[]
}

export interface TaskUpdateRequest {
  title?: string
  description?: string
  status?: 'todo' | 'in_progress' | 'review' | 'done' | 'blocked'
  priority?: 'p0' | 'p1' | 'p2' | 'p3'
  assigneeId?: number
  dueAt?: string
  tags?: string[]
}

export interface TaskQueryParams extends PageRequest {
  status?: string
  priority?: string
  assigneeId?: number
  projectId?: number
}

// Projects
export interface ProjectCreateRequest {
  name: string
  description?: string
  startDate?: string
  endDate?: string
}

export interface ProjectUpdateRequest {
  name?: string
  description?: string
  status?: 'active' | 'completed' | 'paused' | 'archived'
  startDate?: string
  endDate?: string
}

export interface ProjectQueryParams extends PageRequest {
  status?: string
}

// Customers
export interface CustomerCreateRequest {
  name: string
  description?: string
}

export interface CustomerUpdateRequest {
  name?: string
  description?: string
  healthScore?: number
  status?: 'active' | 'inactive' | 'churned'
}

export interface CustomerQueryParams extends PageRequest {
  status?: string
}

// Files
export interface FileUploadRequest {
  file: File
  customerId?: string
  projectId?: string
  path?: string
}

export interface FileQueryParams extends PageRequest {
  customerId?: string
  projectId?: string
  type?: string
}

// Coach
export interface CoachQueryParams extends PageRequest {
  category?: string
  query?: string
}

// Copilot
export interface CopilotRequest {
  assistantId: string
  message: string
  sessionId?: string
  mode?: 'smart' | 'creative' | 'rigorous'
  context?: Record<string, unknown>
  mentions?: Array<{ type: string; id: string; label: string }>
}

export interface ActionPreview {
  actionId: string
  toolName: string
  params: Record<string, unknown>
  preview: string
  expiresAt: string
}

export interface ActionExecute {
  actionId: string
  toolName: string
}

// Mentions
export interface MentionSearchResult {
  tasks: TaskDTO[]
  projects: ProjectDTO[]
  customers: CustomerDTO[]
  files: FileDTO[]
  users: UserDTO[]
}

// API Response Wrapper
export interface ApiResponse<T> {
  code: number
  message?: string
  data: T
}

export interface ApiErrorResponse {
  code: number
  message: string
  details?: Record<string, unknown>
}