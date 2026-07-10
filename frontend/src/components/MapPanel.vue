<template>
  <div class="map-panel">
    <div class="map-header">📍 景点地图</div>
    <div id="amap-container" ref="mapContainer" class="map-container"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, nextTick, watch } from 'vue'
import AMapLoader from '@amap/amap-jsapi-loader'
import type { DayPlan } from '@/types'

const props = defineProps<{
  days: DayPlan[]
}>()

const mapContainer = ref<HTMLElement | null>(null)
let map: any = null
let markers: any[] = []

interface AttractionWithDay {
  name: string
  address: string
  location: { longitude: number; latitude: number }
  visit_duration: number
  description: string
  dayIndex: number
  attrIndex: number
}

onMounted(async () => {
  await nextTick()
  await initMap()
})

onBeforeUnmount(() => {
  if (map) {
    map.destroy()
    map = null
  }
})

// 当 days 变化时重建地图（编辑模式下可能添加/删除景点）
watch(() => props.days, async () => {
  if (map) {
    map.clearMap()
    markers = []
    addMarkers()
  }
}, { deep: true })

const initMap = async () => {
  if (!mapContainer.value) return

  try {
    const AMap = await AMapLoader.load({
      key: import.meta.env.VITE_AMAP_WEB_JS_KEY,
      version: '2.0',
      plugins: ['AMap.Marker', 'AMap.Polyline', 'AMap.InfoWindow'],
    })

    map = new AMap.Map('amap-container', {
      zoom: 12,
      center: [116.397128, 39.916527],
      viewMode: '3D',
    })

    addMarkers()
  } catch (error) {
    console.error('地图加载失败:', error)
  }
}

const collectAttractions = (): AttractionWithDay[] => {
  const result: AttractionWithDay[] = []
  props.days.forEach((day, dayIndex) => {
    day.attractions.forEach((attraction, attrIndex) => {
      if (attraction.location?.longitude && attraction.location?.latitude) {
        result.push({ ...attraction, dayIndex, attrIndex } as AttractionWithDay)
      }
    })
  })
  return result
}

const addMarkers = () => {
  if (!map || !window.AMap) return

  const attractions = collectAttractions()
  if (attractions.length === 0) return

  const AMap = (window as any).AMap

  // 创建标记
  attractions.forEach((attraction, index) => {
    const marker = new AMap.Marker({
      position: [attraction.location.longitude, attraction.location.latitude],
      title: attraction.name,
      label: {
        content: `<div style="background:var(--color-primary, #f97316);color:#fff;padding:3px 8px;border-radius:12px;font-size:12px;font-weight:700;">${index + 1}</div>`,
        offset: new AMap.Pixel(0, -30),
      },
    })

    const infoWindow = new AMap.InfoWindow({
      content: `
        <div style="padding:8px;min-width:160px;">
          <h4 style="margin:0 0 6px;color:#1e293b;">${attraction.name}</h4>
          <p style="margin:2px 0;font-size:12px;color:#64748b;">📍 ${attraction.address}</p>
          <p style="margin:2px 0;font-size:12px;color:#64748b;">⏱️ ${attraction.visit_duration}分钟</p>
          <p style="margin:2px 0;font-size:12px;color:#f97316;font-weight:600;">第${attraction.dayIndex + 1}天 · 景点${attraction.attrIndex + 1}</p>
        </div>
      `,
      offset: new AMap.Pixel(0, -30),
    })

    marker.on('click', () => {
      infoWindow.open(map, marker.getPosition())
    })

    map.add(marker)
    markers.push(marker)
  })

  // 自动适配视野
  map.setFitView(markers)

  // 绘制路线
  drawRoutes(attractions, AMap)
}

const drawRoutes = (attractions: AttractionWithDay[], AMap: any) => {
  // 按天分组
  const dayGroups: Record<number, AttractionWithDay[]> = {}
  attractions.forEach((a) => {
    if (!dayGroups[a.dayIndex]) dayGroups[a.dayIndex] = []
    dayGroups[a.dayIndex].push(a)
  })

  Object.values(dayGroups).forEach((group) => {
    if (group.length < 2) return
    const path = group.map((a) => [a.location.longitude, a.location.latitude])
    const polyline = new AMap.Polyline({
      path,
      strokeColor: '#f97316',
      strokeWeight: 3,
      strokeOpacity: 0.7,
      strokeStyle: 'dashed',
      showDir: true,
    })
    map.add(polyline)
  })
}
</script>

<style scoped>
.map-panel {
  background: var(--color-surface);
  border-radius: var(--radius-md);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--color-border-light);
  margin-bottom: var(--space-lg);
}

.map-header {
  padding: var(--space-md) var(--space-lg);
  font-size: 17px;
  font-weight: 700;
  color: var(--color-text);
  border-bottom: 1px solid var(--color-border-light);
}

.map-container {
  width: 100%;
  height: 420px;
}
</style>
