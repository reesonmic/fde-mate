// Business Entity Types

export interface UserDTO {
  id: number
  name: string
  email: string
  avatar?: string
  roles: string[]
  createdAt: string
}

export interface TaskDTO {
  id: number
  title: string
  description?: string
  status: 'todo' | 'in_progress' | 'review' | 'done' | 'blocked'
  priority: 'p0' | 'p1' | 'p2' | 'p3'
  assignee_id?: number
  projectId?: number
  dueAt?: string
  tags?: string[]
  creator_id?: number
  gmtCreate: string
  gmtModified: string
}

export interface ProjectDTO {
  id: number
  name: string
  customer_id?: number
  phase: 'init' | 'discovery' | 'delivery' | 'review' | 'closed'
  health: number
  owner_id: number
  owner_name?: string
  start_at: string
  end_at?: string
  members: ProjectMemberDTO[]
  milestones: ProjectMilestoneDTO[]
  risks: RiskDTO[]
  gmtCreate: string
  gmtModified: string
}

export interface ProjectMemberDTO {
  id: number
  user_id: number
  user_name: string
  role: string
}

export interface ProjectMilestoneDTO {
  id: number
  title: string
  dueAt: string
  done: boolean
}

export interface RiskDTO {
  id: number
  title: string
  level: 'low' | 'medium' | 'high'
  mitigation?: string
  status: string
}

export interface CustomerDTO {
  id: number
  name: string
  industry?: string
  scale?: string
  owner_id?: number
  contacts: ContactDTO[]
  opportunities: OpportunityDTO[]
  gmtCreate: string
  gmtModified: string
}

export interface ContactDTO {
  id: number
  customer_id: number
  name: string
  title?: string
  phone?: string
  email?: string
  gmtCreate: string
}

export interface OpportunityDTO {
  id: number
  customer_id: number
  title: string
  stage: string
  amount?: number
  close_at?: string
  gmtCreate: string
}

export interface FileDTO {
  id: number
  name: string
  ext: string
  size: number
  scope: string
  scope_id?: number
  owner_id: number
  oss_key: string
  rag_indexed: number
  gmtCreate: string
  gmtModified: string
}

export interface BestPracticeDTO {
  id: number
  title: string
  summary: string
  content: string
  category?: string
  author?: string
  tags?: string[]
  gmtCreate: string
  gmtModified: string
}

export interface SopDTO {
  id: number
  title: string
  description: string
  content: string
  status: 'active' | 'draft' | 'archived'
  version: number
  gmtCreate: string
  gmtModified: string
}

export interface LearningPathDTO {
  id: number
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

export interface WeeklyReportDTO {
  id: number
  project_id: number
  week_start: string
  week_end: string
  content: string
  created_by: number
  gmtCreate: string
}