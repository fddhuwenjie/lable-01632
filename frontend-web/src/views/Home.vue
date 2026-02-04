<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { NIcon, NTag, NSkeleton, NEmpty } from 'naive-ui'
import { ArrowForward, TimeOutline, EyeOutline, LogoGithub, Mail, LocationOutline } from '@vicons/ionicons5'
import { articlesApi, tagsApi, type Article, type Tag } from '@/api'

const articles = ref<Article[]>([])
const tags = ref<Tag[]>([])
const loading = ref(true)

onMounted(async () => {
  try {
    const [articlesRes, tagsRes] = await Promise.all([
      articlesApi.getRecent(6),
      tagsApi.getList()
    ])
    articles.value = articlesRes
    tags.value = tagsRes
  } catch (error) {
    console.error('Failed to load data:', error)
  } finally {
    loading.value = false
  }
})

function formatDate(date: string) {
  return new Date(date).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const skills = [
  { name: 'Vue.js', color: '#42b883' },
  { name: 'TypeScript', color: '#3178c6' },
  { name: 'Python', color: '#3776ab' },
  { name: 'Docker', color: '#2496ed' },
  { name: 'FastAPI', color: '#009688' },
  { name: 'PostgreSQL', color: '#336791' }
]
</script>

<template>
  <div class="min-h-screen">
    <!-- Hero Section -->
    <section class="relative overflow-hidden">
      <div class="absolute inset-0 bg-gradient-to-br from-primary-900/20 via-dark-bg to-dark-bg"></div>
      <div class="absolute top-20 left-10 w-72 h-72 bg-primary-500/10 rounded-full blur-3xl animate-float"></div>
      <div class="absolute bottom-10 right-10 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl animate-float" style="animation-delay: 2s;"></div>
      
      <div class="relative max-w-6xl mx-auto px-4 py-20 md:py-32">
        <div class="flex flex-col md:flex-row items-center gap-12">
          <div class="animate-fade-in">
            <div class="relative">
              <div class="w-40 h-40 md:w-48 md:h-48 rounded-full bg-gradient-to-br from-primary-500 to-cyan-500 p-1">
                <div class="w-full h-full rounded-full bg-dark-card flex items-center justify-center">
                  <span class="text-6xl md:text-7xl">👨‍💻</span>
                </div>
              </div>
              <div class="absolute -bottom-2 -right-2 w-12 h-12 bg-green-500 rounded-full border-4 border-dark-bg flex items-center justify-center">
                <span class="text-xl">🎯</span>
              </div>
            </div>
          </div>

          <div class="flex-1 text-center md:text-left">
            <h1 class="text-4xl md:text-5xl lg:text-6xl font-bold mb-4 animate-slide-up">
              <span class="gradient-text">Hi, I'm Developer</span>
            </h1>
            <p class="text-xl md:text-2xl text-dark-muted mb-6 animate-slide-up animate-delay-100">
              全栈开发者 / 开源爱好者 / 技术博主
            </p>
            <p class="text-dark-muted leading-relaxed mb-8 max-w-2xl animate-slide-up animate-delay-200">
              热爱编程，专注于 Web 全栈开发。喜欢探索新技术，分享技术心得，
              致力于用代码创造有价值的产品。
            </p>

            <div class="flex items-center justify-center md:justify-start gap-4 animate-slide-up animate-delay-300">
              <a href="https://github.com" target="_blank" class="flex items-center gap-2 px-4 py-2 rounded-lg bg-dark-card hover:bg-dark-border transition-colors">
                <NIcon size="20"><LogoGithub /></NIcon>
                <span>GitHub</span>
              </a>
              <a href="mailto:contact@example.com" class="flex items-center gap-2 px-4 py-2 rounded-lg bg-dark-card hover:bg-dark-border transition-colors">
                <NIcon size="20"><Mail /></NIcon>
                <span>Email</span>
              </a>
              <span class="flex items-center gap-2 text-dark-muted">
                <NIcon size="20"><LocationOutline /></NIcon>
                <span>China</span>
              </span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 技能标签 -->
    <section class="max-w-6xl mx-auto px-4 py-12">
      <div class="flex flex-wrap justify-center gap-3">
        <span
          v-for="skill in skills"
          :key="skill.name"
          class="px-4 py-2 rounded-full text-sm font-medium transition-transform hover:scale-105"
          :style="{ backgroundColor: skill.color + '20', color: skill.color, border: `1px solid ${skill.color}40` }"
        >
          {{ skill.name }}
        </span>
      </div>
    </section>

    <!-- 最新文章 -->
    <section class="max-w-6xl mx-auto px-4 py-16">
      <div class="flex items-center justify-between mb-8">
        <h2 class="text-2xl md:text-3xl font-bold">
          <span class="gradient-text">最新文章</span>
        </h2>
        <RouterLink to="/articles" class="flex items-center gap-2 text-primary-400 hover:text-primary-300 transition-colors group">
          <span>查看全部</span>
          <NIcon class="group-hover:translate-x-1 transition-transform"><ArrowForward /></NIcon>
        </RouterLink>
      </div>

      <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="i in 6" :key="i" class="bg-dark-card rounded-xl p-6 border border-dark-border">
          <NSkeleton text :repeat="4" />
        </div>
      </div>

      <div v-else-if="articles.length === 0" class="py-12">
        <NEmpty description="暂无文章" />
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <RouterLink
          v-for="(article, index) in articles"
          :key="article.id"
          :to="`/article/${article.id}`"
          class="group bg-dark-card rounded-xl p-6 border border-dark-border hover:border-primary-500/50 transition-all hover:-translate-y-1 animate-slide-up"
          :style="{ animationDelay: `${index * 100}ms` }"
        >
          <div class="flex items-center gap-2 mb-3">
            <NTag v-if="article.category" size="small" :bordered="false" type="info">
              {{ article.category.name }}
            </NTag>
          </div>

          <h3 class="text-lg font-semibold mb-3 group-hover:text-primary-400 transition-colors line-clamp-2">
            {{ article.title }}
          </h3>

          <p class="text-dark-muted text-sm mb-4 line-clamp-3">
            {{ article.summary }}
          </p>

          <div class="flex items-center gap-4 text-dark-muted text-sm">
            <span class="flex items-center gap-1">
              <NIcon size="16"><TimeOutline /></NIcon>
              {{ formatDate(article.created_at) }}
            </span>
            <span class="flex items-center gap-1">
              <NIcon size="16"><EyeOutline /></NIcon>
              {{ article.views }}
            </span>
          </div>

          <div class="flex flex-wrap gap-2 mt-4">
            <NTag v-for="tag in article.tags.slice(0, 3)" :key="tag.id" size="tiny" :bordered="false" round>
              {{ tag.name }}
            </NTag>
          </div>
        </RouterLink>
      </div>
    </section>

    <!-- 热门标签 -->
    <section class="max-w-6xl mx-auto px-4 py-16">
      <div class="flex items-center justify-between mb-8">
        <h2 class="text-2xl md:text-3xl font-bold">
          <span class="gradient-text">热门标签</span>
        </h2>
        <RouterLink to="/tags" class="flex items-center gap-2 text-primary-400 hover:text-primary-300 transition-colors group">
          <span>查看全部</span>
          <NIcon class="group-hover:translate-x-1 transition-transform"><ArrowForward /></NIcon>
        </RouterLink>
      </div>

      <div v-if="loading" class="flex flex-wrap gap-3">
        <NSkeleton v-for="i in 8" :key="i" :width="80" :height="32" :sharp="false" />
      </div>

      <div v-else-if="tags.length === 0">
        <NEmpty description="暂无标签" />
      </div>

      <div v-else class="flex flex-wrap gap-3">
        <RouterLink
          v-for="tag in tags"
          :key="tag.id"
          :to="`/articles?tag=${tag.id}`"
          class="px-4 py-2 rounded-lg bg-dark-card border border-dark-border hover:border-primary-500/50 hover:bg-dark-border transition-all flex items-center gap-2"
        >
          <span :style="{ color: tag.color || '#0ea5e9' }">#</span>
          <span>{{ tag.name }}</span>
          <span class="text-dark-muted text-sm">({{ tag.article_count || 0 }})</span>
        </RouterLink>
      </div>
    </section>
  </div>
</template>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
