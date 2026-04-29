<script setup lang="ts">
interface Props {
  rows?: number
  width?: string | number
}

const props = withDefaults(defineProps<Props>(), {
  rows: 1,
  width: '100%',
})
</script>

<template>
  <div class="loading-shimmer">
    <div
      v-for="i in rows"
      :key="i"
      class="loading-shimmer-row"
      :style="{ width: typeof width === 'number' ? `${width}px` : width }"
    />
  </div>
</template>

<style scoped>
.loading-shimmer {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.loading-shimmer-row {
  height: 16px;
  background: linear-gradient(
    90deg,
    var(--color-fill-secondary) 25%,
    var(--color-fill) 50%,
    var(--color-fill-secondary) 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 4px;
}

@keyframes shimmer {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}
</style>