<template>
  <div class="result-hero">
    <div class="hero-bg"></div>
    <div class="hero-content">
      <h1 class="hero-city">{{ plan.city }}</h1>
      <p class="hero-dates">{{ plan.start_date }} — {{ plan.end_date }} · {{ plan.days.length }} 天行程</p>
      <p v-if="plan.overall_suggestions" class="hero-suggestion">{{ plan.overall_suggestions }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { TripPlan } from '@/types'

defineProps<{ plan: TripPlan }>()
</script>

<style scoped>
.result-hero {
  position: relative;
  height: 240px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  margin-bottom: var(--space-lg);
}

.hero-bg {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, var(--color-primary-600), var(--color-warm), var(--color-accent-500));
  opacity: 0.92;
}

.hero-bg::after {
  content: '';
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle at 20% 50%, rgba(255,255,255,0.15) 0%, transparent 50%),
    radial-gradient(circle at 80% 50%, rgba(255,255,255,0.1) 0%, transparent 50%);
}

.hero-content {
  position: relative;
  text-align: center;
  color: #fff;
  padding: 0 var(--space-xl);
}

.hero-city {
  font-size: 42px;
  font-weight: 800;
  margin: 0 0 var(--space-sm);
  letter-spacing: 2px;
  text-shadow: 0 2px 12px rgba(0,0,0,0.2);
}

.hero-dates {
  font-size: 16px;
  opacity: 0.9;
  margin: 0 0 var(--space-sm);
  font-weight: 500;
}

.hero-suggestion {
  font-size: 14px;
  opacity: 0.75;
  margin: 0;
  max-width: 600px;
}
</style>
