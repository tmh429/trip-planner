<template>
  <div class="attraction-card" :class="{ 'edit-mode': editMode }">
    <!-- 图片区域 -->
    <div class="attr-image-wrapper">
      <img
        :src="photoSrc"
        :alt="attraction.name"
        class="attr-image"
        @error="handleImageError"
      />
      <div class="attr-badge">
        <span class="badge-num">{{ index + 1 }}</span>
      </div>
      <div v-if="attraction.ticket_price" class="attr-price">
        ¥{{ attraction.ticket_price }}
      </div>
      <div v-if="attraction.category" class="attr-category">
        {{ attraction.category }}
      </div>
    </div>

    <!-- 信息区域 -->
    <div class="attr-body">
      <h4 class="attr-name">{{ attraction.name }}</h4>

      <template v-if="editMode">
        <div class="attr-field">
          <label>地址</label>
          <a-input v-model:value="attraction.address" size="small" />
        </div>
        <div class="attr-field">
          <label>游览时长 (分钟)</label>
          <a-input-number v-model:value="attraction.visit_duration" :min="10" :max="480" size="small" style="width: 100%" />
        </div>
        <div class="attr-field">
          <label>描述</label>
          <a-textarea v-model:value="attraction.description" :rows="2" size="small" />
        </div>
      </template>
      <template v-else>
        <p class="attr-address">📍 {{ attraction.address }}</p>
        <p class="attr-duration">⏱️ {{ attraction.visit_duration }} 分钟</p>
        <p class="attr-desc">{{ attraction.description }}</p>
        <p v-if="attraction.rating" class="attr-rating">⭐ {{ attraction.rating }}</p>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import type { Attraction } from '@/types'

const props = defineProps<{
  attraction: Attraction
  index: number
  editMode: boolean
  photoUrl: string
}>()

const imageError = ref(false)

const photoSrc = computed(() => {
  if (props.photoUrl && !imageError.value) return props.photoUrl
  // 占位渐变图
  const colors = [
    { start: '#f97316', end: '#f59e0b' },
    { start: '#14b8a6', end: '#0ea5e9' },
    { start: '#8b5cf6', end: '#ec4899' },
    { start: '#06b6d4', end: '#10b981' },
    { start: '#f43f5e', end: '#f97316' },
  ]
  const c = colors[props.index % colors.length]
  return `data:image/svg+xml,${encodeURIComponent(`<svg xmlns="http://www.w3.org/2000/svg" width="400" height="240"><defs><linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:${c.start}"/><stop offset="100%" style="stop-color:${c.end}"/></linearGradient></defs><rect width="400" height="240" fill="url(#g)"/><text x="200" y="120" dominant-baseline="middle" text-anchor="middle" font-family="sans-serif" font-size="22" font-weight="bold" fill="white" fill-opacity="0.9">${props.attraction.name}</text></svg>`)}`
})

const handleImageError = () => {
  imageError.value = true
}
</script>

<style scoped>
.attraction-card {
  background: var(--color-surface);
  border-radius: var(--radius-md);
  overflow: hidden;
  border: 1px solid var(--color-border-light);
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-base);
}

.attraction-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.attr-image-wrapper {
  position: relative;
  overflow: hidden;
}

.attr-image {
  width: 100%;
  height: 180px;
  object-fit: cover;
  transition: transform var(--transition-slow);
}

.attraction-card:hover .attr-image {
  transform: scale(1.05);
}

.attr-badge {
  position: absolute;
  top: 10px;
  left: 10px;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--color-primary);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 16px;
  box-shadow: var(--shadow-md);
}

.attr-price {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 4px 12px;
  border-radius: var(--radius-full);
  background: rgba(0,0,0,0.6);
  color: #fff;
  font-weight: 700;
  font-size: 13px;
  backdrop-filter: blur(8px);
}

.attr-category {
  position: absolute;
  bottom: 10px;
  left: 10px;
  padding: 2px 10px;
  border-radius: var(--radius-full);
  background: rgba(255,255,255,0.9);
  color: var(--color-text-secondary);
  font-size: 11px;
  font-weight: 500;
  backdrop-filter: blur(8px);
}

.attr-body {
  padding: var(--space-md);
}

.attr-name {
  font-size: 16px;
  font-weight: 700;
  color: var(--color-text);
  margin: 0 0 var(--space-sm);
}

.attr-address,
.attr-duration,
.attr-desc {
  font-size: 13px;
  color: var(--color-text-secondary);
  margin: 4px 0;
}

.attr-rating {
  font-size: 13px;
  color: var(--color-warm);
  font-weight: 600;
  margin: 4px 0;
}

.attr-field {
  margin-bottom: var(--space-sm);
}

.attr-field label {
  display: block;
  font-size: 12px;
  font-weight: 600;
  color: var(--color-text-secondary);
  margin-bottom: 2px;
}
</style>
