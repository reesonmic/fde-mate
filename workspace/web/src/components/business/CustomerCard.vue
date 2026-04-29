<script setup lang="ts">
import { computed } from 'vue'
import { Card } from 'ant-design-vue'
import HealthRing from '@/components/common/HealthRing.vue'
import StatusDot from '@/components/common/StatusDot.vue'
import type { CustomerDTO } from '@/types/api'

interface Props {
  customer: CustomerDTO
}

const props = defineProps<Props>()

const healthValue = computed(() => {
  return props.customer.healthScore || 0
})

const healthColor = computed(() => {
  if (healthValue.value >= 80) return 'green'
  if (healthValue.value >= 50) return 'yellow'
  return 'red'
})
</script>

<template>
  <div class="customer-card">
    <Card>
      <div class="customer-card-header">
        <h4>{{ customer.name }}</h4>
        <StatusDot status="info" />
      </div>
      <div class="customer-card-health">
        <HealthRing :value="healthValue" :color="healthColor" size="small" />
        <span class="customer-card-health-label">健康度</span>
      </div>
      <div class="customer-card-info">
        <p>{{ customer.description || '暂无描述' }}</p>
      </div>
    </Card>
  </div>
</template>

<style scoped>
.customer-card {
  cursor: pointer;
}

.customer-card:hover {
  box-shadow: var(--shadow-lg);
}

.customer-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.customer-card-header h4 {
  margin: 0;
  font-size: 16px;
}

.customer-card-health {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.customer-card-health-label {
  font-size: 12px;
  color: var(--color-text-secondary);
}

.customer-card-info p {
  margin: 0;
  font-size: 14px;
  color: var(--color-text-secondary);
}
</style>