// Copilot Types

export interface CopilotMessage {
  id: string
  content: string
  role: 'user' | 'assistant'
  timestamp: string
  type?: 'text' | 'action' | 'report' | 'nextSteps' | 'searchResults'
  metadata?: any
}

export interface CopilotSession {
  id: string
  assistantType: 'task' | 'project' | 'coach' | 'file' | 'chat'
  messages: CopilotMessage[]
  createdAt: string
  updatedAt: string
}

export interface CopilotAction {
  actionId: string
  toolName: string
  params: any
  preview: string
  expiresAt: string
}

export interface CopilotState {
  currentAssistant: 'task' | 'project' | 'coach' | 'file' | 'chat'
  sessions: Record<string, CopilotSession>
  pendingAction?: CopilotAction
}

// Assistant Configuration
export interface AssistantConfig {
  key: string
  name: string
  description: string
  icon?: string
  capabilities: string[]
  tools: string[]
}