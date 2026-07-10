<template>
  <div id="app">
    <!-- 顶部导航栏 - 玻璃拟态 -->
    <header class="app-header" :class="{ 'header-scrolled': scrolled }">
      <div class="header-inner">
        <router-link to="/" class="logo">
          <span class="logo-icon">✈️</span>
          <span class="logo-text">Trip Planner</span>
        </router-link>
        <nav class="nav-links">
          <router-link to="/" class="nav-link">首页</router-link>
          <a href="/docs" target="_blank" class="nav-link">API 文档</a>
        </nav>
      </div>
    </header>

    <!-- 页面内容 -->
    <main class="app-content">
      <router-view v-slot="{ Component }">
        <transition name="page-fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <!-- 底部 -->
    <footer class="app-footer">
      <p>Made with <span class="heart">❤️</span> &amp; HelloAgents Framework</p>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const scrolled = ref(false)

const handleScroll = () => {
  scrolled.value = window.scrollY > 20
}

onMounted(() => window.addEventListener('scroll', handleScroll))
onUnmounted(() => window.removeEventListener('scroll', handleScroll))
</script>

<style scoped>
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--color-bg);
}

/* ===== 导航栏 ===== */
.app-header {
  position: sticky;
  top: 0;
  z-index: 1000;
  background: rgba(255, 255, 255, 0.82);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-bottom: 1px solid transparent;
  transition: all var(--transition-base);
}

.header-scrolled {
  border-bottom-color: var(--color-border-light);
  box-shadow: var(--shadow-sm);
}

.header-inner {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 var(--space-xl);
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  text-decoration: none;
  color: var(--color-text);
  font-weight: 700;
  font-size: 20px;
}

.logo-icon {
  font-size: 26px;
}

.logo-text {
  background: linear-gradient(135deg, var(--color-primary), var(--color-warm));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.nav-links {
  display: flex;
  gap: var(--space-lg);
}

.nav-link {
  text-decoration: none;
  color: var(--color-text-secondary);
  font-size: 15px;
  font-weight: 500;
  padding: var(--space-xs) var(--space-sm);
  border-radius: var(--radius-sm);
  transition: all var(--transition-fast);
}

.nav-link:hover,
.nav-link.router-link-exact-active {
  color: var(--color-primary);
  background: var(--color-primary-light);
}

/* ===== 内容区 ===== */
.app-content {
  flex: 1;
}

/* ===== 页面过渡动画 ===== */
.page-fade-enter-active,
.page-fade-leave-active {
  transition: opacity 0.25s ease, transform 0.25s ease;
}

.page-fade-enter-from {
  opacity: 0;
  transform: translateY(8px);
}

.page-fade-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

/* ===== 底部 ===== */
.app-footer {
  text-align: center;
  padding: var(--space-xl);
  color: var(--color-text-muted);
  font-size: 13px;
  border-top: 1px solid var(--color-border-light);
}

.app-footer .heart {
  color: var(--color-primary);
  animation: heartbeat 1.5s infinite;
}

@keyframes heartbeat {
  0%, 100% { transform: scale(1); }
  25% { transform: scale(1.15); }
  50% { transform: scale(1); }
  75% { transform: scale(1.15); }
}
</style>
