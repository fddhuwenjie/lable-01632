<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { NIcon, NTimeline, NTimelineItem, NSkeleton } from 'naive-ui'
import { LogoGithub, Mail, LocationOutline } from '@vicons/ionicons5'
import { settingsApi, type SiteSettings } from '@/api'

const loading = ref(true)
const settings = ref<SiteSettings | null>(null)

const skills = [
  { category: '前端', items: ['Vue.js', 'React', 'TypeScript', 'Tailwind CSS', 'Vite'] },
  { category: '后端', items: ['Python', 'FastAPI', 'Node.js', 'Go'] },
  { category: '数据库', items: ['PostgreSQL', 'MySQL', 'Redis', 'MongoDB'] },
  { category: 'DevOps', items: ['Docker', 'Kubernetes', 'CI/CD', 'Linux'] }
]

const timeline = [
  { year: '2024', title: '高级全栈开发工程师', desc: '负责核心产品开发与架构设计' },
  { year: '2022', title: '全栈开发工程师', desc: '参与多个重要项目的开发工作' },
  { year: '2020', title: '开始编程之旅', desc: '学习编程，踏入技术行业' }
]

onMounted(async () => {
  try {
    settings.value = await settingsApi.get()
  } catch (error) {
    console.error('Failed to load settings:', error)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="max-w-4xl mx-auto px-4 py-12">
    <section class="mb-16 animate-fade-in">
      <div class="flex flex-col md:flex-row items-center gap-8 mb-12">
        <div class="w-32 h-32 rounded-full bg-gradient-to-br from-primary-500 to-cyan-500 p-1 flex-shrink-0">
          <div v-if="settings?.author_avatar" class="w-full h-full rounded-full overflow-hidden">
            <img :src="settings.author_avatar" :alt="settings.author_name" class="w-full h-full object-cover" />
          </div>
          <div v-else class="w-full h-full rounded-full bg-dark-card flex items-center justify-center">
            <span class="text-5xl">👨‍💻</span>
          </div>
        </div>
        <div class="text-center md:text-left">
          <h1 class="text-3xl md:text-4xl font-bold mb-4">
            <span class="gradient-text">{{ settings?.author_name || '关于我' }}</span>
          </h1>
          <p v-if="loading" class="text-xl text-dark-muted">
            <NSkeleton text style="width: 200px" />
          </p>
          <p v-else class="text-xl text-dark-muted">全栈开发者 / 开源爱好者 / 技术博主</p>
        </div>
      </div>

      <div class="prose prose-invert max-w-none text-dark-text leading-relaxed space-y-4">
        <template v-if="loading">
          <NSkeleton text :repeat="3" />
        </template>
        <template v-else-if="settings?.author_bio">
          <p>{{ settings.author_bio }}</p>
        </template>
        <template v-else>
        <p>
          你好！我是一名热爱技术的全栈开发工程师，专注于 Web 全栈开发领域。
          我喜欢探索新技术，热衷于将复杂的问题简化为优雅的解决方案。
        </p>
        <p>
          在这个博客中，我会分享技术心得、项目经验以及对技术趋势的思考。
          希望我的内容能对你有所帮助，也欢迎与我交流讨论。
        </p>
        </template>
      </div>

      <div class="flex flex-wrap items-center gap-4 mt-8">
        <a 
          :href="settings?.github_url || 'https://github.com'" 
          target="_blank" 
          class="flex items-center gap-2 px-4 py-2 rounded-lg bg-dark-card hover:bg-dark-border transition-colors"
        >
          <NIcon size="20"><LogoGithub /></NIcon>
          <span>GitHub</span>
        </a>
        <a 
          :href="`mailto:${settings?.email || 'contact@example.com'}`" 
          class="flex items-center gap-2 px-4 py-2 rounded-lg bg-dark-card hover:bg-dark-border transition-colors"
        >
          <NIcon size="20"><Mail /></NIcon>
          <span>{{ settings?.email || 'Email' }}</span>
        </a>
        <span class="flex items-center gap-2 text-dark-muted">
          <NIcon size="20"><LocationOutline /></NIcon>
          <span>China</span>
        </span>
      </div>
    </section>

    <section class="mb-16 animate-slide-up">
      <h2 class="text-2xl font-bold mb-8">
        <span class="gradient-text">技术栈</span>
      </h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div v-for="skill in skills" :key="skill.category" class="p-6 rounded-xl bg-dark-card border border-dark-border">
          <h3 class="text-lg font-semibold mb-4 text-primary-400">{{ skill.category }}</h3>
          <div class="flex flex-wrap gap-2">
            <span v-for="item in skill.items" :key="item" class="px-3 py-1 rounded-full bg-dark-border text-sm">
              {{ item }}
            </span>
          </div>
        </div>
      </div>
    </section>

    <section class="animate-slide-up" style="animation-delay: 200ms;">
      <h2 class="text-2xl font-bold mb-8">
        <span class="gradient-text">经历</span>
      </h2>
      <NTimeline>
        <NTimelineItem v-for="item in timeline" :key="item.year" :title="item.title" :content="item.desc" :time="item.year">
          <template #icon>
            <div class="w-3 h-3 rounded-full bg-primary-500"></div>
          </template>
        </NTimelineItem>
      </NTimeline>
    </section>
  </div>
</template>
