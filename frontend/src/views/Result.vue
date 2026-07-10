<template>
  <div class="result-page">
    <!-- 顶部工具栏 -->
    <div class="result-toolbar">
      <a-button class="back-btn" size="large" @click="goBack">← 返回首页</a-button>
      <div class="toolbar-right">
        <template v-if="!editMode">
          <a-button @click="toggleEditMode">✏️ 编辑行程</a-button>
        </template>
        <template v-else>
          <a-button type="primary" @click="saveChanges">💾 保存</a-button>
          <a-button @click="cancelEdit">❌ 取消</a-button>
        </template>
        <a-dropdown v-if="!editMode">
          <template #overlay>
            <a-menu>
              <a-menu-item key="image" @click="exportAsImage">📷 导出为图片</a-menu-item>
              <a-menu-item key="pdf" @click="exportAsPDF">📄 导出为PDF</a-menu-item>
            </a-menu>
          </template>
          <a-button>📥 导出 <DownOutlined /></a-button>
        </a-dropdown>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-if="!tripPlan" class="empty-state">
      <span class="empty-icon">🗺️</span>
      <p>暂无旅行计划数据</p>
      <a-button type="primary" @click="goBack">返回首页创建行程</a-button>
    </div>

    <!-- 主内容 -->
    <template v-else>
      <ResultHero :plan="tripPlan" />

      <div class="result-layout">
        <!-- 侧边导航 -->
        <TripSidebar
          :active="activeSection"
          :day-count="tripPlan.days.length"
          @navigate="scrollToSection"
        />

        <!-- 内容区 -->
        <main class="result-main" ref="mainContentRef">
          <!-- 行程概览 -->
          <div id="overview" class="section-anchor">
            <div class="overview-card">
              <div class="card-title">📋 行程概览</div>
              <p class="overview-suggestion">{{ tripPlan.overall_suggestions }}</p>
            </div>
          </div>

          <!-- 预算 -->
          <div id="budget" class="section-anchor">
            <BudgetCard v-if="tripPlan.budget" :budget="tripPlan.budget" />
          </div>

          <!-- 地图 -->
          <div id="map" class="section-anchor">
            <MapPanel :days="tripPlan.days" />
          </div>

          <!-- 每日行程 -->
          <div id="days" class="section-anchor">
            <DayTimeline
              v-for="day in tripPlan.days"
              :key="day.day_index"
              :day="day"
              :edit-mode="editMode"
              :attraction-photos="attractionPhotos"
              @move-attraction="moveAttraction"
              @delete-attraction="deleteAttraction"
            />
          </div>

          <!-- 天气 -->
          <div v-if="tripPlan.weather_info?.length" id="weather" class="section-anchor">
            <div class="card-title">🌤️ 天气信息</div>
            <div class="weather-grid">
              <WeatherCard
                v-for="w in tripPlan.weather_info"
                :key="w.date"
                :weather="w"
              />
            </div>
          </div>
        </main>
      </div>
    </template>

    <a-back-top :visibility-height="300">
      <div class="back-top-btn">↑</div>
    </a-back-top>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import { DownOutlined } from '@ant-design/icons-vue'
import html2canvas from 'html2canvas'
import jsPDF from 'jspdf'
import ResultHero from '@/components/ResultHero.vue'
import BudgetCard from '@/components/BudgetCard.vue'
import MapPanel from '@/components/MapPanel.vue'
import DayTimeline from '@/components/DayTimeline.vue'
import WeatherCard from '@/components/WeatherCard.vue'
import TripSidebar from '@/components/TripSidebar.vue'
import type { TripPlan } from '@/types'

const router = useRouter()
const tripPlan = ref<TripPlan | null>(null)
const editMode = ref(false)
const originalPlan = ref<TripPlan | null>(null)
const attractionPhotos = ref<Record<string, string>>({})
const activeSection = ref('overview')
const mainContentRef = ref<HTMLElement | null>(null)

// ===== 初始化 =====
onMounted(async () => {
  const data = sessionStorage.getItem('tripPlan')
  if (data) {
    tripPlan.value = JSON.parse(data)
    await loadAttractionPhotos()
  }
  window.addEventListener('scroll', handleScrollSpy)
})

onBeforeUnmount(() => {
  window.removeEventListener('scroll', handleScrollSpy)
})

