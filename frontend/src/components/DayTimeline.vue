<template>
  <div :id="`day-${day.day_index}`" class="day-section">
    <!-- 日期标签 -->
    <div class="day-header">
      <div class="day-marker">
        <div class="marker-line"></div>
        <div class="marker-dot"></div>
      </div>
      <div class="day-info">
        <h3 class="day-title">第{{ day.day_index + 1 }}天</h3>
        <span class="day-date">{{ day.date }}</span>
      </div>
      <div class="day-meta">
        <span class="meta-tag">{{ day.transportation }}</span>
        <span class="meta-tag">{{ day.accommodation }}</span>
      </div>
    </div>

    <p class="day-desc">{{ day.description }}</p>

    <!-- 景点卡片网格 -->
    <div class="attractions-grid">
      <AttractionCard
        v-for="(attraction, idx) in day.attractions"
        :key="idx"
        :attraction="attraction"
        :index="idx"
        :edit-mode="editMode"
        :photo-url="attractionPhotos[attraction.name] || ''"
      />
    </div>

    <!-- 操作按钮(编辑模式) -->
    <div v-if="editMode && day.attractions.length > 1" class="edit-actions">
      <a-button
        v-for="(_item, idx) in day.attractions"
        :key="'btn-' + idx"
        size="small"
        @click="$emit('move-attraction', day.day_index, idx, 'up')"
        :disabled="idx === 0"
      >↑ 上移</a-button>
      <a-button
        v-for="(_item, idx) in day.attractions"
        :key="'del-' + idx"
        size="small"
        danger
        @click="$emit('delete-attraction', day.day_index, idx)"
        :disabled="day.attractions.length <= 1"
      >🗑️</a-button>
    </div>

    <!-- 酒店 -->
    <HotelCard v-if="day.hotel" :hotel="day.hotel" />

    <!-- 餐饮 -->
    <MealList :meals="day.meals" />
  </div>
</template>

<script setup lang="ts">
import type { DayPlan } from '@/types'
import AttractionCard from './AttractionCard.vue'
import HotelCard from './HotelCard.vue'
import MealList from './MealList.vue'

defineProps<{
  day: DayPlan
  editMode: boolean
  attractionPhotos: Record<string, string>
}>()

defineEmits<{
  'move-attraction': [dayIndex: number, attrIndex: number, direction: 'up' | 'down']
  'delete-attraction': [dayIndex: number, attrIndex: number]
}>()
</script>

<style scoped>
.day-section {
  position: relative;
  padding-left: 48px;
  margin-bottom: var(--space-xl);
}

/* 时间线 */
.day-header {
  display: flex;
  align-items: flex-start;
  gap: var(--space-md);
  margin-bottom: var(--space-sm);
}

.day-marker {
  position: absolute;
  left: 12px;
  top: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.marker-line {
  width: 2px;
  flex: 1;
  background: var(--color-border);
  margin: 8px 0;
}

.day-section:last-child .marker-line {
  display: none;
}

.marker-dot {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: var(--color-primary);
  border: 3px solid var(--color-primary-100);
  box-shadow: 0 0 0 4px var(--color-surface);
  flex-shrink: 0;
  margin-top: 4px;
}

.day-info {
  flex: 1;
}

.day-title {
  font-size: 20px;
  font-weight: 700;
  color: var(--color-text);
  margin: 0;
}

.day-date {
  font-size: 13px;
  color: var(--color-text-muted);
}

.day-meta {
  display: flex;
  gap: var(--space-xs);
}

.meta-tag {
  padding: 4px 12px;
  border-radius: var(--radius-full);
  background: var(--color-primary-light);
  color: var(--color-primary);
  font-size: 12px;
  font-weight: 500;
}

.day-desc {
  font-size: 14px;
  color: var(--color-text-secondary);
  margin: 0 0 var(--space-md);
  line-height: 1.6;
}

/* 景点网格 */
.attractions-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--space-md);
}

.edit-actions {
  display: flex;
  gap: var(--space-sm);
  margin-top: var(--space-sm);
  flex-wrap: wrap;
}

@media (max-width: 768px) {
  .day-section {
    padding-left: 32px;
  }

  .attractions-grid {
    grid-template-columns: 1fr;
  }

  .day-marker {
    left: 6px;
  }
}
</style>
