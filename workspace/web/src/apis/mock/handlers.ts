import { http, HttpResponse } from 'msw'
import { setupWorker } from 'msw/browser'

// Mock data
const mockUser = {
  id: '1',
  name: 'Test User',
  email: 'test@example.com',
  avatar: '/avatars/default.png',
  roles: ['admin'],
}

const mockTasks = [
  {
    id: 't1',
    title: '完成项目需求文档',
    status: 'in_progress',
    priority: 'high',
    assignee: mockUser,
    projectId: 'p1',
    deadline: '2026-05-15',
    createdAt: '2026-04-20',
  },
  {
    id: 't2',
    title: '系统架构设计',
    status: 'todo',
    priority: 'medium',
    assignee: mockUser,
    projectId: 'p1',
    deadline: '2026-05-20',
    createdAt: '2026-04-21',
  },
]

const mockProjects = [
  {
    id: 'p1',
    name: 'FDE工作台',
    description: 'FDE工作台项目',
    status: 'active',
    progress: 30,
    createdAt: '2026-04-01',
  },
]

// Handlers
export const handlers = [
  // Auth
  http.post('/api/v1/auth/login', () => {
    return HttpResponse.json({
      code: 0,
      data: { token: 'mock-token', user: mockUser },
    })
  }),

  http.get('/api/v1/auth/me', () => {
    return HttpResponse.json({
      code: 0,
      data: mockUser,
    })
  }),

  // Dashboard
  http.get('/api/v1/dashboard/stats', () => {
    return HttpResponse.json({
      code: 0,
      data: {
        totalTasks: 24,
        completedTasks: 8,
        activeProjects: 3,
        pendingApprovals: 2,
      },
    })
  }),

  // Tasks
  http.get('/api/v1/tasks', () => {
    return HttpResponse.json({
      code: 0,
      data: {
        items: mockTasks,
        total: mockTasks.length,
        page: 1,
        pageSize: 20,
      },
    })
  }),

  http.post('/api/v1/tasks', async ({ request }) => {
    const body = await request.json()
    return HttpResponse.json({
      code: 0,
      data: { id: 't-new', ...body },
    })
  }),

  // Projects
  http.get('/api/v1/projects', () => {
    return HttpResponse.json({
      code: 0,
      data: {
        items: mockProjects,
        total: mockProjects.length,
        page: 1,
        pageSize: 20,
      },
    })
  }),

  // Customers
  http.get('/api/v1/customers', () => {
    return HttpResponse.json({
      code: 0,
      data: {
        items: [],
        total: 0,
        page: 1,
        pageSize: 20,
      },
    })
  }),

  // Files
  http.get('/api/v1/files', () => {
    return HttpResponse.json({
      code: 0,
      data: {
        items: [],
        total: 0,
        page: 1,
        pageSize: 20,
      },
    })
  }),

  // Mentions
  http.get('/api/v1/mentions/search', ({ request }) => {
    const url = new URL(request.url)
    const query = url.searchParams.get('query') || ''
    return HttpResponse.json({
      code: 0,
      data: {
        tasks: [],
        projects: [],
        customers: [],
        files: [],
        users: [mockUser],
      },
    })
  }),

  // Copilot
  http.post('/api/v1/copilot/chat', async ({ request }) => {
    const body = await request.json()
    return HttpResponse.json({
      code: 0,
      data: {
        id: 'msg-1',
        content: '这是一个模拟的AI回复',
        role: 'assistant',
        timestamp: new Date().toISOString(),
      },
    })
  }),
]

// Setup worker
export const worker = setupWorker(...handlers)

// Start mock worker
export async function setupMock() {
  if (import.meta.env.VITE_USE_MOCK === 'true') {
    await worker.start({
      onUnhandledRequest: 'bypass',
    })
    console.log('[MSW] Mock server started')
  }
}