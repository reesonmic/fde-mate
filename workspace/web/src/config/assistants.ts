import type { AssistantConfig } from '@/types/copilot'

/**
 * Assistant Configuration
 * Defines the 5 assistants available in FDE Workbench
 */
export const ASSISTANT_CONFIG: AssistantConfig[] = [
  {
    key: 'task',
    name: 'T助手',
    description: '任务管理助手 - 帮助管理任务、批量操作',
    icon: '📋',
    capabilities: [
      '创建任务',
      '更新任务状态',
      '批量操作',
      '任务提醒',
    ],
    tools: [
      'create_task',
      'update_task',
      'batch_update_status',
      'delete_task',
    ],
  },
  {
    key: 'project',
    name: 'P助手',
    description: '项目助手 - 帮助生成周报、分析风险',
    icon: '📁',
    capabilities: [
      '生成周报',
      '更新里程碑',
      '风险分析',
      '进度跟踪',
    ],
    tools: [
      'generate_weekly_report',
      'update_milestone',
      'analyze_risks',
      'get_project_progress',
    ],
  },
  {
    key: 'coach',
    name: 'C助手',
    description: '教练助手 - 10年FDE专家经验，解答问题',
    icon: '👨‍🏫',
    capabilities: [
      '查询最佳实践',
      '查询SOP',
      '专家问答',
      '建议学习路径',
    ],
    tools: [
      'find_best_practice',
      'find_sop',
      'ask_question',
      'suggest_learning_path',
    ],
  },
  {
    key: 'file',
    name: 'F助手',
    description: '文件助手 - 智能搜索、文件摘要',
    icon: '📄',
    capabilities: [
      '智能搜索',
      '文件摘要',
      '文件对比',
      '内容分析',
    ],
    tools: [
      'search_files',
      'summarize_file',
      'compare_files',
      'analyze_content',
    ],
  },
  {
    key: 'chat',
    name: '全局对话',
    description: '自由对话模式 - 不绑定特定助手',
    icon: '💬',
    capabilities: [
      '自由问答',
      '跨领域查询',
      '综合分析',
    ],
    tools: [
      'general_query',
      'cross_domain_search',
    ],
  },
]

/**
 * Get assistant config by key
 */
export function getAssistantConfig(key: string): AssistantConfig | undefined {
  return ASSISTANT_CONFIG.find((a) => a.key === key)
}

/**
 * Get all assistant keys
 */
export function getAssistantKeys(): string[] {
  return ASSISTANT_CONFIG.map((a) => a.key)
}