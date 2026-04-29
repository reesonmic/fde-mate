<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useUiStore } from '@stores/ui'
import AppHeader from './AppHeader.vue'
import AppNav from './AppNav.vue'
import CopilotPanel from '@components/copilot/CopilotPanel.vue'

const route = useRoute()
const ui = useUiStore()

const showCopilot = computed(() => ui.copilotOpen && route.meta.layout !== 'chat-only')
const copilotKey = computed(() => (route.meta.copilot as string) || 'workspace')
</script>

<template>
  <div class="app-layout" :class="{ 'no-copilot': !showCopilot }">
    <AppHeader class="app-header" />
    <AppNav class="app-nav" />
    <main class="app-main">
      <RouterView />
    </main>
    <CopilotPanel v-if="showCopilot" :assistant-key="copilotKey" class="app-copilot" />
  </div>
</template>

<style scoped>
.app-layout {
  display: grid;
  grid-template-columns: 220px 1fr 380px;
  grid-template-rows: 56px 1fr;
  grid-template-areas:
    'header header header'
    'nav main copilot';
  height: 100vh;
}
.app-header { grid-area: header; }
.app-nav { grid-area: nav; }
.app-main { grid-area: main; overflow: auto; padding: 16px; }
.app-copilot { grid-area: copilot; border-left: 1px solid var(--border-color); }

.app-layout.no-copilot {
  grid-template-columns: 220px 1fr;
  grid-template-areas: 'header header' 'nav main';
}
</style>
