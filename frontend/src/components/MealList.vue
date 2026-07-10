<template>
  <div class="meal-list">
    <div class="meal-title">🍽️ 餐饮安排</div>
    <div class="meal-items">
      <div v-for="meal in meals" :key="meal.type" class="meal-item">
        <span class="meal-type">{{ mealTypeLabel(meal.type) }}</span>
        <span class="meal-name">{{ meal.name }}</span>
        <span v-if="meal.description" class="meal-desc">{{ meal.description }}</span>
        <span v-if="meal.estimated_cost" class="meal-cost">¥{{ meal.estimated_cost }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Meal } from '@/types'

defineProps<{ meals: Meal[] }>()

const mealTypeLabel = (type: string): string => {
  const labels: Record<string, string> = {
    breakfast: '🥐 早餐',
    lunch: '🍱 午餐',
    dinner: '🍲 晚餐',
    snack: '🍿 小吃',
  }
  return labels[type] || type
}
</script>

<style scoped>
.meal-list {
  margin-top: var(--space-md);
}

.meal-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--color-text);
  margin-bottom: var(--space-sm);
}

.meal-items {
  display: flex;
  flex-direction: column;
  gap: var(--space-xs);
}

.meal-item {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-sm) var(--space-md);
  background: var(--color-bg);
  border-radius: var(--radius-sm);
  font-size: 14px;
}

.meal-type {
  font-weight: 600;
  color: var(--color-text);
  white-space: nowrap;
  min-width: 70px;
}

.meal-name {
  color: var(--color-text);
  flex: 1;
}

.meal-desc {
  color: var(--color-text-muted);
  font-size: 13px;
}

.meal-cost {
  font-weight: 600;
  color: var(--color-primary);
  white-space: nowrap;
}
</style>
