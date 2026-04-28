/* ==========================================================================
   FDE 工作台 · Copilot 配置 + 渲染逻辑
   4 个页面级助手：tasks(T 蓝) / project-detail(P 紫) / coach(C 青) / files(F 橙)
   ========================================================================== */

const copilotConfig = {
  'dashboard': {
    badgeKey: 'task', badgeLetter: 'W', name: '工作台助手',
    context: ['当前页: 工作台', '今日任务: 8 项 · P0 3 项', '今日会议: 3 场', '在交付项目: 4 个'],
    suggestions: ['帮我准备晨会要点', '今天最重要的 3 件事', '生成今日工作日报', '把客户C 的风险升级给团队'],
    messages: [
      {role: 'ai', text: '早上好，吾明 ☀️<br/>我是你的 <b>工作台助手</b>，可帮你做：晨会准备、聚焦今日 Top 3、生成日报、跨场景跳转执行。'},
      {role: 'user', text: '帮我准备一下今天的晨会要点'},
      {role: 'ai', text: '已基于你的 4 个在交付项目，整理今日晨会要点：', report: {
        titleIcon: 'i-flag', title: '今日晨会要点 · 2026-04-28',
        risks: [
          {level: 'high', label: '焦点', desc: '阿里云A：数据接入 60% / 客户A POC 方案明天交付'},
          {level: 'mid',  label: '风险', desc: '客户C 智能客服项目健康度 35，需团队介入'},
          {level: 'low',  label: '协同', desc: '客户B 验收材料已就绪，下午 14:00 评审会'}
        ]
      }},
      {role: 'user', text: '今天我最重要的 3 件事是什么？'},
      {role: 'ai', text: '基于优先级 + 截止时间 + 项目健康度综合分析：', nextSteps: [
        '【上午】完成客户A 的 POC 方案（明天 18:00 截止 · P0）',
        '【下午 14:00】客户B 需求评审会，确认验收标准',
        '【下班前】客户C 风险升级邮件 + 团队协调会议邀请'
      ]}
    ]
  },

  'tasks': {
    badgeKey: 'task', badgeLetter: 'T', name: '任务助手',
    context: ['当前页: 任务中心', '我的任务: 8 项 · 逾期 1 项', '本周新增: 5 项'],
    suggestions: ['创建一个 P0 任务', '分析下我的工作量', '把所有逾期任务延期到下周五', '帮我归档已完成的任务'],
    messages: [
      {role: 'ai', text: '你好！我是 <b>任务助手</b><br/>我可以帮你：创建任务、查询任务、批量调整、工作量分析。所有写操作都会先预览给你确认。'},
      {role: 'user', text: '创建一个明天截止的 P0 任务：完成客户A的POC方案'},
      {role: 'ai', text: '好的，我已生成任务预览，请确认：', actionCard: {
        titleIcon: 'i-plus', title: '创建任务', status: 'pending',
        rows: [
          {label: '标题',     value: '完成客户A的POC方案'},
          {label: '优先级',   value: 'P0', addClass: 'add'},
          {label: '截止时间', value: '2026-04-29 18:00'},
          {label: '关联项目', value: '阿里云A数据中台'}
        ]
      }},
      {role: 'user', text: '把所有逾期任务延期到下周五'},
      {role: 'ai', text: '我找到了 3 个逾期任务，请确认批量操作：', actionCard: {
        titleIcon: 'i-history', title: '批量修改', status: 'pending',
        rows: [
          {label: '操作', value: '修改截止时间'},
          {label: '新值', value: '2026-05-02', addClass: 'add'}
        ],
        impact: ['1. 客户 B 数据接入测试（原 4-25）', '2. 内部技术分享 PPT（原 4-26）', '3. 季度复盘报告（原 4-27）']
      }}
    ]
  },

  'project-detail': {
    badgeKey: 'project', badgeLetter: 'P', name: '项目助手',
    context: ['当前项目: 阿里云A数据中台', '阶段: 实施中', '健康度: 78'],
    suggestions: ['分析下当前项目风险', '生成本周项目周报', '把负责人改成张三', '推荐 1 个相似案例'],
    messages: [
      {role: 'ai', text: '你好！我是 <b>项目助手</b><br/>我已绑定<b>阿里云A数据中台</b>项目，可帮你分析风险、生成报告、调整成员/里程碑。'},
      {role: 'user', text: '分析下当前项目的风险'},
      {role: 'ai', text: '基于项目当前状态，我识别出以下 3 个风险：', report: {
        titleIcon: 'i-alert-triangle', title: '项目风险分析报告',
        risks: [
          {level: 'high', label: '高', desc: '数据接入进度滞后 5 天，可能影响 5/20 UAT 节点'},
          {level: 'mid',  label: '中', desc: '客户方接口联调资源不足，建议提前 1 周协调'},
          {level: 'low',  label: '低', desc: '上线前性能压测尚未启动，建议本周内排期'}
        ]
      }},
      {role: 'user', text: '把负责人改成张三'},
      {role: 'ai', text: '已生成修改预览，请确认：', actionCard: {
        titleIcon: 'i-settings', title: '修改项目负责人', status: 'pending',
        rows: [
          {label: '项目',     value: '阿里云A数据中台'},
          {label: '原负责人', value: '吾明', delClass: 'del'},
          {label: '新负责人', value: '张三', addClass: 'add'}
        ]
      }}
    ]
  },

  'coach': {
    badgeKey: 'coach', badgeLetter: 'C', name: 'FDE 专家 AI',
    context: ['当前项目: 阿里云A数据中台', '项目阶段: 实施中', '我的等级: P5 · 第 2 年 FDE', '专家身份: 10 年交付经验'],
    suggestions: ['实施阶段我下一步该做什么', '客户验收冲突怎么处理', '怎么把技术方案讲给客户 CTO', '项目延期 5 天我该怎么挽救'],
    messages: [
      {role: 'ai', text: '你好！我是 <b>FDE 专家 AI</b>（10 年交付经验，已学习 86 案例 + 128 SOP）<br/>有任何 FDE 工作问题，直接问我，我会基于你的项目背景给出针对性建议。'},
      {role: 'user', text: '实施阶段我下一步该做什么？'},
      {role: 'ai', text: '基于你当前所在的<b>实施阶段</b>（阿里云A数据中台 · 健康度 78），我推荐以下 5 个 Next Step：', nextSteps: [
        '完成数据源接入与质量校验，确保上游数据完整性',
        '组织一次客户内部演示，提前验证关键场景',
        '编写 UAT 测试用例，提前 2 周与客户对齐验收标准',
        '识别上线前可能的运维风险，准备应急预案',
        '启动客户培训计划，沉淀知识传递文档'
      ]},
      {role: 'user', text: '客户验收时如果起冲突怎么处理？'},
      {role: 'ai', text: '基于「客户验收冲突 · 4 步化解法」最佳实践，我给你 4 步建议：', report: {
        titleIcon: 'i-shield-check', title: '客户验收冲突 · 4 步化解法',
        risks: [
          {level: 'high', label: '步1', desc: '先共情后澄清：「我理解您的顾虑，能否帮我确认一下具体是哪部分不符合预期？」'},
          {level: 'mid',  label: '步2', desc: '锁定核心争议：列出 2-3 个客户最在意的点，避免话题发散'},
          {level: 'mid',  label: '步3', desc: '提出可行方案：给出 A/B 两个方案 + 时间承诺，让客户做选择题而非问答题'},
          {level: 'low',  label: '步4', desc: '闭环跟进：会后 24h 内发送会议纪要 + Action Plan，并约定下次同步时间'}
        ]
      }}
    ]
  },

  'files': {
    badgeKey: 'files', badgeLetter: 'F', name: '文件助手',
    context: ['当前路径: 项目空间/阿里云A/交付物', '已选中: 项目交付方案 v2.1.pdf', '文件夹: 6 个文件'],
    suggestions: ['帮我找客户A最近 1 周的需求文档', '总结下当前 PDF 的关键信息', '对比 v2.0 和 v2.1 的差异', '把所有验收文档归档到 客户验收/2026Q2'],
    messages: [
      {role: 'ai', text: '你好！我是 <b>文件助手</b><br/>我可以帮你：智能搜索、文档总结、版本对比、批量归档。已自动绑定<b>当前路径</b>和<b>选中文件</b>。'},
      {role: 'user', text: '帮我找客户A最近 1 周的需求文档'},
      {role: 'ai', text: '为你找到 4 份相关文档：', searchResults: [
        {iconId: 'i-file-doc', iconCls: 'ico-primary', name: '需求规格说明书.docx',   meta: '876 KB · 4-22 · 阿里云A数据中台'},
        {iconId: 'i-file-pdf', iconCls: 'ico-danger',  name: '客户需求确认单.pdf',     meta: '1.2 MB · 4-21 · 阿里云A数据中台'},
        {iconId: 'i-file-pdf', iconCls: 'ico-danger',  name: 'POC 需求清单.pdf',       meta: '520 KB · 4-19 · 阿里云A数据中台'},
        {iconId: 'i-file-doc', iconCls: 'ico-primary', name: '数据字典补充说明.docx', meta: '340 KB · 4-18 · 阿里云A数据中台'}
      ]},
      {role: 'user', text: '总结下《项目交付方案 v2.1.pdf》的关键信息'},
      {role: 'ai', text: '已为你总结 PDF 的关键信息：', report: {
        titleIcon: 'i-file-pdf', title: '项目交付方案 v2.1 · 关键信息',
        risks: [
          {level: 'high', label: '核心', desc: '交付周期 4 个月，分 5 个里程碑，UAT 安排在 2026-05-20'},
          {level: 'mid',  label: '变更', desc: '相比 v2.0，新增数据接入模块（第 3 章）、调整 UAT 验收标准（第 6 章）'},
          {level: 'low',  label: '范围', desc: '交付范围包含数据中台底座 + 4 个业务主题域'}
        ]
      }},
      {role: 'user', text: '把所有验收文档归档到 客户验收/2026Q2 文件夹'},
      {role: 'ai', text: '我找到了 8 个验收文档，请确认批量归档：', actionCard: {
        titleIcon: 'i-folder', title: '批量归档', status: 'pending',
        rows: [
          {label: '操作',     value: '移动文件'},
          {label: '目标位置', value: '客户验收 / 2026Q2', addClass: 'add'},
          {label: '文件数量', value: '8 个'}
        ],
        impact: ['1. UAT 测试用例.pdf', '2. 客户验收报告 v1.docx', '3. UAT 缺陷清单.xlsx', '4. 上线 Checklist.pdf', '... 还有 4 个']
      }}
    ]
  }
};

