import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import { setupGuards } from './guards'

const routes: RouteRecordRaw[] = [
  { path: '/login', name: 'Login', component: () => import('@/pages/login/LoginPage.vue'), meta: { layout: 'blank', requiresAuth: false } },
  {
    path: '/',
    component: () => import('@components/layout/AppLayout.vue'),
    redirect: '/dashboard',
    meta: { requiresAuth: true },
    children: [
      { path: 'dashboard', name: 'Dashboard', component: () => import('@/pages/dashboard/DashboardPage.vue'), meta: { title: '工作台', icon: 'home', copilot: 'workspace' } },
      { path: 'tasks', name: 'Tasks', component: () => import('@/pages/tasks/TasksPage.vue'), meta: { title: '任务中心', icon: 'check', copilot: 'tasks' } },
      { path: 'projects', name: 'Projects', component: () => import('@/pages/projects/ProjectsListPage.vue'), meta: { title: '项目', icon: 'folder', copilot: 'project' } },
      { path: 'projects/:id', name: 'ProjectDetail', component: () => import('@/pages/projects/ProjectDetailPage.vue'), meta: { title: '项目详情', copilot: 'project' } },
      { path: 'customers', name: 'Customers', component: () => import('@/pages/customers/CustomersPage.vue'), meta: { title: '客户空间', icon: 'users', copilot: 'chat' } },
      { path: 'files', name: 'Files', component: () => import('@/pages/files/FilesPage.vue'), meta: { title: '文件中心', icon: 'file', copilot: 'files' } },
      { path: 'coach', name: 'Coach', component: () => import('@/pages/coach/CoachIndexPage.vue'), meta: { title: 'FDE 教练', icon: 'graduation', copilot: 'coach' } },
      { path: 'coach/best-practices', name: 'BestPractices', component: () => import('@/pages/coach/BestPracticesPage.vue'), meta: { title: '最佳实践库', copilot: 'coach' } },
      { path: 'coach/sops', name: 'Sops', component: () => import('@/pages/coach/SopsPage.vue'), meta: { title: '方法论 SOP', copilot: 'coach' } },
      { path: 'coach/learning-path', name: 'LearningPath', component: () => import('@/pages/coach/LearningPathPage.vue'), meta: { title: '学习路径', copilot: 'coach' } },
      { path: 'chat', name: 'AiChat', component: () => import('@/pages/chat/AiChatPage.vue'), meta: { title: 'AI 对话中心', icon: 'message', layout: 'chat-only' } },
      { path: 'settings', name: 'Settings', component: () => import('@/pages/settings/SettingsPage.vue'), meta: { title: '设置', icon: 'settings' } },
    ],
  },
  { path: '/:pathMatch(.*)*', name: 'NotFound', component: () => import('@/pages/error/NotFoundPage.vue'), meta: { layout: 'blank' } },
]

const router = createRouter({ history: createWebHistory(), routes })

setupGuards(router)

export default router
