<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import { NIcon, NTag, NPagination, NEmpty, NSelect } from 'naive-ui'
import { TimeOutline, EyeOutline } from '@vicons/ionicons5'
import { articlesApi, categoriesApi, tagsApi, type Article, type Category, type Tag } from '@/api'

const route = useRoute()

const articles = ref<Article[]>([])
const categories = ref<Category[]>([])
const tags = ref<Tag[]>([])
const loading = ref(true)
const total = ref(0)
const page = ref(1)
const pageSize = ref(12)

const selectedCategory = ref<number | null>(null)
const selectedTag = ref<number | null>(null)

onMounted(async () => {
  // 先从 URL 读取参数，再加载数据，避免二次请求导致抖动
  if (route.query.category) {
    selectedCategory.value = Number(route.query.category)
  }
  if (route.query.tag) {
    selectedTag.value = Number(route.query.tag)
  }
  
  await Promise.all([loadArticles(), loadFilters()])
})

async function loadArticles() {
  loading.value = true
  try {
    const res = await articlesApi.getList({
      page: page.value,
      page_size: pageSize.value,
      category_id: selectedCategory.value || undefined,
      tag_id: selectedTag.value || undefined,
      status: 'published'
    })
    articles.value = res.items
    total.value = res.total
  } catch (error) {
    console.error('Failed to load articles:', error)
  } finally {
    loading.value = false
  }
}

async function loadFilters() {
  try {
    const [categoriesRes, tagsRes] = await Promise.all([
      categoriesApi.getList(),
      tagsApi.getList()
    ])
    categories.value = categoriesRes
    tags.value = tagsRes
  } catch (error) {
    console.error('Failed to load filters:', error)
  }
}

watch([selectedCategory, selectedTag, page], () => {
  loadArticles()
})

function formatDate(date: string) {
  return new Date(date).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const categoryOptions = ref<Array<{ label: string; value: number | null }>>([
  { label: '全部分类', value: null },
])

const tagOptions = ref<Array<{ label: string; value: number | null }>>([
  { label: '全部标签', value: null },
])

watch(categories, (newCategories) => {
  categoryOptions.value = [
    { label: '全部分类', value: null },
    ...newCategories.map(c => ({ label: c.name, value: c.id }))
  ]
})

watch(tags, (newTags) => {
  tagOptions.value = [
    { label: '全部标签', value: null },
    ...newTags.map(t => ({ label: t.name, value: t.id }))
  ]
})
</script>

<template>
  <div class="max-w-6xl mx-auto px-4 py-12">
    <div class="mb-12 text-center">
      <h1 class="text-4xl font-bold mb-4">
        <span class="gradient-text">文章列表</span>
      </h1>
      <p class="text-dark-muted">共 {{ total }} 篇文章</p>
    </div>

    <div class="flex flex-wrap gap-4 mb-8">
      <NSelect
        v-model:value="selectedCategory"
        :options="categoryOptions as any"
        placeholder="选择分类"
        clearable
        style="width: 160px"
      />
      <NSelect
        v-model:value="selectedTag"
        :options="tagOptions as any"
        placeholder="选择标签"
        clearable
        style="width: 160px"
      />
    </div>

    <div v-if="!loading && articles.length === 0" class="py-20">
      <NEmpty description="暂无文章" />
    </div>

    <div v-else class="space-y-6">
      <RouterLink
        v-for="article in articles"
        :key="article.id"
        :to="`/article/${article.id}`"
        class="block group bg-dark-card rounded-xl p-6 border border-dark-border hover:border-primary-500/50 transition-all hover:-translate-y-1"
      >
        <div class="flex flex-col md:flex-row gap-6">
          <div v-if="article.cover_image" class="md:w-64 flex-shrink-0">
            <img :src="article.cover_image" :alt="article.title" class="w-full h-40 md:h-full object-cover rounded-lg" />
          </div>

          <div class="flex-1">
            <div class="flex items-center gap-2 mb-3">
              <NTag v-if="article.category" size="small" :bordered="false" type="info">
                {{ article.category.name }}
              </NTag>
            </div>

            <h2 class="text-xl font-semibold mb-3 group-hover:text-primary-400 transition-colors">
              {{ article.title }}
            </h2>

            <p class="text-dark-muted mb-4 line-clamp-2">
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
              <NTag v-for="tag in article.tags" :key="tag.id" size="tiny" :bordered="false" round>
                {{ tag.name }}
              </NTag>
            </div>
          </div>
        </div>
      </RouterLink>
    </div>

    <div v-if="total > pageSize" class="flex justify-center mt-12">
      <NPagination v-model:page="page" :page-count="Math.ceil(total / pageSize)" :page-slot="5" />
    </div>
  </div>
</template>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
