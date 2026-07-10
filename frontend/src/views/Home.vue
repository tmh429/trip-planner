<template>
  <div class="home-page">
    <!-- Hero 区域 -->
    <section class="hero">
      <div class="hero-decoration">
        <div class="float-icon" style="top:10%;left:10%;animation-delay:0s">🏖️</div>
        <div class="float-icon" style="top:20%;right:15%;animation-delay:2s">🗺️</div>
        <div class="float-icon" style="bottom:30%;left:20%;animation-delay:4s">🎒</div>
        <div class="float-icon" style="bottom:20%;right:10%;animation-delay:1s">✈️</div>
      </div>
      <div class="hero-content">
        <h1 class="hero-title">规划你的完美旅程</h1>
        <p class="hero-subtitle">AI 驱动的个性化旅行助手，几分钟生成专属旅行计划</p>
      </div>
    </section>

    <!-- 表单区域 -->
    <section class="form-section">
      <div class="form-card">
        <a-form :model="formData" layout="vertical" @finish="handleSubmit" class="trip-form">

          <!-- 第一步：目的地与日期 -->
          <div class="form-block">
            <div class="block-header">
              <span class="block-icon">📍</span>
              <span class="block-title">目的地与日期</span>
            </div>
            <a-row :gutter="20">
              <a-col :span="6">
                <a-form-item name="city" :rules="[{ required: true, message: '请输入目的地城市' }]">
                  <template #label><span class="input-label">目的地城市</span></template>
                  <a-input v-model:value="formData.city" placeholder="例如：北京" size="large">
                    <template #prefix>🏙️</template>
                  </a-input>
                </a-form-item>
              </a-col>
              <a-col :span="6">
                <a-form-item name="start_date" :rules="[{ required: true, message: '请选择开始日期' }]">
                  <template #label><span class="input-label">开始日期</span></template>
                  <a-date-picker v-model:value="formData.start_date" style="width:100%" size="large" placeholder="选择日期" />
                </a-form-item>
              </a-col>
              <a-col :span="6">
                <a-form-item name="end_date" :rules="[{ required: true, message: '请选择结束日期' }]">
                  <template #label><span class="input-label">结束日期</span></template>
                  <a-date-picker v-model:value="formData.end_date" style="width:100%" size="large" placeholder="选择日期" />
                </a-form-item>
              </a-col>
              <a-col :span="6">
                <a-form-item>
                  <template #label><span class="input-label">旅行天数</span></template>
                  <div class="days-pill">
                    <span class="days-num" :class="{ bounce: daysBounce }">{{ formData.travel_days }}</span>
                    <span class="days-unit">天</span>
                  </div>
                </a-form-item>
              </a-col>
            </a-row>
          </div>

          <!-- 第二步：偏好设置 -->
          <div class="form-block">
            <div class="block-header">
              <span class="block-icon">⚙️</span>
              <span class="block-title">偏好设置</span>
            </div>
            <a-row :gutter="20">
              <a-col :span="8">
                <a-form-item name="transportation">
                  <template #label><span class="input-label">交通方式</span></template>
                  <a-select v-model:value="formData.transportation" size="large">
                    <a-select-option value="公共交通">🚇 公共交通</a-select-option>
                    <a-select-option value="自驾">🚗 自驾</a-select-option>
                    <a-select-option value="步行">🚶 步行</a-select-option>
                    <a-select-option value="混合">🔀 混合</a-select-option>
                  </a-select>
                </a-form-item>
              </a-col>
              <a-col :span="8">
                <a-form-item name="accommodation">
                  <template #label><span class="input-label">住宿偏好</span></template>
                  <a-select v-model:value="formData.accommodation" size="large">
                    <a-select-option value="经济型酒店">💰 经济型酒店</a-select-option>
                    <a-select-option value="舒适型酒店">🏨 舒适型酒店</a-select-option>
                    <a-select-option value="豪华酒店">⭐ 豪华酒店</a-select-option>
                    <a-select-option value="民宿">🏡 民宿</a-select-option>
                  </a-select>
                </a-form-item>
              </a-col>
              <a-col :span="8">
                <a-form-item name="preferences">
                  <template #label><span class="input-label">旅行偏好</span></template>
                  <a-checkbox-group v-model:value="formData.preferences" class="pref-group">
                    <a-checkbox value="历史文化" class="pref-chip">🏛️ 历史文化</a-checkbox>
                    <a-checkbox value="自然风光" class="pref-chip">🏞️ 自然风光</a-checkbox>
                    <a-checkbox value="美食" class="pref-chip">🍜 美食</a-checkbox>
                    <a-checkbox value="购物" class="pref-chip">🛍️ 购物</a-checkbox>
                    <a-checkbox value="艺术" class="pref-chip">🎨 艺术</a-checkbox>
                    <a-checkbox value="休闲" class="pref-chip">☕ 休闲</a-checkbox>
                  </a-checkbox-group>
                </a-form-item>
              </a-col>
            </a-row>
          </div>

          <!-- 第三步：额外要求 -->
          <div class="form-block">
            <div class="block-header">
              <span class="block-icon">💬</span>
              <span class="block-title">额外要求</span>
            </div>
            <a-form-item name="free_text_input">
              <a-textarea
                v-model:value="formData.free_text_input"
                placeholder="例如：想去看升旗、需要无障碍设施、对海鲜过敏..."
                :rows="3"
                size="large"
              />
            </a-form-item>
          </div>

          <!-- 提交按钮 -->
          <a-form-item>
            <a-button
              type="primary"
              html-type="submit"
              :loading="loading"
              size="large"
              block
              class="submit-btn"
            >
              <template v-if="!loading">🚀 开始规划我的旅行</template>
              <template v-else>正在生成中...</template>
            </a-button>
          </a-form-item>

          <!-- 加载状态 -->
          <div v-if="loading" class="loading-box">
            <div class="loading-steps">
              <div
                v-for="(step, i) in loadingSteps"
                :key="i"
                class="loading-step"
                :class="{ done: loadingProgress > step.threshold, current: loadingProgress > step.threshold - 25 && loadingProgress <= step.threshold }"
              >
                <span class="step-dot">{{ loadingProgress > step.threshold ? '✅' : step.icon }}</span>
                <span class="step-text">{{ step.label }}</span>
              </div>
            </div>
            <a-progress
              :percent="loadingProgress"
              :show-info="false"
              :stroke-color="{ from: '#f97316', to: '#f59e0b' }"
              :stroke-width="8"
              style="margin-top: 16px"
            />
          </div>
        </a-form>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, watch } from 'vue'
import { useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import { generateTripPlan } from '@/services/api'
import type { TripFormData } from '@/types'
import type { Dayjs } from 'dayjs'

const router = useRouter()
const loading = ref(false)
const loadingProgress = ref(0)
const daysBounce = ref(false)

const loadingSteps = [
  { icon: '🔍', label: '搜索景点', threshold: 25 },
  { icon: '🌤️', label: '查询天气', threshold: 50 },
  { icon: '🏨', label: '推荐酒店', threshold: 75 },
  { icon: '📋', label: '生成行程', threshold: 90 },
]

interface HomeFormData {
  city: string
  start_date: Dayjs | null
  end_date: Dayjs | null
  travel_days: number
  transportation: string
  accommodation: string
  preferences: string[]
  free_text_input: string
}

const formData = reactive<HomeFormData>({
  city: '',
  start_date: null,
  end_date: null,
  travel_days: 1,
  transportation: '公共交通',
  accommodation: '经济型酒店',
  preferences: [],
  free_text_input: '',
})

// 日期变化时自动计算天数
watch([() => formData.start_date, () => formData.end_date], ([start, end]) => {
  if (start && end) {
    const days = end.diff(start, 'day') + 1
    if (days > 0 && days <= 30) {
      formData.travel_days = days
      daysBounce.value = true
      setTimeout(() => (daysBounce.value = false), 400)
    } else if (days > 30) {
      message.warning('旅行天数不能超过 30 天')
      formData.end_date = null
    } else {
      message.warning('结束日期不能早于开始日期')
      formData.end_date = null
    }
  }
})

const handleSubmit = async () => {
  if (!formData.start_date || !formData.end_date) {
    message.error('请选择日期')
    return
  }

  loading.value = true
  loadingProgress.value = 0

  const progressInterval = setInterval(() => {
    if (loadingProgress.value < 90) {
      loadingProgress.value += 3
    }
  }, 1000)

  try {
    const requestData: TripFormData = {
      city: formData.city,
      start_date: formData.start_date.format('YYYY-MM-DD'),
      end_date: formData.end_date.format('YYYY-MM-DD'),
      travel_days: formData.travel_days,
      transportation: formData.transportation,
      accommodation: formData.accommodation,
      preferences: formData.preferences,
      free_text_input: formData.free_text_input,
    }

    const response = await generateTripPlan(requestData)
    clearInterval(progressInterval)
    loadingProgress.value = 100

    if (response.success && response.data) {
      sessionStorage.setItem('tripPlan', JSON.stringify(response.data))
      message.success('旅行计划生成成功！')
      setTimeout(() => router.push('/result'), 600)
    } else {
      message.error(response.message || '生成失败')
    }
  } catch (error: any) {
    clearInterval(progressInterval)
    message.error(error.message || '生成旅行计划失败，请稍后重试')
  } finally {
    setTimeout(() => {
      loading.value = false
      loadingProgress.value = 0
    }, 1000)
  }
}
</script>

<style scoped>
/* ===== 页面 ===== */
.home-page {
  min-height: 100vh;
  background: var(--color-bg);
}

/* ===== Hero ===== */
.hero {
  position: relative;
  background: linear-gradient(160deg, #fff7ed 0%, #fff 30%, #fafbfc 100%);
  padding: var(--space-3xl) var(--space-xl) var(--space-2xl);
  text-align: center;
  overflow: hidden;
}

.hero-decoration {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.float-icon {
  position: absolute;
  font-size: 36px;
  opacity: 0.25;
  animation: hero-float 6s ease-in-out infinite;
}

@keyframes hero-float {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-16px) rotate(6deg); }
}

.hero-content {
  position: relative;
  max-width: 640px;
  margin: 0 auto;
}

.hero-title {
  font-size: 48px;
  font-weight: 800;
  color: var(--color-text);
  margin: 0 0 var(--space-md);
  letter-spacing: -1px;
  line-height: 1.2;
}

.hero-subtitle {
  font-size: 18px;
  color: var(--color-text-secondary);
  margin: 0;
  font-weight: 400;
  line-height: 1.6;
}

/* ===== 表单卡片 ===== */
.form-section {
  max-width: 1100px;
  margin: -40px auto 0;
  padding: 0 var(--space-xl) var(--space-3xl);
  position: relative;
}

.form-card {
  background: rgba(255, 255, 255, 0.88);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  padding: var(--space-xl);
}

.trip-form :deep(.ant-form-item) {
  margin-bottom: var(--space-md);
}

/* ===== 表单分区 ===== */
.form-block {
  margin-bottom: var(--space-lg);
  padding-bottom: var(--space-lg);
  border-bottom: 1px solid var(--color-border-light);
}

.form-block:last-of-type {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.block-header {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  margin-bottom: var(--space-md);
}

.block-icon {
  font-size: 20px;
}

.block-title {
  font-size: 16px;
  font-weight: 700;
  color: var(--color-text);
}

.input-label {
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text-secondary);
}

/* ===== 天数显示 ===== */
.days-pill {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  height: 40px;
  background: linear-gradient(135deg, var(--color-primary-100), var(--color-warm-light));
  border-radius: var(--radius-sm);
  border: 2px solid var(--color-primary-100);
}

.days-num {
  font-size: 24px;
  font-weight: 800;
  color: var(--color-primary);
  transition: transform var(--transition-base);
}

.days-num.bounce {
  animation: num-bounce 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes num-bounce {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.3); }
}

