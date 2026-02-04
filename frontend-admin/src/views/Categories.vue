<script setup lang="ts">
import { ref, onMounted, h } from 'vue'
import { NCard, NDataTable, NButton, NIcon, NSpace, NModal, NForm, NFormItem, NInput, useMessage, useDialog } from 'naive-ui'
import type { DataTableColumns, FormInst, FormRules } from 'naive-ui'
import { AddOutline, CreateOutline, TrashOutline } from '@vicons/ionicons5'
import { categoriesApi, type Category } from '@/api'

const message = useMessage()
const dialog = useDialog()

const loading = ref(true)
const categories = ref<Category[]>([])
const showModal = ref(false)
const modalLoading = ref(false)
const isEdit = ref(false)
const editId = ref<number | null>(null)

const formRef = ref<FormInst | null>(null)
const formValue = ref({ name: '', slug: '', description: '' })

const rules: FormRules = {
  name: [{ required: true, message: '请输入分类名称', trigger: 'blur' }]
}

const columns: DataTableColumns<Category> = [
  { title: 'ID', key: 'id', width: 60 },
  { title: '名称', key: 'name' },
  { title: 'Slug', key: 'slug' },
  { title: '描述', key: 'description', ellipsis: { tooltip: true } },
  { title: '文章数', key: 'article_count', width: 80 },
  {
    title: '操作',
    key: 'actions',
    width: 200,
    render: (row) => h(NSpace, { wrap: false }, {
      default: () => [
        h(NButton, { size: 'small', quaternary: true, onClick: () => handleEdit(row) }, { icon: () => h(NIcon, null, { default: () => h(CreateOutline) }), default: () => '编辑' }),
        h(NButton, { size: 'small', quaternary: true, type: 'error', onClick: () => handleDelete(row) }, { icon: () => h(NIcon, null, { default: () => h(TrashOutline) }), default: () => '删除' })
      ]
    })
  }
]

onMounted(() => loadCategories())

async function loadCategories() {
  loading.value = true
  try {
    categories.value = await categoriesApi.getList()
  } catch (error) {
    message.error('加载分类列表失败')
  } finally {
    loading.value = false
  }
}

function handleCreate() {
  isEdit.value = false
  editId.value = null
  formValue.value = { name: '', slug: '', description: '' }
  showModal.value = true
}

function handleEdit(category: Category) {
  isEdit.value = true
  editId.value = category.id
  formValue.value = { name: category.name, slug: category.slug, description: category.description || '' }
  showModal.value = true
}

async function handleSubmit() {
  try {
    await formRef.value?.validate()
    modalLoading.value = true

    const data = {
      name: formValue.value.name,
      slug: formValue.value.slug || formValue.value.name.toLowerCase().replace(/\s+/g, '-'),
      description: formValue.value.description || undefined
    }

    if (isEdit.value && editId.value) {
      await categoriesApi.update(editId.value, data)
      message.success('更新成功')
    } else {
      await categoriesApi.create(data)
      message.success('创建成功')
    }

    showModal.value = false
    loadCategories()
  } catch (error: any) {
    if (error?.detail) message.error(error.detail)
  } finally {
    modalLoading.value = false
  }
}

function handleDelete(category: Category) {
  dialog.warning({
    title: '确认删除',
    content: `确定要删除分类「${category.name}」吗？`,
    positiveText: '删除',
    negativeText: '取消',
    onPositiveClick: async () => {
      try {
        await categoriesApi.delete(category.id)
        message.success('删除成功')
        loadCategories()
      } catch (error) {
        message.error('删除失败')
      }
    }
  })
}
</script>

<template>
  <NCard title="分类管理">
    <template #header-extra>
      <NButton type="primary" @click="handleCreate">
        <template #icon><NIcon><AddOutline /></NIcon></template>
        添加分类
      </NButton>
    </template>

    <NDataTable :columns="columns" :data="categories" :loading="loading" :bordered="false" />

    <NModal v-model:show="showModal" :title="isEdit ? '编辑分类' : '添加分类'" preset="dialog" style="width: 500px">
      <NForm ref="formRef" :model="formValue" :rules="rules" label-placement="top">
        <NFormItem path="name" label="名称">
          <NInput v-model:value="formValue.name" placeholder="请输入分类名称" />
        </NFormItem>
        <NFormItem path="slug" label="Slug">
          <NInput v-model:value="formValue.slug" placeholder="留空自动生成" />
        </NFormItem>
        <NFormItem path="description" label="描述">
          <NInput v-model:value="formValue.description" type="textarea" placeholder="请输入描述 (可选)" />
        </NFormItem>
      </NForm>
      <template #action>
        <NSpace>
          <NButton @click="showModal = false">取消</NButton>
          <NButton type="primary" :loading="modalLoading" @click="handleSubmit">确定</NButton>
        </NSpace>
      </template>
    </NModal>
  </NCard>
</template>
