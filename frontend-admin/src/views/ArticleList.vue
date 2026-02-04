<script setup lang="ts">
import { ref, onMounted, h } from 'vue'
import { useRouter } from 'vue-router'
import { NCard, NDataTable, NButton, NIcon, NTag, NSpace, NPagination, useMessage, useDialog } from 'naive-ui'
import type { DataTableColumns } from 'naive-ui'
import { AddOutline, CreateOutline, TrashOutline, EyeOutline } from '@vicons/ionicons5'
import { articlesApi, type Article } from '@/api'

const router = useRouter()
const message = useMessage()
const dialog = useDialog()

const loading = ref(true)
const articles = ref<Article[]>([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(10)

const columns: DataTableColumns<Article> = [
  { title: 'ID', key: 'id', width: 60 },
  { title: '标题', key: 'title', ellipsis: { tooltip: true } },
  { title: '分类', key: 'category', width: 100, render: (row) => row.category?.name || '-' },
  {
    title: '状态',
    key: 'status',
    width: 80,
    render: (row) => h(NTag, { type: row.status === 'published' ? 'success' : 'warning', size: 'small' }, { default: () => row.status === 'published' ? '已发布' : '草稿' })
  },
  {
    title: '阅读量',
    key: 'views',
    width: 80,
    render: (row) => h('div', { class: 'flex items-center gap-1' }, [h(NIcon, { size: 14 }, { default: () => h(EyeOutline) }), row.views])
  },
  { title: '创建时间', key: 'created_at', width: 120, render: (row) => new Date(row.created_at).toLocaleDateString('zh-CN') },
  {
    title: '操作',
    key: 'actions',
    width: 200,
    render: (row) => h(NSpace, { wrap: false }, {
      default: () => [
        h(NButton, { size: 'small', quaternary: true, onClick: () => router.push(`/article/edit/${row.id}`) }, { icon: () => h(NIcon, null, { default: () => h(CreateOutline) }), default: () => '编辑' }),
        h(NButton, { size: 'small', quaternary: true, type: 'error', onClick: () => handleDelete(row) }, { icon: () => h(NIcon, null, { default: () => h(TrashOutline) }), default: () => '删除' })
      ]
    })
  }
]

onMounted(() => loadArticles())

async function loadArticles() {
  loading.value = true
  try {
    const res = await articlesApi.getList({ page: page.value, page_size: pageSize.value })
    articles.value = res.items
    total.value = res.total
  } catch (error) {
    message.error('加载文章列表失败')
  } finally {
    loading.value = false
  }
}

function handleDelete(article: Article) {
  dialog.warning({
    title: '确认删除',
    content: `确定要删除文章「${article.title}」吗？此操作不可撤销。`,
    positiveText: '删除',
    negativeText: '取消',
    onPositiveClick: async () => {
      try {
        await articlesApi.delete(article.id)
        message.success('删除成功')
        loadArticles()
      } catch (error) {
        message.error('删除失败')
      }
    }
  })
}

function handlePageChange(newPage: number) {
  page.value = newPage
  loadArticles()
}
</script>

<template>
  <NCard title="文章管理">
    <template #header-extra>
      <NButton type="primary" @click="router.push('/article/create')">
        <template #icon><NIcon><AddOutline /></NIcon></template>
        创建文章
      </NButton>
    </template>

    <NDataTable :columns="columns" :data="articles" :loading="loading" :bordered="false" />

    <div class="flex justify-end mt-4">
      <NPagination :page="page" :page-count="Math.ceil(total / pageSize)" @update:page="handlePageChange" />
    </div>
  </NCard>
</template>
