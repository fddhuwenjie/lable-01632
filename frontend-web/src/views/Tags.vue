<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { NSkeleton, NEmpty } from 'naive-ui'
import { tagsApi, type Tag } from '@/api'

const tags = ref<Tag[]>([])
const loading = ref(true)

onMounted(async () => {
  try {
    tags.value = await tagsApi.getList()
  } catch (error) {
    console.error('Failed to load tags:', error)
  } finally {
    loading.value = false
  }
})

function getTagSize(count: number): string {
  if (count >= 10) return 'text-2xl'
  if (count >= 5) return 'text-xl'
  if (count >= 3) return 'text-lg'
  return 'text-base'
}
</script>

<template>
  <div class="max-w-6xl mx-auto px-4 py-12">
    <div class="mb-12 text-center">
      <h1 class="text-4xl font-bold mb-4">
        <span class="gradient-text">所有标签</span>
      </h1>
      <p class="text-dark-muted">共 {{ tags.length }} 个标签</p>
    </div>

    <div v-if="loading" class="flex flex-wrap justify-center gap-4">
      <NSkeleton v-for="i in 12" :key="i" :width="100" :height="40" :sharp="false" />
    </div>

    <div v-else-if="tags.length === 0" class="py-20">
      <NEmpty description="暂无标签" />
    </div>

    <div v-else class="flex flex-wrap justify-center gap-4">
      <RouterLink
        v-for="(tag, index) in tags"
        :key="tag.id"
        :to="`/articles?tag=${tag.id}`"
        class="px-6 py-3 rounded-xl bg-dark-card border border-dark-border hover:border-primary-500/50 hover:bg-dark-border transition-all hover:scale-105 animate-slide-up"
        :style="{ animationDelay: `${index * 30}ms` }"
      >
        <span :class="getTagSize(tag.article_count || 0)" :style="{ color: tag.color || '#0ea5e9' }">
          #{{ tag.name }}
        </span>
        <span class="ml-2 text-dark-muted text-sm">({{ tag.article_count || 0 }})</span>
      </RouterLink>
    </div>
  </div>
</template>