/* ========== 渲染 Copilot ========== */
function renderCopilot(pageId) {
  const copilot = document.getElementById('copilot');
  if (!copilot) return;
  const cfg = copilotConfig[pageId];
  if (!cfg) { copilot.classList.add('hidden'); return; }
  copilot.classList.remove('hidden', 'collapsed');

  const badge   = badgeHtml(cfg.badgeKey, cfg.badgeLetter);
  const badgeSm = badgeHtml(cfg.badgeKey, cfg.badgeLetter, 'sm');

  copilot.innerHTML = `
    <div class="copilot-collapsed-bar" onclick="toggleCopilot()">
      <div class="copilot-icon">${badgeSm}</div>
      <div class="copilot-collapsed-text">${cfg.name}</div>
      <button class="btn-text" style="font-size:14px;">${icoSvg('i-chevron-left','ico-sm')}</button>
    </div>
    <div class="copilot-header">
      <div>${badge}</div>
      <div class="copilot-header-info">
        <div class="copilot-header-name">${cfg.name}</div>
        <div class="copilot-header-meta">基于 GPT-4 + 业务知识库</div>
      </div>
      <div class="copilot-header-actions">
        <button class="btn-text" title="新对话">${icoSvg('i-plus','ico-sm')}</button>
        <button class="btn-text" title="历史">${icoSvg('i-history','ico-sm')}</button>
        <button class="btn-text" title="折叠" onclick="toggleCopilot()">${icoSvg('i-chevron-right','ico-sm')}</button>
      </div>
    </div>
    <div class="copilot-context">
      <div class="copilot-context-label">${icoSvg('i-pin','ico-sm')}当前上下文</div>
      <div class="copilot-context-tags" id="copilot-context-tags">
        ${cfg.context.map(c => `<span class="copilot-context-tag">${c}<span class="close">×</span></span>`).join('')}
        <span class="copilot-context-add">+ 添加</span>
      </div>
    </div>
    <div class="copilot-body" id="copilot-body">
      ${cfg.messages.map(m => renderMessage(m, badgeSm)).join('')}
    </div>
    <div class="copilot-input-area">
      <div class="copilot-suggestions">
        ${cfg.suggestions.map(s => `<span class="copilot-suggestion-chip">${s}</span>`).join('')}
      </div>
      <div class="copilot-input-box">
        <textarea class="copilot-input" placeholder="向${cfg.name}提问，按 Enter 发送 / Shift+Enter 换行"></textarea>
        <div class="copilot-input-tools">
          <span class="copilot-tool-btn" onclick="openMention()">${icoSvg('i-at-sign','ico-sm')}引用</span>
          <span class="copilot-tool-btn">${icoSvg('i-paperclip','ico-sm')}附件</span>
          <span class="copilot-tool-btn">${icoSvg('i-sparkles','ico-sm')}增强</span>
          <button class="copilot-send-btn">${icoSvg('i-send','ico-sm')}发送</button>
        </div>
      </div>
    </div>
  `;

  setTimeout(() => {
    const body = document.getElementById('copilot-body');
    if (body) body.scrollTop = body.scrollHeight;
  }, 50);
}