// ===== 滚动监听 =====
const handleScrollSpy = () => {
  const sections = ['overview', 'budget', 'map', 'weather']
  tripPlan.value?.days.forEach((_, i) => sections.push(`day-${i}`))

  for (const id of sections.reverse()) {
    const el = document.getElementById(id)
    if (el) {
      const rect = el.getBoundingClientRect()
      if (rect.top <= 120) {
        activeSection.value = id
        break
      }
    }
  }
}

const scrollToSection = (key: string) => {
  activeSection.value = key
  document.getElementById(key)?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

// ===== 导航 =====
const goBack = () => router.push('/')

// ===== 图片加载 =====
const loadAttractionPhotos = async () => {
  if (!tripPlan.value) return

  const seen = new Set<string>()
  const attractions: { name: string }[] = []
  tripPlan.value.days.forEach((day) => {
    day.attractions.forEach((a) => {
      if (!seen.has(a.name)) {
        seen.add(a.name)
        attractions.push(a)
      }
    })
  })

  for (let i = 0; i < attractions.length; i++) {
    const attr = attractions[i]
    try {
      if (i > 0) await new Promise((r) => setTimeout(r, 300))
      const res = await fetch(
        `${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}/api/poi/photo?name=${encodeURIComponent(attr.name)}`
      )
      const data = await res.json()
      if (data.success && data.data.photo_url) {
        attractionPhotos.value[attr.name] = data.data.photo_url
      }
    } catch (err) {
      console.error(`获取${attr.name}图片失败:`, err)
    }
  }
}

// ===== 编辑模式 =====
const toggleEditMode = () => {
  editMode.value = true
  originalPlan.value = JSON.parse(JSON.stringify(tripPlan.value))
  message.info('进入编辑模式')
}

const saveChanges = () => {
  editMode.value = false
  if (tripPlan.value) {
    sessionStorage.setItem('tripPlan', JSON.stringify(tripPlan.value))
  }
  message.success('修改已保存')
}

const cancelEdit = () => {
  if (originalPlan.value) {
    tripPlan.value = JSON.parse(JSON.stringify(originalPlan.value))
  }
  editMode.value = false
  message.info('已取消编辑')
}

const deleteAttraction = (dayIndex: number, attrIndex: number) => {
  if (!tripPlan.value) return
  const day = tripPlan.value.days[dayIndex]
  if (day.attractions.length <= 1) {
    message.warning('每天至少需要保留一个景点')
    return
  }
  day.attractions.splice(attrIndex, 1)
  message.success('景点已删除')
}

const moveAttraction = (dayIndex: number, attrIndex: number, direction: 'up' | 'down') => {
  if (!tripPlan.value) return
  const day = tripPlan.value.days[dayIndex]
  const arr = day.attractions
  if (direction === 'up' && attrIndex > 0) {
    ;[arr[attrIndex], arr[attrIndex - 1]] = [arr[attrIndex - 1], arr[attrIndex]]
  } else if (direction === 'down' && attrIndex < arr.length - 1) {
    ;[arr[attrIndex], arr[attrIndex + 1]] = [arr[attrIndex + 1], arr[attrIndex]]
  }
}

// ===== 导出 =====
const cloneContentForExport = (): HTMLElement | null => {
  const el = mainContentRef.value
  if (!el) return null
  const clone = document.createElement('div')
  clone.style.width = el.offsetWidth + 'px'
  clone.style.backgroundColor = '#fafbfc'
  clone.style.padding = '24px'
  clone.innerHTML = el.innerHTML

  // 处理地图 canvas
  const mapCanvas = document.querySelector('#amap-container canvas')
  if (mapCanvas) {
    const img = document.createElement('img')
    img.src = (mapCanvas as HTMLCanvasElement).toDataURL('image/png')
    img.style.cssText = 'width:100%;height:420px;object-fit:cover;border-radius:14px;'
    const mapDiv = clone.querySelector('#amap-container')
    if (mapDiv) {
      mapDiv.innerHTML = ''
      mapDiv.appendChild(img)
    }
  }
  return clone
}

const exportAsImage = async () => {
  try {
    message.loading({ content: '正在生成图片...', key: 'export', duration: 0 })
    const container = cloneContentForExport()
    if (!container) throw new Error('未找到内容')
    container.style.position = 'absolute'
    container.style.left = '-9999px'
    document.body.appendChild(container)

    const canvas = await html2canvas(container, {
      backgroundColor: '#fafbfc',
      scale: 2,
      logging: false,
      useCORS: true,
      allowTaint: true,
    })
    document.body.removeChild(container)

    const link = document.createElement('a')
    link.download = `旅行计划_${tripPlan.value?.city}_${Date.now()}.png`
    link.href = canvas.toDataURL('image/png')
    link.click()
    message.success({ content: '导出成功！', key: 'export' })
  } catch (err: any) {
    message.error({ content: `导出失败: ${err.message}`, key: 'export' })
  }
}

const exportAsPDF = async () => {
  try {
    message.loading({ content: '正在生成PDF...', key: 'export', duration: 0 })
    const container = cloneContentForExport()
    if (!container) throw new Error('未找到内容')
    container.style.position = 'absolute'
    container.style.left = '-9999px'
    document.body.appendChild(container)

    const canvas = await html2canvas(container, {
      backgroundColor: '#fafbfc',
      scale: 2,
      logging: false,
      useCORS: true,
      allowTaint: true,
    })
    document.body.removeChild(container)

    const imgData = canvas.toDataURL('image/png')
    const pdf = new jsPDF({ orientation: 'portrait', unit: 'mm', format: 'a4' })
    const imgWidth = 210
    const imgHeight = (canvas.height * imgWidth) / canvas.width
    let heightLeft = imgHeight
    let position = 0

    pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight)
    heightLeft -= 297
    while (heightLeft > 0) {
      position = heightLeft - imgHeight
      pdf.addPage()
      pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight)
      heightLeft -= 297
    }
    pdf.save(`旅行计划_${tripPlan.value?.city}_${Date.now()}.pdf`)
    message.success({ content: '导出成功！', key: 'export' })
  } catch (err: any) {
    message.error({ content: `导出失败: ${err.message}`, key: 'export' })
  }
}
</script>

