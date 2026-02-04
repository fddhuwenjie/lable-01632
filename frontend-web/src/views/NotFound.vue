<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { NButton, NIcon } from 'naive-ui'
import { HomeOutline, ArrowBack } from '@vicons/ionicons5'
</script>

<template>
  <div class="min-h-screen bg-dark-bg flex items-center justify-center px-4">
    <div class="text-center">
      <h1 class="text-9xl font-bold gradient-text mb-4">404</h1>
      <h2 class="text-2xl font-semibold mb-4">页面未找到</h2>
      <p class="text-dark-muted mb-8">抱歉，您访问的页面不存在或已被移除</p>
      <div class="flex items-center justify-center gap-4">
        <NButton @click="$router.back()">
          <template #icon>
            <NIcon><ArrowBack /></NIcon>
          </template>
          返回上页
        </NButton>
        <RouterLink to="/">
          <NButton type="primary">
            <template #icon>
              <NIcon><HomeOutline /></NIcon>
            </template>
            返回首页
          </NButton>
        </RouterLink>
      </div>
    </div>
  </div>
</template>
