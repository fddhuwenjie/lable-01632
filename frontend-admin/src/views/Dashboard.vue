<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { RouterLink } from 'vue-router'
import { NIcon, NSkeleton, NEmpty, NTag, NProgress } from 'naive-ui'
import { 
  DocumentTextOutline, 
  PeopleOutline, 
  EyeOutline, 
  PricetagsOutline, 
  TimeOutline,
  TrendingUpOutline,
  CreateOutline,
  ArrowForward
} from '@vicons/ionicons5'
import { statsApi, type Article } from '@/api'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const loading = ref(true)
const stats = ref({
  total_articles: 0,
  total_users: 0,
  total_views: 0,
  total_tags: 0,
  recent_articles: [] as Article[],
  popular_articles: [] as Article[]
})

onMounted(async () => {
  try {
    stats.value = await statsApi.getDashboard()
  } catch (error) {
    console.error('Failed to load stats:', error)
  } finally {
    loading.value = false
  }
})

function formatDate(date: string) {
  return new Date(date).toLocaleDateString('zh-CN', {
    month: 'short',
    day: 'numeric'
  })
}

function getGreeting() {
  const hour = new Date().getHours()
  if (hour < 12) return '早上好'
  if (hour < 18) return '下午好'
  return '晚上好'
}

const statCards = [
  { key: 'total_articles', label: '文章总数', icon: DocumentTextOutline, color: '#6366f1', bgColor: 'from-indigo-500/20 to-purple-500/10' },
  { key: 'total_users', label: '用户总数', icon: PeopleOutline, color: '#10b981', bgColor: 'from-emerald-500/20 to-teal-500/10' },
  { key: 'total_views', label: '总阅读量', icon: EyeOutline, color: '#f59e0b', bgColor: 'from-amber-500/20 to-orange-500/10' },
  { key: 'total_tags', label: '标签总数', icon: PricetagsOutline, color: '#ec4899', bgColor: 'from-pink-500/20 to-rose-500/10' }
]

const quickActions = computed(() => {
  const actions = [
    { label: '写文章', icon: CreateOutline, to: '/article/create', color: '#6366f1' },
    { label: '文章管理', icon: DocumentTextOutline, to: '/articles', color: '#10b981' }
  ]
  if (userStore.isAdmin) {
    actions.push(
      { label: '用户管理', icon: PeopleOutline, to: '/users', color: '#f59e0b' },
      { label: '标签管理', icon: PricetagsOutline, to: '/tags', color: '#ec4899' }
    )
  }
  return actions
})

// 计算最大阅读量用于进度条
const maxViews = computed(() => {
  if (stats.value.popular_articles.length === 0) return 1
  return Math.max(...stats.value.popular_articles.map(a => a.views))
})
</script>

