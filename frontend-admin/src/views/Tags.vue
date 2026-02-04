<script setup lang="ts">
import { ref, onMounted, h } from 'vue'
import { NCard, NDataTable, NButton, NIcon, NSpace, NModal, NForm, NFormItem, NInput, NColorPicker, NTag, useMessage, useDialog } from 'naive-ui'
import type { DataTableColumns, FormInst, FormRules } from 'naive-ui'
import { AddOutline, CreateOutline, TrashOutline } from '@vicons/ionicons5'
import { tagsApi, type Tag } from '@/api'

const message = useMessage()
const dialog = useDialog()

const loading = ref(true)
const tags = ref<Tag[]>([])
const showModal = ref(false)
const modalLoading = ref(false)
const isEdit = ref(false)
const editId = ref<number | null>(null)

const formRef = ref<FormInst | null>(null)
const formValue = ref({ name: '', slug: '', color: '#0ea5e9' })

const rules: FormRules = {
  name: [{ required: true, message: '请输入标签名称', trigger: 'blur' }]
}

const columns: DataTableColumns<Tag> = [
  { title: 'ID', key: 'id', width: 60 },
  {
    title: '名称',
    key: 'name',
    render: (row) => h(NTag, { style: { backgroundColor: (row.color || '#0ea5e9') + '20', color: row.color || '#0ea5e9', border: 'none' } }, { default: () => '#' + row.name })
  },
  { title: 'Slug', key: 'slug' },
  {
    title: '颜色',
    key: 'color',
    width: 100,
    render: (row) => h('div', { class: 'w-6 h-6 rounded', style: { backgroundColor: row.color || '#0ea5e9' } })
  },
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

onMounted(() => loadTags())

async function loadTags() {
  loading.value = true
  try {
    tags.value = await tagsApi.getList()
  } catch (error) {
    message.error('加载标签列表失败')
  } finally {
    loading.value = false
  }
}

function handleCreate() {
  isEdit.value = false
  editId.value = null
  formValue.value = { name: '', slug: '', color: '#0ea5e9' }
  showModal.value = true
}

function handleEdit(tag: Tag) {
  isEdit.value = true
  editId.value = tag.id
  formValue.value = { name: tag.name, slug: tag.slug, color: tag.color || '#0ea5e9' }
  showModal.value = true
}

async function handleSubmit() {
  try {
    await formRef.value?.validate()
    modalLoading.value = true

    const data = {
      name: formValue.value.name,
      slug: formValue.value.slug || formValue.value.name.toLowerCase().replace(/\s+/g, '-'),
      color: formValue.value.color
    }

    if (isEdit.value && editId.value) {
      await tagsApi.update(editId.value, data)
      message.success('更新成功')
    } else {
      await tagsApi.create(data)
      message.success('创建成功')
    }

    showModal.value = false
    loadTags()
  } catch (error: any) {
    if (error?.detail) message.error(error.detail)
  } finally {
    modalLoading.value = false
  }
}

function handleDelete(tag: Tag) {
  dialog.warning({
    title: '确认删除',
    content: `确定要删除标签「${tag.name}」吗？`,
    positiveText: '删除',
    negativeText: '取消',
    onPositiveClick: async () => {
      try {
        await tagsApi.delete(tag.id)
        message.success('删除成功')
        loadTags()
      } catch (error) {
        message.error('删除失败')
      }
    }
  })
}
</script>

<template>
  <NCard title="标签管理">
    <template #header-extra>
      <NButton type="primary" @click="handleCreate">
        <template #icon><NIcon><AddOutline /></NIcon></template>
        添加标签
      </NButton>
    </template>

    <NDataTable :columns="columns" :data="tags" :loading="loading" :bordered="false" />

    <NModal v-model:show="showModal" :title="isEdit ? '编辑标签' : '添加标签'" preset="dialog" style="width: 500px">
      <NForm ref="formRef" :model="formValue" :rules="rules" label-placement="top">
        <NFormItem path="name" label="名称">
          <NInput v-model:value="formValue.name" placeholder="请输入标签名称" />
        </NFormItem>
        <NFormItem path="slug" label="Slug">
          <NInput v-model:value="formValue.slug" placeholder="留空自动生成" />
        </NFormItem>
        <NFormItem path="color" label="颜色">
          <NColorPicker v-model:value="formValue.color" :show-alpha="false" />
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
