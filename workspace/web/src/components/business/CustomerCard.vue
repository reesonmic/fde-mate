<script setup lang="ts">
import { Card } from 'ant-design-vue'
import type { CustomerDTO } from '@/types/business'

interface Props {
  customer: CustomerDTO
  selected?: boolean
}

withDefaults(defineProps<Props>(), {
  selected: false,
})
</script>

<template>
  <div class="customer-card" :class="{ 'customer-card--selected': selected }">
    <Card hoverable>
      <div class="customer-card-header">
        <h4>{{ customer.name }}</h4>
      </div>
      <div class="customer-card-info">
        <span v-if="customer.industry" class="info-item">行业: {{ customer.industry }}</span>
        <span v-if="customer.scale" class="info-item">规模: {{ customer.scale }}</span>
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