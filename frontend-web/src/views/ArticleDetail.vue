<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import { NIcon, NTag, NSkeleton, NEmpty, NAvatar, NDivider } from 'naive-ui'
import { TimeOutline, EyeOutline, ArrowBack, PersonOutline } from '@vicons/ionicons5'
import { marked } from 'marked'
import { articlesApi, type Article } from '@/api'

const route = useRoute()
const article = ref<Article | null>(null)
const loading = ref(true)

marked.setOptions({
  breaks: true,
  gfm: true
})

const renderedContent = computed(() => {
  if (!article.value?.content) return ''
  return marked(article.value.content)
})

onMounted(async () => {
  try {
    const id = Number(route.params.id)
    article.value = await articlesApi.getById(id)
  } catch (error) {
    console.error('Failed to load article:', error)
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
</script>

<template>
  <div class="max-w-4xl mx-auto px-4 py-12">
    <RouterLink to="/articles" class="inline-flex items-center gap-2 text-dark-muted hover:text-white transition-colors mb-8">
      <NIcon><ArrowBack /></NIcon>
      <span>返回文章列表</span>
    </RouterLink>

    <div v-if="loading" class="space-y-6">
      <NSkeleton text style="width: 60%" />
      <NSkeleton text :repeat="8" />
    </div>

    <div v-else-if="!article" class="py-20">
      <NEmpty description="文章不存在" />
    </div>

    <article v-else class="animate-fade-in">
      <header class="mb-12">
        <div class="flex items-center gap-2 mb-4">
          <NTag v-if="article.category" size="small" :bordered="false" type="info">
            {{ article.category.name }}
          </NTag>
        </div>

        <h1 class="text-3xl md:text-4xl font-bold mb-6">
          {{ article.title }}
        </h1>

        <p class="text-xl text-dark-muted mb-6">
          {{ article.summary }}
        </p>

        <div class="flex flex-wrap items-center gap-6 text-dark-muted">
          <div class="flex items-center gap-2">
            <NAvatar round size="small" :src="article.author?.avatar">
              <template #fallback>
                <NIcon><PersonOutline /></NIcon>
              </template>
            </NAvatar>
            <span>{{ article.author?.username || '匿名' }}</span>
          </div>
          <span class="flex items-center gap-1">
            <NIcon size="18"><TimeOutline /></NIcon>
            {{ formatDate(article.created_at) }}
          </span>
          <span class="flex items-center gap-1">
            <NIcon size="18"><EyeOutline /></NIcon>
            {{ article.views }} 阅读
          </span>
        </div>

        <div class="flex flex-wrap gap-2 mt-6">
          <NTag v-for="tag in article.tags" :key="tag.id" size="small" :bordered="false" round>
            #{{ tag.name }}
          </NTag>
        </div>
      </header>

      <div v-if="article.cover_image" class="mb-12">
        <img :src="article.cover_image" :alt="article.title" class="w-full rounded-xl" />
      </div>

      <NDivider />

      <div class="blog-content prose prose-invert max-w-none" v-html="renderedContent"></div>

      <NDivider />

      <footer class="mt-12">
        <div class="flex flex-wrap items-center gap-4">
          <span class="text-dark-muted">标签：</span>
          <RouterLink
            v-for="tag in article.tags"
            :key="tag.id"
            :to="`/articles?tag=${tag.id}`"
            class="px-3 py-1 rounded-lg bg-dark-card hover:bg-dark-border transition-colors"
          >
            #{{ tag.name }}
          </RouterLink>
        </div>

        <div class="mt-8 p-6 rounded-xl bg-dark-card border border-dark-border">
          <div class="flex items-center gap-4">
            <NAvatar round size="large" :src="article.author?.avatar">
              <template #fallback>
                <NIcon size="24"><PersonOutline /></NIcon>
              </template>
            </NAvatar>
            <div>
              <div class="font-semibold">{{ article.author?.username || '匿名' }}</div>
              <div class="text-dark-muted text-sm">文章作者</div>
            </div>
          </div>
        </div>
      </footer>
    </article>
  </div>
</template>

<style scoped>
:deep(.blog-content) {
  color: #c9d1d9;
  line-height: 1.8;
}

:deep(.blog-content h1),
:deep(.blog-content h2),
:deep(.blog-content h3),
:deep(.blog-content h4) {
  color: #fff;
  font-weight: 600;
  margin-top: 2rem;
  margin-bottom: 1rem;
}

:deep(.blog-content h1) { font-size: 2rem; }
:deep(.blog-content h2) { font-size: 1.5rem; }
:deep(.blog-content h3) { font-size: 1.25rem; }

:deep(.blog-content p) { margin-bottom: 1rem; }

:deep(.blog-content a) { color: #0ea5e9; }
:deep(.blog-content a:hover) { color: #38bdf8; }

:deep(.blog-content code) {
  background-color: #161b22;
  padding: 0.2rem 0.4rem;
  border-radius: 0.25rem;
  font-size: 0.875rem;
  font-family: 'JetBrains Mono', monospace;
}

:deep(.blog-content pre) {
  background-color: #161b22;
  padding: 1rem;
  border-radius: 0.5rem;
  overflow-x: auto;
  margin: 1.5rem 0;
}

:deep(.blog-content pre code) {
  background-color: transparent;
  padding: 0;
}

:deep(.blog-content blockquote) {
  border-left: 4px solid #0ea5e9;
  padding-left: 1rem;
  margin: 1rem 0;
  color: #8b949e;
  font-style: italic;
}

:deep(.blog-content ul),
:deep(.blog-content ol) {
  padding-left: 1.5rem;
  margin-bottom: 1rem;
}

:deep(.blog-content li) { margin-bottom: 0.5rem; }

:deep(.blog-content img) {
  border-radius: 0.5rem;
  max-width: 100%;
  height: auto;
  margin: 1rem 0;
}
</style>
