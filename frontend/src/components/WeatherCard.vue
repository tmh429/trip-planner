<template>
  <div class="weather-card">
    <div class="weather-date">{{ weather.date }}</div>
    <div class="weather-main">
      <div class="weather-period">
        <span class="period-icon">☀️</span>
        <div class="period-info">
          <span class="period-label">白天</span>
          <span class="period-temp">{{ weather.day_temp }}°</span>
          <span class="period-weather">{{ weather.day_weather }}</span>
        </div>
      </div>
      <div class="weather-divider"></div>
      <div class="weather-period">
        <span class="period-icon">🌙</span>
        <div class="period-info">
          <span class="period-label">夜间</span>
          <span class="period-temp">{{ weather.night_temp }}°</span>
          <span class="period-weather">{{ weather.night_weather }}</span>
        </div>
      </div>
    </div>
    <div class="weather-wind">
      💨 {{ weather.wind_direction }} {{ weather.wind_power }}
    </div>
  </div>
</template>

<script setup lang="ts">
import type { WeatherInfo } from '@/types'

defineProps<{ weather: WeatherInfo }>()
</script>

<style scoped>
.weather-card {
  background: linear-gradient(135deg, #ecfdf5, #ccfbf1);
  border: 1px solid #a7f3d0;
  border-radius: var(--radius-md);
  padding: var(--space-md);
  text-align: center;
  transition: all var(--transition-base);
}

.weather-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.weather-date {
  font-size: 15px;
  font-weight: 700;
  color: #065f46;
  margin-bottom: var(--space-sm);
}

.weather-main {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  justify-content: center;
}

.weather-divider {
  width: 1px;
  height: 40px;
  background: #a7f3d0;
}

.weather-period {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
}

.period-icon {
  font-size: 28px;
}

.period-info {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.period-label {
  font-size: 11px;
  color: var(--color-text-secondary);
}

.period-temp {
  font-size: 20px;
  font-weight: 800;
  color: #065f46;
}

.period-weather {
  font-size: 13px;
  color: var(--color-text-secondary);
}

.weather-wind {
  margin-top: var(--space-sm);
  padding-top: var(--space-sm);
  border-top: 1px solid rgba(6, 95, 70, 0.12);
  font-size: 13px;
  color: #065f46;
}
</style>
