<template>
  <div class="hotel-card">
    <div class="hotel-header">
      <span class="hotel-name">{{ hotel.name }}</span>
      <span class="hotel-rating">⭐ {{ hotel.rating }}</span>
    </div>
    <div class="hotel-details">
      <div class="hotel-detail">
        <span class="detail-icon">📍</span>
        <span>{{ hotel.address }}</span>
      </div>
      <div class="hotel-meta">
        <span class="hotel-tag">{{ hotel.type }}</span>
        <span class="hotel-tag price">{{ hotel.price_range }}</span>
        <span class="hotel-tag">{{ hotel.distance }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Hotel } from '@/types'

defineProps<{ hotel: Hotel }>()
</script>

<style scoped>
.hotel-card {
  background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
  border: 1px solid #bae6fd;
  border-radius: var(--radius-md);
  padding: var(--space-md);
  margin-top: var(--space-md);
}

.hotel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-sm);
}

.hotel-name {
  font-size: 16px;
  font-weight: 700;
  color: #0369a1;
}

.hotel-rating {
  font-size: 14px;
  color: var(--color-warm);
  font-weight: 600;
}

.hotel-details {
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}

.hotel-detail {
  display: flex;
  align-items: center;
  gap: var(--space-xs);
  font-size: 13px;
  color: var(--color-text-secondary);
}

.detail-icon {
  flex-shrink: 0;
}

.hotel-meta {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-xs);
}

.hotel-tag {
  padding: 2px 10px;
  border-radius: var(--radius-full);
  font-size: 12px;
  font-weight: 500;
  background: var(--color-surface);
  color: var(--color-text-secondary);
  border: 1px solid var(--color-border-light);
}

.hotel-tag.price {
  color: var(--color-primary);
  background: var(--color-primary-light);
  border-color: var(--color-primary-100);
  font-weight: 600;
}
</style>