.days-unit {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-primary-600);
}

/* ===== 偏好标签 ===== */
.pref-group {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

:deep(.pref-chip) {
  margin: 0 !important;
}

:deep(.pref-chip .ant-checkbox-wrapper) {
  padding: 6px 16px;
  border: 2px solid var(--color-border);
  border-radius: 20px;
  transition: all var(--transition-fast);
  background: var(--color-surface);
  font-size: 14px;
}

:deep(.pref-chip .ant-checkbox-wrapper:hover) {
  border-color: var(--color-primary);
  background: var(--color-primary-light);
}

:deep(.pref-chip .ant-checkbox-wrapper-checked) {
  border-color: var(--color-primary);
  background: linear-gradient(135deg, var(--color-primary-100), var(--color-warm-light));
  color: var(--color-primary);
  font-weight: 600;
}

/* ===== 提交按钮 ===== */
.submit-btn {
  height: 54px;
  border-radius: var(--radius-lg);
  font-size: 17px;
  font-weight: 700;
  background: linear-gradient(135deg, var(--color-primary), var(--color-warm));
  border: none;
  box-shadow: 0 4px 20px rgba(249, 115, 22, 0.35);
  transition: all var(--transition-base);
  letter-spacing: 1px;
}

.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(249, 115, 22, 0.45);
}

.submit-btn:active {
  transform: translateY(0);
}

/* ===== 加载状态 ===== */
.loading-box {
  padding: var(--space-lg);
  background: var(--color-bg);
  border-radius: var(--radius-md);
  border: 2px dashed var(--color-primary-100);
}

.loading-steps {
  display: flex;
  justify-content: space-between;
  margin-bottom: var(--space-sm);
}

.loading-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  opacity: 0.35;
  transition: opacity var(--transition-base);
}

.loading-step.current {
  opacity: 1;
}

.loading-step.done {
  opacity: 0.7;
}

.step-dot {
  font-size: 22px;
}

.step-text {
  font-size: 12px;
  font-weight: 500;
  color: var(--color-text-secondary);
}

/* ===== 响应式 ===== */
@media (max-width: 768px) {
  .hero {
    padding: var(--space-2xl) var(--space-md) var(--space-xl);
  }

  .hero-title {
    font-size: 32px;
  }

  .hero-subtitle {
    font-size: 15px;
  }

  .form-section {
    margin-top: -20px;
    padding: 0 var(--space-md) var(--space-2xl);
  }

  .form-card {
    padding: var(--space-md);
  }

  .loading-steps {
    flex-wrap: wrap;
    gap: var(--space-sm);
  }
}
</style>