function renderMessage(m, badgeSm) {
  if (m.role === 'user') {
    return `<div class="copilot-msg copilot-msg-user"><div class="copilot-bubble">${m.text}</div></div>`;
  }
  let bubble = `<div class="copilot-msg-avatar-wrap">${badgeSm}</div><div class="copilot-bubble">${m.text}`;

  if (m.actionCard) {
    const ac = m.actionCard;
    const statusHtml = ac.status === 'pending'
      ? `<span class="action-status pending">${icoSvg('i-hourglass','ico-sm')}待确认</span>`
      : ac.status === 'running'
        ? `<span class="action-status running">${icoSvg('i-history','ico-sm')}执行中</span>`
        : `<span class="action-status done">${icoSvg('i-check-circle','ico-sm')}已完成</span>`;
    const titleIconHtml = ac.titleIcon ? icoSvg(ac.titleIcon, 'ico-sm ico-primary') : '';
    bubble += `<div class="action-card"><div class="action-card-header"><span class="action-card-title">${titleIconHtml}${ac.title}</span>${statusHtml}</div><div class="action-card-body">`;
    ac.rows.forEach(r => {
      bubble += `<div class="action-row"><div class="action-row-label">${r.label}</div><div class="action-row-value ${r.addClass||''} ${r.delClass||''}">${r.value}</div></div>`;
    });
    if (ac.impact) {
      bubble += `<div class="action-impact">${icoSvg('i-alert-triangle','ico-sm ico-warning')}影响 ${ac.impact.length} 个对象<div class="action-impact-list">` + ac.impact.map(i => `<div class="action-impact-list-item">${i}</div>`).join('') + `</div></div>`;
    }
    bubble += `</div><div class="action-card-footer"><button class="btn btn-default btn-sm">取消</button><button class="btn btn-primary btn-sm">${icoSvg('i-check-circle','ico-sm')}确认执行</button></div></div>`;
  }

  if (m.report) {
    const rTitleIcon = m.report.titleIcon ? icoSvg(m.report.titleIcon, 'ico-sm ico-primary') : '';
    bubble += `<div class="report-card"><div class="report-card-title">${rTitleIcon}${m.report.title}</div>`;
    m.report.risks.forEach(r => {
      bubble += `<div class="report-risk-row"><span class="risk-level ${r.level}">${r.label}</span><span>${r.desc}</span></div>`;
    });
    bubble += `</div>`;
  }

  if (m.nextSteps) {
    bubble += `<div class="next-step-list">` + m.nextSteps.map((s,i) => `<div class="next-step-item"><div class="next-step-num">${i+1}</div><div>${s}</div></div>`).join('') + `</div>`;
  }

  if (m.searchResults) {
    bubble += `<div class="search-results-card">` + m.searchResults.map(r => `<div class="search-result-item">${icoSvg(r.iconId, r.iconCls + ' ico-lg')}<div class="search-result-info"><div class="search-result-name">${r.name}</div><div class="search-result-meta">${r.meta}</div></div><button class="btn-text">${icoSvg('i-arrow-right','ico-sm')}</button></div>`).join('') + `</div>`;
  }

  bubble += `</div>`;
  return `<div class="copilot-msg copilot-msg-ai">${bubble}</div>`;
}

function toggleCopilot() {
  const c = document.getElementById('copilot');
  if (c) c.classList.toggle('collapsed');
}
