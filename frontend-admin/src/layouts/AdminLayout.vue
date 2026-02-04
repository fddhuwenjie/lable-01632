<script setup lang="ts">
import { ref, computed, h } from 'vue'
import { RouterLink, RouterView, useRoute, useRouter } from 'vue-router'
import { NLayout, NLayoutSider, NLayoutHeader, NLayoutContent, NMenu, NIcon, NButton, NAvatar, NDropdown, NBreadcrumb, NBreadcrumbItem } from 'naive-ui'
import type { MenuOption } from 'naive-ui'
import {
  HomeOutline,
  DocumentTextOutline,
  FolderOutline,
  PricetagsOutline,
  PeopleOutline,
  SettingsOutline,
  MenuOutline,
  LogOutOutline,
  AddOutline,
  GlobeOutline
} from '@vicons/ionicons5'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const collapsed = ref(false)
const activeKey = computed(() => route.name as string)

function renderIcon(icon: any) {
  return () => h(NIcon, null, { default: () => h(icon) })
}

const menuOptions: MenuOption[] = [
  {
    label: () => h(RouterLink, { to: '/' }, { default: () => '仪表盘' }),
    key: 'Dashboard',
    icon: renderIcon(HomeOutline)
  },
  {
    label: '内容管理',
    key: 'content',
    icon: renderIcon(DocumentTextOutline),
    children: [
      {
        label: () => h(RouterLink, { to: '/articles' }, { default: () => '文章列表' }),
        key: 'Articles'
      },
      {
        label: () => h(RouterLink, { to: '/article/create' }, { default: () => '创建文章' }),
        key: 'CreateArticle',
        icon: renderIcon(AddOutline)
      }
    ]
  },
  {
    label: () => h(RouterLink, { to: '/categories' }, { default: () => '分类管理' }),
    key: 'Categories',
    icon: renderIcon(FolderOutline)
  },
  {
    label: () => h(RouterLink, { to: '/tags' }, { default: () => '标签管理' }),
    key: 'Tags',
    icon: renderIcon(PricetagsOutline)
  },
  {
    label: () => h(RouterLink, { to: '/users' }, { default: () => '用户管理' }),
    key: 'Users',
    icon: renderIcon(PeopleOutline)
  },
  {
    label: () => h(RouterLink, { to: '/settings' }, { default: () => '系统设置' }),
    key: 'Settings',
    icon: renderIcon(SettingsOutline)
  }
]

const userDropdownOptions = [
  {
    label: '访问前台',
    key: 'frontend',
    icon: renderIcon(GlobeOutline)
  },
  {
    type: 'divider',
    key: 'd1'
  },
  {
    label: '退出登录',
    key: 'logout',
    icon: renderIcon(LogOutOutline)
  }
]

function handleUserSelect(key: string) {
  switch (key) {
    case 'frontend':
      window.open('/', '_blank')
      break
    case 'logout':
      userStore.logout()
      router.push('/login')
      break
  }
}

const breadcrumbItems = computed(() => {
  const items = [{ name: '首页', path: '/' }]
  if (route.meta.title && route.name !== 'Dashboard') {
    items.push({ name: route.meta.title as string, path: route.path })
  }
  return items
})
</script>

<template>
  <NLayout class="h-screen" has-sider>
    <NLayoutSider
      bordered
      collapse-mode="width"
      :collapsed-width="64"
      :width="220"
      :collapsed="collapsed"
      show-trigger
      @collapse="collapsed = true"
      @expand="collapsed = false"
      class="!bg-dark-card"
    >
      <div class="h-16 flex items-center justify-center border-b border-dark-border">
        <RouterLink to="/" class="flex items-center gap-2">
          <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-violet-500 to-indigo-500 flex items-center justify-center text-white font-bold">
            A
          </div>
          <span v-if="!collapsed" class="text-lg font-semibold text-white">Admin</span>
        </RouterLink>
      </div>

      <NMenu
        :value="activeKey"
        :collapsed="collapsed"
        :collapsed-width="64"
        :collapsed-icon-size="22"
        :options="menuOptions"
        class="pt-2"
      />
    </NLayoutSider>

    <NLayout>
      <NLayoutHeader class="h-16 px-6 flex items-center justify-between border-b border-dark-border bg-dark-card">
        <div class="flex items-center gap-4">
          <NButton quaternary circle @click="collapsed = !collapsed">
            <template #icon>
              <NIcon><MenuOutline /></NIcon>
            </template>
          </NButton>
          <NBreadcrumb>
            <NBreadcrumbItem v-for="item in breadcrumbItems" :key="item.path">
              <RouterLink :to="item.path">{{ item.name }}</RouterLink>
            </NBreadcrumbItem>
          </NBreadcrumb>
        </div>

        <div class="flex items-center gap-4">
          <NDropdown trigger="click" :options="userDropdownOptions" @select="handleUserSelect">
            <div class="flex items-center gap-2 cursor-pointer hover:bg-dark-border px-3 py-2 rounded-lg transition-colors">
              <NAvatar round size="small" :src="userStore.user?.avatar">
                {{ userStore.user?.username?.charAt(0)?.toUpperCase() }}
              </NAvatar>
              <span class="text-sm">{{ userStore.user?.username || 'Admin' }}</span>
            </div>
          </NDropdown>
        </div>
      </NLayoutHeader>

      <NLayoutContent class="p-6 bg-dark-bg overflow-auto">
        <RouterView />
      </NLayoutContent>
    </NLayout>
  </NLayout>
</template>

<style scoped>
:deep(.n-layout-sider) {
  background-color: #161b22 !important;
}

:deep(.n-menu) {
  background-color: transparent !important;
}

:deep(.n-menu-item-content) {
  color: #8b949e !important;
}

:deep(.n-menu-item-content:hover) {
  color: #c9d1d9 !important;
}

:deep(.n-menu-item-content--selected) {
  color: #0ea5e9 !important;
}
</style>