<template>
  <div class="dashboard">
    <!-- 欢迎区域 -->
    <div class="welcome-section">
      <div class="welcome-content">
        <div class="welcome-text">
          <h1 class="greeting">{{ getGreeting() }}，{{ userStore.user?.username || 'Admin' }} 👋</h1>
          <p class="subtitle">欢迎回到博客管理系统，今天也要加油哦！</p>
        </div>
        <div class="quick-actions">
          <RouterLink
            v-for="action in quickActions"
            :key="action.label"
            :to="action.to"
            class="quick-action-btn"
          >
            <NIcon :size="18" :style="{ color: action.color }">
              <component :is="action.icon" />
            </NIcon>
            <span>{{ action.label }}</span>
          </RouterLink>
        </div>
      </div>
      <div class="welcome-decoration">
        <div class="decoration-circle circle-1"></div>
        <div class="decoration-circle circle-2"></div>
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-grid">
      <div v-for="stat in statCards" :key="stat.key" class="stat-card">
        <div class="stat-card-bg" :class="`bg-gradient-to-br ${stat.bgColor}`"></div>
        <div class="stat-card-content">
          <div class="stat-icon" :style="{ backgroundColor: stat.color + '20' }">
            <NIcon :size="24" :style="{ color: stat.color }">
              <component :is="stat.icon" />
            </NIcon>
          </div>
          <div class="stat-info">
            <span class="stat-label">{{ stat.label }}</span>
            <div v-if="loading" class="stat-value">
              <NSkeleton text style="width: 50px; height: 32px" />
            </div>
            <span v-else class="stat-value">{{ (stats as any)[stat.key].toLocaleString() }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 内容区域 -->
    <div class="content-grid">
      <!-- 最新文章 -->
      <div class="content-card">
        <div class="card-header">
          <div class="card-title">
            <NIcon :size="20" color="#6366f1"><TimeOutline /></NIcon>
            <span>最新文章</span>
          </div>
          <RouterLink to="/articles" class="view-all">
            查看全部
            <NIcon :size="16"><ArrowForward /></NIcon>
          </RouterLink>
        </div>

        <div v-if="loading" class="card-content">
          <div v-for="i in 5" :key="i" class="article-item-skeleton">
            <NSkeleton circle size="small" />
            <div class="flex-1">
              <NSkeleton text style="width: 80%" />
              <NSkeleton text style="width: 40%; margin-top: 8px" />
            </div>
          </div>
        </div>

        <div v-else-if="stats.recent_articles.length === 0" class="card-content">
          <NEmpty description="暂无文章" />
        </div>

        <div v-else class="card-content">
          <RouterLink
            v-for="(article, index) in stats.recent_articles"
            :key="article.id"
            :to="`/article/edit/${article.id}`"
            class="article-item"
            :style="{ animationDelay: `${index * 50}ms` }"
          >
            <div class="article-avatar">
              {{ article.title.charAt(0) }}
            </div>
            <div class="article-info">
              <div class="article-title">{{ article.title }}</div>
              <div class="article-meta">
                <span class="article-date">{{ formatDate(article.created_at) }}</span>
                <NTag v-if="article.status === 'draft'" size="tiny" type="warning" :bordered="false">草稿</NTag>
              </div>
            </div>
            <div class="article-views">
              <NIcon :size="14"><EyeOutline /></NIcon>
              {{ article.views }}
            </div>
          </RouterLink>
        </div>
      </div>

      <!-- 热门文章 -->
      <div class="content-card">
        <div class="card-header">
          <div class="card-title">
            <NIcon :size="20" color="#f59e0b"><TrendingUpOutline /></NIcon>
            <span>热门文章</span>
          </div>
          <RouterLink to="/articles" class="view-all">
            查看全部
            <NIcon :size="16"><ArrowForward /></NIcon>
          </RouterLink>
        </div>

        <div v-if="loading" class="card-content">
          <div v-for="i in 5" :key="i" class="popular-item-skeleton">
            <NSkeleton text style="width: 24px" />
            <div class="flex-1">
              <NSkeleton text style="width: 70%" />
              <NSkeleton text style="width: 100%; height: 6px; margin-top: 8px" />
            </div>
          </div>
        </div>

        <div v-else-if="stats.popular_articles.length === 0" class="card-content">
          <NEmpty description="暂无文章" />
        </div>

        <div v-else class="card-content">
          <RouterLink
            v-for="(article, index) in stats.popular_articles"
            :key="article.id"
            :to="`/article/edit/${article.id}`"
            class="popular-item"
            :style="{ animationDelay: `${index * 50}ms` }"
          >
            <div 
              class="rank-badge"
              :class="{
                'rank-1': index === 0,
                'rank-2': index === 1,
                'rank-3': index === 2
              }"
            >
              {{ index + 1 }}
            </div>
            <div class="popular-info">
              <div class="popular-title">{{ article.title }}</div>
              <div class="popular-progress">
                <NProgress
                  type="line"
                  :percentage="(article.views / maxViews) * 100"
                  :show-indicator="false"
                  :height="4"
                  :border-radius="2"
                  :fill-border-radius="2"
                  :color="index === 0 ? '#f59e0b' : index === 1 ? '#94a3b8' : index === 2 ? '#cd7c2f' : '#6366f1'"
                  rail-color="rgba(255,255,255,0.1)"
                />
              </div>
            </div>
            <div class="popular-views">{{ article.views.toLocaleString() }}</div>
          </RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* 欢迎区域 */
