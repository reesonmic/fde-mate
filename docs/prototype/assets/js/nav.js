/* ==========================================================================
   FDE 工作台 · 导航高亮 + 通用初始化
   ========================================================================== */

const navConfig = [
  {group: '核心工作', items: [
    {id: 'dashboard', name: '工作台',  iconId: 'i-dashboard', href: 'dashboard.html'},
    {id: 'tasks',     name: '任务中心', iconId: 'i-task',      href: 'tasks.html', badge: 8}
  ]},
  {group: '项目管理', items: [
    {id: 'project',   name: '项目空间', iconId: 'i-project',   href: 'project-detail.html'},
    {id: 'customer',  name: '客户空间', iconId: 'i-users',     href: 'customers.html'}
  ]},
  {group: 'AI 加速', items: [
    {id: 'coach',     name: 'FDE',     iconId: 'i-compass',   href: 'coach.html'},
    {id: 'files',     name: '文件中心', iconId: 'i-folder',    href: 'files.html'},
    {id: 'ai-chat',   name: 'AI 对话', iconId: 'i-sparkles',  href: 'ai-chat.html'}
  ]},
  {group: '我的', items: [
    {id: 'analytics', name: '我的分析', iconId: 'i-trending-up', href: '#'},
    {id: 'settings',  name: '系统设置', iconId: 'i-settings',    href: '#'}
  ]}
];

/* 注入页面 Header */
function injectHeader() {
  const headerEl = document.querySelector('.header');
  if (!headerEl) return;
  headerEl.innerHTML = `
    <a class="logo" href="../index.html">
      <span class="logo-mark">F</span>
      <span class="logo-name">FDE 工作台</span>
    </a>
    <div class="header-search">
      ${icoSvg('i-search','ico-sm ico-muted')}
      <input placeholder="搜索项目 / 任务 / 客户 / 文件 / 案例">
      <span class="shortcut">⌘K</span>
    </div>
    <div class="header-actions">
      <button class="header-icon-btn" title="帮助">${icoSvg('i-help-circle','ico-lg')}</button>
      <button class="header-icon-btn" title="通知">${icoSvg('i-bell','ico-lg')}<span class="badge-dot"></span></button>
      <div class="header-user">
        <div class="header-avatar">吾</div>
        <span class="header-username">吾明</span>
        ${icoSvg('i-chevron-down','ico-sm')}
      </div>
    </div>
  `;
}

/* 注入左侧 Nav */
function injectNav(activePageId) {
  const navEl = document.querySelector('.nav');
  if (!navEl) return;
  navEl.innerHTML = navConfig.map(g => `
    <div class="nav-group">
      <div class="nav-group-title">${g.group}</div>
      ${g.items.map(it => {
        const linkable = it.href !== '#';
        const tag      = linkable ? 'a' : 'div';
        const hrefAttr = linkable ? `href="${it.href}"` : '';
        const isActive = it.id === activePageId
          || (activePageId === 'project-detail' && it.id === 'project')
          || (activePageId === 'customers'      && it.id === 'customer');
        return `<${tag} class="nav-item ${isActive?'active':''}" ${hrefAttr}>${icoSvg(it.iconId,'nav-icon')}<span>${it.name}</span>${it.badge?`<span class="nav-badge">${it.badge}</span>`:''}</${tag}>`;
      }).join('')}
    </div>
  `).join('');
}

/* 通用页面初始化 */
function initPage() {
  const pageId = document.body.dataset.page;
  injectHeader();
  injectNav(pageId);
  injectMentionModal();
  if (typeof renderCopilot === 'function') renderCopilot(pageId);
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initPage);
} else {
  initPage();
}
