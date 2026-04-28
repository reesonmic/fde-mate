/* ==========================================================================
   FDE 工作台 · SVG Sprite（Lucide 风格图标库）
   每个 symbol 都使用 24x24 viewBox / 1.5px stroke
   使用方式：<svg class="ico"><use href="#i-xxx"/></svg>
   ========================================================================== */

const SVG_SPRITE = `
<svg xmlns="http://www.w3.org/2000/svg" style="display:none;">
  <!-- 导航类 -->
  <symbol id="i-dashboard" viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="9" rx="1"/><rect x="14" y="3" width="7" height="5" rx="1"/><rect x="14" y="12" width="7" height="9" rx="1"/><rect x="3" y="16" width="7" height="5" rx="1"/></symbol>
  <symbol id="i-task" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="16" rx="2"/><path d="M8 10l2.5 2.5L16 7"/></symbol>
  <symbol id="i-project" viewBox="0 0 24 24"><path d="M3 7a2 2 0 012-2h4l2 2h8a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V7z"/></symbol>
  <symbol id="i-users" viewBox="0 0 24 24"><circle cx="9" cy="8" r="3.5"/><path d="M3 20c0-3 2.5-5.5 6-5.5s6 2.5 6 5.5"/><circle cx="17" cy="9" r="2.5"/><path d="M15 20c0-2 1-4 4-4"/></symbol>
  <symbol id="i-compass" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M15.5 8.5l-2 5-5 2 2-5 5-2z"/></symbol>
  <symbol id="i-folder" viewBox="0 0 24 24"><path d="M3 7a2 2 0 012-2h4l2 2h8a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V7z"/></symbol>
  <symbol id="i-sparkles" viewBox="0 0 24 24"><path d="M12 3l1.8 4.5L18 9l-4.2 1.5L12 15l-1.8-4.5L6 9l4.2-1.5L12 3z"/><path d="M19 14l.9 2.1L22 17l-2.1.9L19 20l-.9-2.1L16 17l2.1-.9L19 14z"/></symbol>
  <symbol id="i-trending-up" viewBox="0 0 24 24"><path d="M3 17l6-6 4 4 8-8"/><path d="M14 7h7v7"/></symbol>
  <symbol id="i-settings" viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 11-2.83 2.83l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 11-4 0v-.09A1.65 1.65 0 008 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 11-2.83-2.83l.06-.06A1.65 1.65 0 004.6 15a1.65 1.65 0 00-1.51-1H3a2 2 0 110-4h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 112.83-2.83l.06.06A1.65 1.65 0 009 4.6a1.65 1.65 0 001-1.51V3a2 2 0 114 0v.09A1.65 1.65 0 0015 4.6a1.65 1.65 0 001.82-.33l.06-.06a2 2 0 112.83 2.83l-.06.06A1.65 1.65 0 0019.4 9c.16.39.27.82.27 1.27"/></symbol>

  <!-- 操作类 -->
  <symbol id="i-search" viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.5-4.5"/></symbol>
  <symbol id="i-bell" viewBox="0 0 24 24"><path d="M6 8a6 6 0 0112 0c0 6 3 8 3 8H3s3-2 3-8z"/><path d="M10 21a2 2 0 004 0"/></symbol>
  <symbol id="i-help-circle" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M9.5 9a2.5 2.5 0 015 0c0 1.5-2.5 2-2.5 4"/><circle cx="12" cy="17" r="0.5" fill="currentColor"/></symbol>
  <symbol id="i-chevron-down" viewBox="0 0 24 24"><polyline points="6,9 12,15 18,9"/></symbol>
  <symbol id="i-chevron-left" viewBox="0 0 24 24"><polyline points="15,18 9,12 15,6"/></symbol>
  <symbol id="i-chevron-right" viewBox="0 0 24 24"><polyline points="9,18 15,12 9,6"/></symbol>
  <symbol id="i-arrow-right" viewBox="0 0 24 24"><line x1="4" y1="12" x2="20" y2="12"/><polyline points="14,6 20,12 14,18"/></symbol>
  <symbol id="i-plus" viewBox="0 0 24 24"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></symbol>
  <symbol id="i-x" viewBox="0 0 24 24"><line x1="6" y1="6" x2="18" y2="18"/><line x1="18" y1="6" x2="6" y2="18"/></symbol>
  <symbol id="i-check" viewBox="0 0 24 24"><polyline points="5,12 10,17 20,7"/></symbol>
  <symbol id="i-check-circle" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><polyline points="8,12 11,15 16,9"/></symbol>
  <symbol id="i-edit" viewBox="0 0 24 24"><path d="M14 4l6 6-12 12H2v-6L14 4z"/></symbol>
  <symbol id="i-trash" viewBox="0 0 24 24"><path d="M3 6h18M8 6V4a2 2 0 012-2h4a2 2 0 012 2v2M6 6l1 14a2 2 0 002 2h6a2 2 0 002-2l1-14"/></symbol>
  <symbol id="i-upload" viewBox="0 0 24 24"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/><polyline points="17,8 12,3 7,8"/><line x1="12" y1="3" x2="12" y2="15"/></symbol>
  <symbol id="i-download" viewBox="0 0 24 24"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/><polyline points="7,10 12,15 17,10"/><line x1="12" y1="15" x2="12" y2="3"/></symbol>
  <symbol id="i-paperclip" viewBox="0 0 24 24"><path d="M21 11.5L12 20.5a5 5 0 01-7-7l9-9a3.5 3.5 0 015 5l-9 9a2 2 0 01-3-3l8-8"/></symbol>
  <symbol id="i-at-sign" viewBox="0 0 24 24"><circle cx="12" cy="12" r="4"/><path d="M16 8v5a3 3 0 006 0v-1a9 9 0 10-9 9"/></symbol>
  <symbol id="i-send" viewBox="0 0 24 24"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22,2 15,22 11,13 2,9 22,2"/></symbol>

  <!-- 状态类 -->
  <symbol id="i-alert-triangle" viewBox="0 0 24 24"><path d="M10.3 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><circle cx="12" cy="17" r="0.5" fill="currentColor"/></symbol>
  <symbol id="i-shield-check" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="9,12 11,14 15,10"/></symbol>
  <symbol id="i-zap" viewBox="0 0 24 24"><polygon points="13,2 3,14 12,14 11,22 21,10 12,10 13,2"/></symbol>
  <symbol id="i-flag" viewBox="0 0 24 24"><path d="M4 22V4M4 4h13l-2 4 2 4H4"/></symbol>
  <symbol id="i-pin" viewBox="0 0 24 24"><path d="M12 17v5M9 3h6l-1 6 4 3v2H6v-2l4-3-1-6z"/></symbol>
  <symbol id="i-history" viewBox="0 0 24 24"><path d="M3 12a9 9 0 1015-6.7L3 7"/><polyline points="3,3 3,7 7,7"/><polyline points="12,7 12,12 16,14"/></symbol>
  <symbol id="i-hourglass" viewBox="0 0 24 24"><path d="M6 2h12v4l-5 6 5 6v4H6v-4l5-6-5-6V2z"/></symbol>
  <symbol id="i-eye" viewBox="0 0 24 24"><path d="M1 12s4-7 11-7 11 7 11 7-4 7-11 7-11-7-11-7z"/><circle cx="12" cy="12" r="3"/></symbol>

  <!-- 时间日历 -->
  <symbol id="i-calendar" viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="16" rx="2"/><line x1="3" y1="10" x2="21" y2="10"/><line x1="8" y1="3" x2="8" y2="7"/><line x1="16" y1="3" x2="16" y2="7"/></symbol>
  <symbol id="i-clock" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><polyline points="12,7 12,12 16,14"/></symbol>

  <!-- 文件类型（特殊设计带文字） -->
  <symbol id="i-file" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8l-6-6z"/><polyline points="14,2 14,8 20,8"/></symbol>
  <symbol id="i-file-pdf" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8l-6-6z"/><polyline points="14,2 14,8 20,8"/><text x="7" y="18" font-size="6" font-weight="bold" fill="currentColor" stroke="none">PDF</text></symbol>
  <symbol id="i-file-doc" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8l-6-6z"/><polyline points="14,2 14,8 20,8"/><text x="7" y="18" font-size="6" font-weight="bold" fill="currentColor" stroke="none">DOC</text></symbol>
  <symbol id="i-file-xls" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8l-6-6z"/><polyline points="14,2 14,8 20,8"/><text x="7" y="18" font-size="6" font-weight="bold" fill="currentColor" stroke="none">XLS</text></symbol>
  <symbol id="i-file-ppt" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8l-6-6z"/><polyline points="14,2 14,8 20,8"/><text x="7" y="18" font-size="6" font-weight="bold" fill="currentColor" stroke="none">PPT</text></symbol>
  <symbol id="i-file-img" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8l-6-6z"/><polyline points="14,2 14,8 20,8"/><circle cx="9" cy="14" r="1.5"/><polyline points="7,18 11,15 17,19"/></symbol>

  <!-- Coach 专属 -->
  <symbol id="i-brain" viewBox="0 0 24 24"><path d="M9 3a3 3 0 00-3 3 3 3 0 00-3 3v3a3 3 0 002 3 3 3 0 003 3 3 3 0 003 3V3a3 3 0 00-2 0z"/><path d="M15 3a3 3 0 013 3 3 3 0 013 3v3a3 3 0 01-2 3 3 3 0 01-3 3 3 3 0 01-3 3V3"/></symbol>
  <symbol id="i-map" viewBox="0 0 24 24"><polygon points="1,6 8,3 16,6 23,3 23,18 16,21 8,18 1,21 1,6"/><line x1="8" y1="3" x2="8" y2="18"/><line x1="16" y1="6" x2="16" y2="21"/></symbol>
  <symbol id="i-book" viewBox="0 0 24 24"><path d="M4 19V5a2 2 0 012-2h13v18H6a2 2 0 01-2-2z"/><line x1="9" y1="7" x2="15" y2="7"/><line x1="9" y1="11" x2="15" y2="11"/></symbol>
  <symbol id="i-mic" viewBox="0 0 24 24"><rect x="9" y="3" width="6" height="12" rx="3"/><path d="M5 11a7 7 0 0014 0"/><line x1="12" y1="18" x2="12" y2="22"/><line x1="9" y1="22" x2="15" y2="22"/></symbol>

  <!-- 视图切换 -->
  <symbol id="i-grid" viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></symbol>
  <symbol id="i-list" viewBox="0 0 24 24"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><circle cx="4" cy="6" r="0.8" fill="currentColor"/><circle cx="4" cy="12" r="0.8" fill="currentColor"/><circle cx="4" cy="18" r="0.8" fill="currentColor"/></symbol>

  <!-- 通用 -->
  <symbol id="i-message-circle" viewBox="0 0 24 24"><path d="M21 11.5a8.4 8.4 0 01-1 4 8.5 8.5 0 01-7.5 4.5 8.4 8.4 0 01-4-1L3 21l2-5.5A8.5 8.5 0 0112.5 3 8.5 8.5 0 0121 11.5z"/></symbol>
  <symbol id="i-target" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.5" fill="currentColor"/></symbol>
  <symbol id="i-lightbulb" viewBox="0 0 24 24"><path d="M9 18h6M10 22h4M12 2a7 7 0 00-4 12.7c.7.5 1 1.3 1 2.1V18h6v-1.2c0-.8.3-1.6 1-2.1A7 7 0 0012 2z"/></symbol>
  <symbol id="i-star" viewBox="0 0 24 24"><polygon points="12,2 15,9 22,10 17,15 18,22 12,18 6,22 7,15 2,10 9,9 12,2"/></symbol>
  <symbol id="i-rocket" viewBox="0 0 24 24"><path d="M5 13l-2 8 8-2-6-6z"/><path d="M14 6l4 4-9 9-4-4 9-9z"/><circle cx="16" cy="8" r="1.5"/><path d="M14 6c0-3 3-5 7-5 0 4-2 7-5 7"/></symbol>
</svg>`;

/* 注入 SVG sprite 到页面 */
function injectSvgSprite() {
  const mount = document.getElementById('svg-sprite-mount');
  if (mount) mount.innerHTML = SVG_SPRITE;
  else document.body.insertAdjacentHTML('afterbegin', SVG_SPRITE);
}

/* helper：生成 SVG 引用 HTML */
function icoSvg(id, cls) { return `<svg class="ico ${cls||''}"><use href="#${id}"/></svg>`; }

/* helper：生成助手徽章 HTML */
function badgeHtml(key, letter, size) {
  const sizeCls = size === 'sm' ? 'sm' : (size === 'lg' ? 'lg' : (size === 'xl' ? 'xl' : ''));
  return `<span class="assistant-badge ${key} ${sizeCls}">${letter}</span>`;
}

/* 自动注入 */
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', injectSvgSprite);
} else {
  injectSvgSprite();
}
