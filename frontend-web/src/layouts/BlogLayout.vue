<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { RouterLink, RouterView } from 'vue-router'
import { NButton, NIcon, NDrawer, NDrawerContent } from 'naive-ui'
import { MenuOutline, CloseOutline, LogoGithub, Mail } from '@vicons/ionicons5'
import { settingsApi, type SiteSettings } from '@/api'

const showMobileMenu = ref(false)
const settings = ref<SiteSettings | null>(null)

const navLinks = [
  { name: '首页', path: '/' },
  { name: '文章', path: '/articles' },
  { name: '标签', path: '/tags' },
  { name: '关于', path: '/about' }
]

onMounted(async () => {
  try {
    settings.value = await settingsApi.get()
  } catch (error) {
    console.error('Failed to load settings:', error)
}
})
</script>

<template>
  <div class="min-h-screen bg-dark-bg text-dark-text">
    <!-- 导航栏 -->
    <header class="fixed top-0 left-0 right-0 z-50 glass">
      <nav class="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
        <!-- Logo -->
        <RouterLink to="/" class="flex items-center gap-2 group">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-primary-500 to-cyan-500 flex items-center justify-center text-white font-bold text-xl group-hover:scale-110 transition-transform">
            {{ settings?.site_name?.charAt(0) || 'B' }}
          </div>
          <span class="text-xl font-semibold hidden sm:block">{{ settings?.site_name || 'Blog' }}</span>
        </RouterLink>

        <!-- 桌面导航 -->
        <div class="hidden md:flex items-center gap-8">
          <RouterLink
            v-for="link in navLinks"
            :key="link.path"
            :to="link.path"
            class="text-dark-muted hover:text-white transition-colors relative group"
          >
            {{ link.name }}
            <span class="absolute -bottom-1 left-0 w-0 h-0.5 bg-primary-500 group-hover:w-full transition-all"></span>
          </RouterLink>
        </div>

        <!-- 右侧操作 -->
        <div class="flex items-center gap-4">
          <!-- 移动端菜单按钮 -->
          <NButton quaternary circle class="md:hidden" @click="showMobileMenu = true">
            <template #icon>
              <NIcon><MenuOutline /></NIcon>
            </template>
          </NButton>
        </div>
      </nav>
    </header>

    <!-- 移动端抽屉菜单 -->
    <NDrawer v-model:show="showMobileMenu" placement="right" :width="280">
      <NDrawerContent>
        <div class="flex flex-col h-full">
          <div class="flex justify-end p-4">
            <NButton quaternary circle @click="showMobileMenu = false">
              <template #icon>
                <NIcon><CloseOutline /></NIcon>
              </template>
            </NButton>
          </div>
          <div class="flex-1 px-4">
            <RouterLink
              v-for="link in navLinks"
              :key="link.path"
              :to="link.path"
              class="block py-3 text-lg text-dark-muted hover:text-white transition-colors border-b border-dark-border"
              @click="showMobileMenu = false"
            >
              {{ link.name }}
            </RouterLink>
          </div>
        </div>
      </NDrawerContent>
    </NDrawer>

    <!-- 主内容 -->
    <main class="pt-16">
      <RouterView />
    </main>

    <!-- 页脚 -->
    <footer class="border-t border-dark-border mt-20">
      <div class="max-w-6xl mx-auto px-4 py-12">
        <div class="flex flex-col md:flex-row justify-between items-center gap-6">
          <div class="text-center md:text-left">
            <p class="text-dark-muted">
              © {{ new Date().getFullYear() }} {{ settings?.site_name || 'Blog' }}. All rights reserved.
            </p>
            <p class="text-dark-muted text-sm mt-1">
              {{ settings?.site_description || 'Built with Vue 3 + Naive UI + Tailwind CSS' }}
            </p>
          </div>
          <div class="flex items-center gap-4">
            <a :href="settings?.github_url || 'https://github.com'" target="_blank" class="text-dark-muted hover:text-white transition-colors">
              <NIcon size="24"><LogoGithub /></NIcon>
            </a>
            <a :href="`mailto:${settings?.email || 'contact@example.com'}`" class="text-dark-muted hover:text-white transition-colors">
              <NIcon size="24"><Mail /></NIcon>
            </a>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>
