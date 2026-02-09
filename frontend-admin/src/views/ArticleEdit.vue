<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { NCard, NForm, NFormItem, NInput, NSelect, NButton, NSpace, useMessage } from 'naive-ui'
import type { FormInst, FormRules } from 'naive-ui'
import { MdEditor } from 'md-editor-v3'
import 'md-editor-v3/lib/style.css'
import { articlesApi, categoriesApi, tagsApi, uploadApi, type Article, type Category, type Tag, getErrorMessage } from '@/api'

const route = useRoute()
const router = useRouter()
const message = useMessage()

const isEdit = computed(() => !!route.params.id)
const articleId = computed(() => Number(route.params.id))

const formRef = ref<FormInst | null>(null)
const loading = ref(false)
const saving = ref(false)
const categories = ref<Category[]>([])
const tags = ref<Tag[]>([])

const formValue = ref({
  title: '',
  slug: '',
  summary: '',
  content: '',
  cover_image: '',
  category_id: null as number | null,
  tag_ids: [] as number[],
  status: 'draft' as 'draft' | 'published'
})

const rules: FormRules = {
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  summary: [{ required: true, message: '请输入摘要', trigger: 'blur' }],
  content: [{ required: true, message: '请输入内容', trigger: 'blur' }],
  category_id: [{ required: true, type: 'number', message: '请选择分类', trigger: 'change' }]
}

const categoryOptions = computed(() => categories.value.map(c => ({ label: c.name, value: c.id })))
const tagOptions = computed(() => tags.value.map(t => ({ label: t.name, value: t.id })))

// 图片上传处理
async function onUploadImg(files: File[], callback: (urls: string[]) => void) {
  const urls: string[] = []
  for (const file of files) {
    try {
      const res = await uploadApi.uploadImage(file)
      urls.push(res.url)
    } catch (error) {
      message.error(`上传失败: ${getErrorMessage(error)}`)
    }
  }
  callback(urls)
}

onMounted(async () => {
  await loadOptions()
  if (isEdit.value) {
    await loadArticle()
  }
})

async function loadOptions() {
  try {
    const [categoriesRes, tagsRes] = await Promise.all([categoriesApi.getList(), tagsApi.getList()])
    categories.value = categoriesRes
    tags.value = tagsRes
  } catch (error) {
    message.error(getErrorMessage(error))
  }
}

async function loadArticle() {
  loading.value = true
  try {
    const article = await articlesApi.getById(articleId.value)
    formValue.value = {
      title: article.title,
      slug: article.slug,
      summary: article.summary,
      content: article.content,
      cover_image: article.cover_image || '',
      category_id: article.category_id,
      tag_ids: article.tags.map(t => t.id),
      status: article.status
    }
  } catch (error) {
    message.error(getErrorMessage(error))
    router.push('/articles')
  } finally {
    loading.value = false
  }
}

async function handleSave(publish = false) {
  try {
    await formRef.value?.validate()
  } catch {
    message.warning('请填写必填项')
    return
  }
  
  saving.value = true
  try {
    const data: Partial<Article> = {
      title: formValue.value.title,
      slug: formValue.value.slug || formValue.value.title.toLowerCase().replace(/\s+/g, '-'),
      summary: formValue.value.summary,
      content: formValue.value.content,
      cover_image: formValue.value.cover_image || undefined,
      category_id: formValue.value.category_id!,
      tags: formValue.value.tag_ids.map(id => ({ id } as Tag)),
      status: publish ? 'published' : 'draft'
    }

    if (isEdit.value) {
      await articlesApi.update(articleId.value, data)
      message.success('更新成功')
    } else {
      await articlesApi.create(data)
      message.success('创建成功')
    }

    router.push('/articles')
  } catch (error) {
    message.error(getErrorMessage(error))
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <NCard :title="isEdit ? '编辑文章' : '创建文章'" :loading="loading">
    <NForm ref="formRef" :model="formValue" :rules="rules" label-placement="top">
      <NFormItem path="title" label="标题">
        <NInput v-model:value="formValue.title" placeholder="请输入文章标题" />
      </NFormItem>

      <NFormItem path="slug" label="Slug (URL别名)">
        <NInput v-model:value="formValue.slug" placeholder="留空自动生成" />
      </NFormItem>

      <NFormItem path="summary" label="摘要">
        <NInput v-model:value="formValue.summary" type="textarea" placeholder="请输入文章摘要" :rows="3" />
      </NFormItem>

      <NFormItem path="content" label="内容 (Markdown)">
        <MdEditor
          v-model="formValue.content"
          theme="dark"
          :preview="true"
          style="height: 500px; width: 100%"
          placeholder="请输入文章内容，支持 Markdown 格式"
          @on-upload-img="onUploadImg"
        />
      </NFormItem>

      <NFormItem path="cover_image" label="封面图片 URL">
        <NInput v-model:value="formValue.cover_image" placeholder="请输入封面图片 URL (可选)" />
      </NFormItem>

      <NFormItem path="category_id" label="分类">
        <NSelect v-model:value="formValue.category_id" :options="categoryOptions" placeholder="请选择分类" />
      </NFormItem>

      <NFormItem path="tag_ids" label="标签">
        <NSelect v-model:value="formValue.tag_ids" :options="tagOptions" placeholder="请选择标签" multiple />
      </NFormItem>

      <NFormItem>
        <NSpace>
          <NButton @click="router.back()">取消</NButton>
          <NButton :loading="saving" @click="handleSave(false)">保存草稿</NButton>
          <NButton type="primary" :loading="saving" @click="handleSave(true)">保存并发布</NButton>
        </NSpace>
      </NFormItem>
    </NForm>
  </NCard>
</template>

<style scoped>
:deep(.md-editor) {
  --md-bk-color: #1a1a2e;
  border-radius: 8px;
}
</style>
