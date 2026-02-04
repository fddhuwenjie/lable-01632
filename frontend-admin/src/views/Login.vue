<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { NForm, NFormItem, NInput, NButton, NCard, useMessage } from 'naive-ui'
import type { FormInst, FormRules } from 'naive-ui'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const route = useRoute()
const message = useMessage()
const userStore = useUserStore()

const formRef = ref<FormInst | null>(null)
const loading = ref(false)
const formValue = ref({
  username: '',
  password: ''
})

const rules: FormRules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少6位', trigger: 'blur' }
  ]
}

async function handleSubmit() {
  try {
    await formRef.value?.validate()
    loading.value = true
    
    await userStore.login(formValue.value.username, formValue.value.password)
    message.success('登录成功')
    
    const redirect = route.query.redirect as string || '/'
    router.push(redirect)
  } catch (error: any) {
    message.error(error?.message || error?.detail || '登录失败')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen bg-dark-bg flex items-center justify-center px-4">
    <div class="absolute inset-0 overflow-hidden">
      <div class="absolute top-1/4 left-1/4 w-96 h-96 bg-violet-500/10 rounded-full blur-3xl"></div>
      <div class="absolute bottom-1/4 right-1/4 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl"></div>
    </div>

    <NCard class="w-full max-w-md relative" :bordered="false">
      <div class="text-center mb-8">
        <div class="w-16 h-16 mx-auto mb-6 rounded-2xl bg-gradient-to-br from-violet-500 to-indigo-500 flex items-center justify-center text-white font-bold text-2xl">
          A
        </div>
        <h1 class="text-2xl font-bold mb-2">后台管理系统</h1>
        <p class="text-dark-muted">请使用管理员账号登录</p>
      </div>

      <NForm ref="formRef" :model="formValue" :rules="rules">
        <NFormItem path="username" label="用户名">
          <NInput v-model:value="formValue.username" placeholder="请输入用户名" size="large" @keydown.enter="handleSubmit" />
        </NFormItem>
        <NFormItem path="password" label="密码">
          <NInput v-model:value="formValue.password" type="password" placeholder="请输入密码" size="large" show-password-on="click" @keydown.enter="handleSubmit" />
        </NFormItem>
        <NButton type="primary" block size="large" :loading="loading" @click="handleSubmit">
          登录
        </NButton>
      </NForm>
    </NCard>
  </div>
</template>

<style scoped>
:deep(.n-card) {
  background-color: rgba(22, 27, 34, 0.8);
  backdrop-filter: blur(20px);
  border: 1px solid #30363d;
}
</style>
