<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { NCard, NGrid, NGridItem, NIcon, NSkeleton, NEmpty, NTag } from 'naive-ui'
import { DocumentTextOutline, PeopleOutline, EyeOutline, PricetagsOutline, TimeOutline } from '@vicons/ionicons5'
import { statsApi, type Article } from '@/api'

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
  return new Date(date).toLocaleDateString('zh-CN')
}

const statCards = [
  { key: 'total_articles', label: '文章总数', icon: DocumentTextOutline, color: '#0ea5e9' },
  { key: 'total_users', label: '用户总数', icon: PeopleOutline, color: '#10b981' },
  { key: 'total_views', label: '总阅读量', icon: EyeOutline, color: '#f59e0b' },
  { key: 'total_tags', label: '标签总数', icon: PricetagsOutline, color: '#8b5cf6' }
]
</script>

<template>
  <div class="space-y-6">
    <NGrid :cols="4" :x-gap="16" :y-gap="16" responsive="screen" item-responsive>
      <NGridItem v-for="stat in statCards" :key="stat.key" span="4 m:2 l:1">
        <NCard class="h-full">
          <div class="flex items-center gap-4">
            <div class="w-12 h-12 rounded-xl flex items-center justify-center" :style="{ backgroundColor: stat.color + '20' }">
              <NIcon :size="24" :style="{ color: stat.color }">
                <component :is="stat.icon" />
              </NIcon>
            </div>
            <div>
              <div class="text-dark-muted text-sm mb-1">{{ stat.label }}</div>
              <div v-if="loading">
                <NSkeleton text style="width: 60px" />
              </div>
              <div v-else class="text-2xl font-bold">
                {{ (stats as any)[stat.key] }}
              </div>
            </div>
          </div>
        </NCard>
      </NGridItem>
    </NGrid>

    <NGrid :cols="2" :x-gap="16" :y-gap="16" responsive="screen" item-responsive>
      <NGridItem span="2 l:1">
        <NCard title="最新文章">
          <template #header-extra>
            <RouterLink to="/articles" class="text-primary-400 hover:text-primary-300 text-sm">
              查看全部
            </RouterLink>
          </template>

          <div v-if="loading" class="space-y-4">
            <NSkeleton v-for="i in 5" :key="i" text :repeat="2" />
          </div>

          <div v-else-if="stats.recent_articles.length === 0">
            <NEmpty description="暂无文章" />
          </div>

          <div v-else class="space-y-4">
            <RouterLink
              v-for="article in stats.recent_articles"
              :key="article.id"
              :to="`/article/edit/${article.id}`"
              class="block p-3 rounded-lg hover:bg-dark-border transition-colors"
            >
              <div class="flex items-center justify-between gap-4">
                <div class="flex-1 min-w-0">
                  <div class="font-medium truncate">{{ article.title }}</div>
                  <div class="flex items-center gap-2 text-dark-muted text-sm mt-1">
                    <NIcon size="14"><TimeOutline /></NIcon>
                    <span>{{ formatDate(article.created_at) }}</span>
                    <NTag v-if="article.status === 'draft'" size="tiny" type="warning">草稿</NTag>
                  </div>
                </div>
                <div class="flex items-center gap-1 text-dark-muted text-sm">
                  <NIcon size="14"><EyeOutline /></NIcon>
                  <span>{{ article.views }}</span>
                </div>
              </div>
            </RouterLink>
          </div>
        </NCard>
      </NGridItem>

      <NGridItem span="2 l:1">
        <NCard title="热门文章">
          <template #header-extra>
            <RouterLink to="/articles" class="text-primary-400 hover:text-primary-300 text-sm">
              查看全部
            </RouterLink>
          </template>

          <div v-if="loading" class="space-y-4">
            <NSkeleton v-for="i in 5" :key="i" text :repeat="2" />
          </div>

          <div v-else-if="stats.popular_articles.length === 0">
            <NEmpty description="暂无文章" />
          </div>

          <div v-else class="space-y-4">
            <RouterLink
              v-for="(article, index) in stats.popular_articles"
              :key="article.id"
              :to="`/article/edit/${article.id}`"
              class="block p-3 rounded-lg hover:bg-dark-border transition-colors"
            >
              <div class="flex items-center gap-4">
                <div
                  class="w-8 h-8 rounded-lg flex items-center justify-center font-bold"
                  :class="{
                    'bg-yellow-500/20 text-yellow-500': index === 0,
                    'bg-gray-500/20 text-gray-400': index === 1,
                    'bg-orange-500/20 text-orange-500': index === 2,
                    'bg-dark-border text-dark-muted': index > 2
                  }"
                >
                  {{ index + 1 }}
                </div>
                <div class="flex-1 min-w-0">
                  <div class="font-medium truncate">{{ article.title }}</div>
                </div>
                <div class="flex items-center gap-1 text-dark-muted text-sm">
                  <NIcon size="14"><EyeOutline /></NIcon>
                  <span>{{ article.views }}</span>
                </div>
              </div>
            </RouterLink>
          </div>
        </NCard>
      </NGridItem>
    </NGrid>
  </div>
</template>