<style scoped>
.result-page {
  min-height: 100vh;
  background: var(--color-bg);
  padding-bottom: var(--space-3xl);
}

/* ===== 工具栏 ===== */
.result-toolbar {
  max-width: 1400px;
  margin: 0 auto;
  padding: var(--space-md) var(--space-xl);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.back-btn {
  border-radius: var(--radius-sm);
  font-weight: 500;
}

.toolbar-right {
  display: flex;
  gap: var(--space-sm);
}

/* ===== 空状态 ===== */
.empty-state {
  text-align: center;
  padding: 100px var(--space-xl);
}

.empty-icon {
  font-size: 80px;
  display: block;
  margin-bottom: var(--space-md);
}

.empty-state p {
  font-size: 16px;
  color: var(--color-text-secondary);
  margin-bottom: var(--space-lg);
}

/* ===== 内容布局 ===== */
.result-layout {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 var(--space-xl);
  display: flex;
  gap: var(--space-xl);
  align-items: flex-start;
}

.result-main {
  flex: 1;
  min-width: 0;
}

.section-anchor {
  scroll-margin-top: 80px;
}

/* ===== 卡片公用 ===== */
.overview-card {
  background: var(--color-surface);
  border-radius: var(--radius-md);
  padding: var(--space-lg);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--color-border-light);
  margin-bottom: var(--space-lg);
}

.card-title {
  font-size: 17px;
  font-weight: 700;
  color: var(--color-text);
  margin-bottom: var(--space-md);
}

.overview-suggestion {
  font-size: 15px;
  color: var(--color-text-secondary);
  line-height: 1.8;
  margin: 0;
}

/* ===== 天气网格 ===== */
.weather-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-md);
  margin-bottom: var(--space-lg);
}

/* ===== 回到顶部 ===== */
.back-top-btn {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--color-primary), var(--color-warm));
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: 700;
  box-shadow: var(--shadow-md);
  cursor: pointer;
  transition: all var(--transition-base);
}

.back-top-btn:hover {
  transform: scale(1.1);
}

/* ===== 响应式 ===== */
@media (max-width: 768px) {
  .result-layout {
    flex-direction: column;
    padding: 0 var(--space-md);
  }

  .result-toolbar {
    flex-direction: column;
    gap: var(--space-sm);
    padding: var(--space-md);
  }

  .toolbar-right {
    width: 100%;
    justify-content: flex-end;
  }

  .weather-grid {
    grid-template-columns: 1fr;
  }
}
</style>
