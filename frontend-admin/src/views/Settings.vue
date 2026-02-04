<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { NCard, NForm, NFormItem, NInput, NButton, useMessage } from 'naive-ui'
import type { FormInst } from 'naive-ui'
import { settingsApi, type SiteSettings } from '@/api'

const message = useMessage()
const formRef = ref<FormInst | null>(null)
const loading = ref(true)
const saving = ref(false)

const formValue = ref<SiteSettings>({
  site_name: '',
  site_description: '',
  site_keywords: '',
  author_name: '',
  author_bio: '',
  author_avatar: '',
  github_url: '',
  email: ''
})

onMounted(async () => {
  try {
    formValue.value = await settingsApi.get()
  } catch (error) {
    console.error('Failed to load settings:', error)
  } finally {
    loading.value = false
  }
})

async function handleSave() {
  try {
    saving.value = true
    await settingsApi.update(formValue.value)
    message.success('保存成功')
  } catch (error: any) {
    message.error(error?.detail || '保存失败')
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <div class="space-y-6">
    <NCard title="网站设置" :loading="loading">
      <NForm ref="formRef" :model="formValue" label-placement="top">
        <NFormItem label="网站名称">
          <NInput v-model:value="formValue.site_name" placeholder="请输入网站名称" />
        </NFormItem>

        <NFormItem label="网站描述">
          <NInput v-model:value="formValue.site_description" type="textarea" placeholder="请输入网站描述" :rows="3" />
        </NFormItem>

        <NFormItem label="网站关键词">
          <NInput v-model:value="formValue.site_keywords" placeholder="多个关键词用逗号分隔" />
        </NFormItem>
      </NForm>
    </NCard>

    <NCard title="作者信息" :loading="loading">
      <NForm :model="formValue" label-placement="top">
        <NFormItem label="作者名称">
          <NInput v-model:value="formValue.author_name" placeholder="请输入作者名称" />
        </NFormItem>

        <NFormItem label="作者简介">
          <NInput v-model:value="formValue.author_bio" type="textarea" placeholder="请输入作者简介" :rows="3" />
        </NFormItem>
      </NForm>
    </NCard>

    <NCard title="联系方式" :loading="loading">
      <NForm :model="formValue" label-placement="top">
        <NFormItem label="联系邮箱">
          <NInput v-model:value="formValue.email" placeholder="请输入联系邮箱" />
        </NFormItem>
      </NForm>
    </NCard>

    <div class="flex justify-end">
      <NButton type="primary" size="large" :loading="saving" @click="handleSave">
        保存设置
      </NButton>
    </div>
  </div>
</template>
