<script setup lang="ts">
</script>

<template>
  <div class="not-found-page">
    <div class="not-found-content">
      <h1>404</h1>
      <p>页面未找到</p>
      <router-link to="/dashboard">返回首页</router-link>
    </div>
  </div>
</template>

<style scoped>
.not-found-page {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
}

.not-found-content {
  text-align: center;
}

.not-found-content h1 {
  font-size: 120px;
  color: var(--color-text-secondary);
}

.not-found-content p {
  font-size: 24px;
  margin-bottom: 24px;
}

.not-found-content a {
  font-size: 16px;
}
</style>