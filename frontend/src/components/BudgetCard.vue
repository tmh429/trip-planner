<template>
  <div class="budget-card-wrapper" v-if="budget">
    <div class="budget-title">💰 预算明细</div>
    <div class="budget-grid">
      <div class="budget-item" v-for="item in budgetItems" :key="item.label">
        <div class="budget-item-icon" :style="{ background: item.color }">{{ item.icon }}</div>
        <div class="budget-item-info">
          <span class="budget-item-label">{{ item.label }}</span>
          <span class="budget-item-value">¥{{ item.value.toLocaleString() }}</span>
        </div>
      </div>
    </div>
    <div class="budget-total">
      <span>预估总费用</span>
      <span class="budget-total-value">¥{{ budget.total.toLocaleString() }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Budget } from '@/types'

const props = defineProps<{ budget: Budget }>()

const budgetItems = computed(() => [
  { label: '景点门票', value: props.budget.total_attractions, icon: '🎫', color: 'var(--color-primary-100)' },
  { label: '酒店住宿', value: props.budget.total_hotels, icon: '🏨', color: '#e0f2fe' },
  { label: '餐饮费用', value: props.budget.total_meals, icon: '🍽️', color: 'var(--color-warm-light)' },
  { label: '交通费用', value: props.budget.total_transportation, icon: '🚗', color: 'var(--color-accent-light)' },
])
</script>

<style scoped>
.budget-card-wrapper {
  background: var(--color-surface);
  border-radius: var(--radius-md);
  padding: var(--space-lg);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--color-border-light);
  margin-bottom: var(--space-lg);
}

.budget-title {
  font-size: 17px;
  font-weight: 700;
  color: var(--color-text);
  margin-bottom: var(--space-md);
}

.budget-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-md);
  margin-bottom: var(--space-md);
}

.budget-item {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-sm);
}

.budget-item-icon {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
}

.budget-item-info {
  display: flex;
  flex-direction: column;
}

.budget-item-label {
  font-size: 12px;
  color: var(--color-text-secondary);
}

.budget-item-value {
  font-size: 16px;
  font-weight: 700;
  color: var(--color-text);
}

.budget-total {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-md);
  background: linear-gradient(135deg, var(--color-primary-100), var(--color-warm-light));
  border-radius: var(--radius-sm);
  font-weight: 600;
  color: var(--color-text);
}

.budget-total-value {
  font-size: 24px;
  font-weight: 800;
  background: linear-gradient(135deg, var(--color-primary), var(--color-warm));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

@media (max-width: 768px) {
  .budget-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