.welcome-section {
  position: relative;
  padding: 32px;
  background: rgba(22, 27, 34, 0.9);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  overflow: hidden;
}

.welcome-content {
  position: relative;
  z-index: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 24px;
}

.greeting {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 8px;
  color: #fff;
}

.subtitle {
  color: rgba(255, 255, 255, 0.6);
  font-size: 15px;
}

.quick-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.quick-action-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: #fff;
  font-size: 14px;
  transition: all 0.2s;
}

.quick-action-btn:hover {
  background: rgba(255, 255, 255, 0.15);
  transform: translateY(-2px);
}

.welcome-decoration {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.decoration-circle {
  position: absolute;
  border-radius: 50%;
  opacity: 0.5;
}

.circle-1 {
  width: 200px;
  height: 200px;
  background: radial-gradient(circle, rgba(14, 165, 233, 0.15), transparent);
  top: -50px;
  right: -50px;
}

.circle-2 {
  width: 150px;
  height: 150px;
  background: radial-gradient(circle, rgba(16, 185, 129, 0.15), transparent);
  bottom: -30px;
  right: 100px;
}

/* 统计卡片 */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

@media (max-width: 1200px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
}

.stat-card {
  position: relative;
  padding: 24px;
  background: rgba(22, 27, 34, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.3s;
}

.stat-card:hover {
  transform: translateY(-4px);
  border-color: rgba(255, 255, 255, 0.15);
}

.stat-card-bg {
  position: absolute;
  inset: 0;
  opacity: 0.5;
}

.stat-card-content {
  position: relative;
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-label {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.6);
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #fff;
}

/* 内容区域 */
.content-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

@media (max-width: 1024px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
}

.content-card {
  background: rgba(22, 27, 34, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  overflow: hidden;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.card-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 16px;
  font-weight: 600;
  color: #fff;
}

.view-all {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: rgba(255, 255, 255, 0.5);
  transition: color 0.2s;
}

.view-all:hover {
  color: #6366f1;
}

.card-content {
  padding: 16px;
}

/* 文章列表项 */
.article-item,
.popular-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px;
  border-radius: 12px;
  transition: all 0.2s;
  animation: fadeIn 0.3s ease-out forwards;
  opacity: 0;
}

@keyframes fadeIn {
  to {
    opacity: 1;
  }
}

.article-item:hover,
.popular-item:hover {
  background: rgba(255, 255, 255, 0.05);
}

.article-avatar {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  color: #fff;
  flex-shrink: 0;
}

.article-info {
  flex: 1;
  min-width: 0;
}

.article-title,
.popular-title {
  font-size: 14px;
  font-weight: 500;
  color: #fff;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-bottom: 4px;
}

.article-meta {
  display: flex;
  align-items: center;
  gap: 8px;
}

.article-date {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.4);
}

.article-views,
.popular-views {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: rgba(255, 255, 255, 0.5);
  flex-shrink: 0;
}

/* 热门文章排名 */
.rank-badge {
  width: 28px;
  height: 28px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 700;
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.5);
  flex-shrink: 0;
}

.rank-1 {
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: #fff;
}

.rank-2 {
  background: linear-gradient(135deg, #94a3b8, #64748b);
  color: #fff;
}

.rank-3 {
  background: linear-gradient(135deg, #cd7c2f, #a16207);
  color: #fff;
}

.popular-info {
  flex: 1;
  min-width: 0;
}

.popular-progress {
  margin-top: 8px;
}

/* 骨架屏 */
.article-item-skeleton,
.popular-item-skeleton {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px;
}
</style>
