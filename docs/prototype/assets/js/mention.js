/* ==========================================================================
   FDE 工作台 · @ 引用上下文选择弹窗
   5 类业务对象：project / task / customer / file / case
   ========================================================================== */

const mentionData = [
  // 项目
  {cat: 'project',  iconId: 'i-project',  iconCls: 'ico-primary', name: '阿里云A数据中台交付项目', meta: '实施阶段 · 健康度 78 · 8 人'},
  {cat: 'project',  iconId: 'i-project',  iconCls: 'ico-primary', name: '客户 B 营销数据平台',     meta: '验收阶段 · 健康度 65 · 5 人'},
  {cat: 'project',  iconId: 'i-project',  iconCls: 'ico-primary', name: '客户 C 智能客服项目',     meta: '实施阶段 · 健康度 35 · 6 人'},
  {cat: 'project',  iconId: 'i-project',  iconCls: 'ico-primary', name: '客户 D 数据治理咨询',     meta: '启动阶段 · 健康度 -- · 3 人'},
  // 任务
  {cat: 'task',     iconId: 'i-task',     iconCls: 'ico-success', name: '完成阿里云A客户的 POC 方案', meta: 'P0 · 明天截止 · 进行中'},
  {cat: 'task',     iconId: 'i-task',     iconCls: 'ico-success', name: '阿里云A数据接入开发',         meta: 'P0 · 进行中 · 已 2 天'},
  {cat: 'task',     iconId: 'i-task',     iconCls: 'ico-success', name: '本周项目周报编写',           meta: 'P1 · 进行中'},
  {cat: 'task',     iconId: 'i-task',     iconCls: 'ico-success', name: '需求评审会议材料准备',       meta: 'P1 · 周五截止 · 待办'},
  {cat: 'task',     iconId: 'i-task',     iconCls: 'ico-success', name: '客户 C 风险跟踪',            meta: 'P0 · 进行中'},
  // 客户
  {cat: 'customer', iconId: 'i-users',    iconCls: 'ico-primary', name: '阿里云客户A',                meta: '战略客户 · 3 个在交付项目'},
  {cat: 'customer', iconId: 'i-users',    iconCls: 'ico-primary', name: '客户 B（零售集团）',          meta: '重点客户 · 2 个在交付项目'},
  {cat: 'customer', iconId: 'i-users',    iconCls: 'ico-primary', name: '客户 C（金融行业）',          meta: '重点客户 · 1 个在交付项目'},
  // 文件
  {cat: 'file',     iconId: 'i-file-pdf', iconCls: 'ico-danger',  name: '项目交付方案 v2.1.pdf',       meta: '2.4 MB · 阿里云A数据中台'},
  {cat: 'file',     iconId: 'i-file-doc', iconCls: 'ico-primary', name: '需求规格说明书.docx',         meta: '876 KB · 阿里云A数据中台'},
  {cat: 'file',     iconId: 'i-file-xls', iconCls: 'ico-success', name: '数据字典 v1.3.xlsx',          meta: '1.2 MB · 阿里云A数据中台'},
  {cat: 'file',     iconId: 'i-file-pdf', iconCls: 'ico-danger',  name: 'UAT 测试用例.pdf',            meta: '1.8 MB · 阿里云A数据中台'},
  // 案例
  {cat: 'case',     iconId: 'i-book',     iconCls: 'ico-primary', name: '某银行数据中台交付项目（金牌案例）', meta: '匹配度 92% · 4 个月 · 10 人'},
  {cat: 'case',     iconId: 'i-book',     iconCls: 'ico-primary', name: '某零售集团数据治理项目',                meta: '匹配度 85% · 5 个月 · 8 人'},
  {cat: 'case',     iconId: 'i-book',     iconCls: 'ico-primary', name: '某制造业数据资产盘点',                  meta: '匹配度 76% · 3 个月 · 6 人'}
];

const mentionTabs = [
  {id: 'all',      name: '全部',   iconId: 'i-grid'},
  {id: 'project',  name: '项目',   iconId: 'i-project'},
  {id: 'task',     name: '任务',   iconId: 'i-task'},
  {id: 'customer', name: '客户',   iconId: 'i-users'},
  {id: 'file',     name: '文件',   iconId: 'i-file'},
  {id: 'case',     name: '案例',   iconId: 'i-book'}
];

let currentMentionTab = 'all';

function openMention() {
  const modal = document.getElementById('mention-modal');
  const mask  = document.getElementById('mention-mask');
  if (!modal || !mask) return;
  modal.classList.add('active');
  mask.classList.add('active');
  renderMentionList();
}

function closeMention() {
  document.getElementById('mention-modal')?.classList.remove('active');
  document.getElementById('mention-mask')?.classList.remove('active');
}

function switchMentionTab(tabId) {
  currentMentionTab = tabId;
  document.querySelectorAll('.mention-tab').forEach(t => t.classList.toggle('active', t.dataset.tab === tabId));
  renderMentionList();
}

function renderMentionList() {
  const listEl = document.getElementById('mention-list');
  if (!listEl) return;
  const items = currentMentionTab === 'all' ? mentionData : mentionData.filter(d => d.cat === currentMentionTab);
  listEl.innerHTML = items.map(d => `
    <div class="mention-item" onclick="selectMentionItem(this, '${d.name.replace(/'/g, '&#39;')}', '${d.iconId}', '${d.iconCls}')">
      ${icoSvg(d.iconId, d.iconCls + ' ico-lg')}
      <div class="mention-item-info">
        <div class="mention-item-name">${d.name}</div>
        <div class="mention-item-meta">${d.meta}</div>
      </div>
      <button class="btn btn-default btn-sm">引用</button>
    </div>
  `).join('');
}

function selectMentionItem(_el, name, iconId, iconCls) {
  // 添加为上下文 tag
  const tagsEl = document.getElementById('copilot-context-tags');
  if (tagsEl) {
    const tag = document.createElement('span');
    tag.className = 'copilot-context-tag';
    tag.innerHTML = `${icoSvg(iconId, iconCls + ' ico-sm')} ${name}<span class="close" onclick="this.parentElement.remove()">×</span>`;
    const addBtn = tagsEl.querySelector('.copilot-context-add');
    if (addBtn) tagsEl.insertBefore(tag, addBtn);
    else tagsEl.appendChild(tag);
  }
  closeMention();
}

/* 注入 @ 引用弹窗 DOM（每个页面统一注入） */
function injectMentionModal() {
  if (document.getElementById('mention-modal')) return;
  const html = `
    <div class="mention-mask" id="mention-mask" onclick="closeMention()"></div>
    <div class="mention-modal" id="mention-modal">
      <div class="mention-header">
        <span style="font-weight:600;font-size:13px;">引用上下文</span>
        <div class="mention-search">
          ${icoSvg('i-search','ico-sm ico-muted')}
          <input placeholder="搜索 项目 / 任务 / 客户 / 文件 / 案例">
        </div>
        <button class="btn-text" onclick="closeMention()">${icoSvg('i-x','ico-sm')}</button>
      </div>
      <div class="mention-tabs">
        ${mentionTabs.map(t => `<div class="mention-tab ${t.id==='all'?'active':''}" data-tab="${t.id}" onclick="switchMentionTab('${t.id}')">${icoSvg(t.iconId,'ico-sm')} ${t.name}</div>`).join('')}
      </div>
      <div class="mention-list" id="mention-list"></div>
    </div>
  `;
  document.body.insertAdjacentHTML('beforeend', html);
}
