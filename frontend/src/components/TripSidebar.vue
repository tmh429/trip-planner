<template>
  <nav class="trip-sidebar">
    <a
      v-for="section in sections"
      :key="section.key"
      :href="`#${section.key}`"
      class="sidebar-item"
      :class="{ active: active === section.key }"
      @click.prevent="$emit('navigate', section.key)"
    >
      <span class="sidebar-dot"></span>
      <span class="sidebar-label">{{ section.label }}</span>
    </a>
    <!-- 子导航：每天行程 -->
    <template v-if="dayCount > 0">
      <a
        v-for="i in dayCount"
        :key="`day-${i - 1}`"
        :href="`#day-${i - 1}`"
        class="sidebar-item sidebar-sub"
        :class="{ active: active === `day-${i - 1}` }"
        @click.prevent="$emit('navigate', `day-${i - 1}`)"
      >
        <span class="sidebar-dot small"></span>
        <span class="sidebar-label">第{{ i }}天</span>
      </a>
    </template>
  </nav>
</template>

<script setup lang="ts">
defineProps<{
  active: string
  dayCount: number
}>()

defineEmits<{
  navigate: [key: string]
}>()

const sections = [
  { key: 'overview', label: '📋 行程概览' },
  { key: 'budget', label: '💰 预算明细' },
  { key: 'map', label: '📍 景点地图' },
  { key: 'weather', label: '🌤️ 天气信息' },
]
</script>

<style scoped>
.trip-sidebar {
  position: sticky;
  top: 80px;
  display: flex;
  flex-direction: column;
  gap: 2px;
  background: var(--color-surface);
  border-radius: var(--radius-md);
  padding: var(--space-sm);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--color-border-light);
  min-width: 160px;
}

.sidebar-item {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: 8px 12px;
  border-radius: var(--radius-sm);
  text-decoration: none;
  color: var(--color-text-secondary);
  font-size: 13px;
  font-weight: 500;
  transition: all var(--transition-fast);
}

.sidebar-item:hover {
  background: var(--color-bg);
  color: var(--color-text);
}

.sidebar-item.active {
  background: var(--color-primary-light);
  color: var(--color-primary);
}

.sidebar-sub {
  padding-left: 24px;
}

.sidebar-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--color-border);
  transition: all var(--transition-fast);
  flex-shrink: 0;
}

.sidebar-dot.small {
  width: 5px;
  height: 5px;
}

.sidebar-item.active .sidebar-dot {
  background: var(--color-primary);
  box-shadow: 0 0 0 3px var(--color-primary-100);
}

.sidebar-label {
  white-space: nowrap;
}

@media (max-width: 768px) {
  .trip-sidebar {
    display: none;
  }
}
</style>
