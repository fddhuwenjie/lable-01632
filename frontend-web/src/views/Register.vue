<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import { NForm, NFormItem, NInput, NButton, NCard, useMessage } from 'naive-ui'
import type { FormInst, FormRules } from 'naive-ui'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const message = useMessage()
const userStore = useUserStore()

const formRef = ref<FormInst | null>(null)
const loading = ref(false)
const formValue = ref({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const rules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度为3-20个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    {
      validator: (_rule, value) => value === formValue.value.password,
      message: '两次输入的密码不一致',
      trigger: 'blur'
    }
  ]
}

async function handleSubmit() {
  try {
    await formRef.value?.validate()
    loading.value = true
    
    await userStore.register(formValue.value.username, formValue.value.email, formValue.value.password)
    message.success('注册成功，请登录')
    router.push('/login')
  } catch (error: any) {
    message.error(error?.detail || '注册失败')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen bg-dark-bg flex items-center justify-center px-4">
    <div class="absolute inset-0 overflow-hidden">
      <div class="absolute top-1/4 right-1/4 w-96 h-96 bg-primary-500/10 rounded-full blur-3xl"></div>
      <div class="absolute bottom-1/4 left-1/4 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl"></div>
    </div>

    <NCard class="w-full max-w-md relative" :bordered="false">
      <div class="text-center mb-8">
        <RouterLink to="/" class="inline-block mb-6">
          <div class="w-16 h-16 mx-auto rounded-2xl bg-gradient-to-br from-primary-500 to-cyan-500 flex items-center justify-center text-white font-bold text-2xl">
            B
          </div>
        </RouterLink>
        <h1 class="text-2xl font-bold mb-2">创建账户</h1>
        <p class="text-dark-muted">注册以开始使用</p>
      </div>

      <NForm ref="formRef" :model="formValue" :rules="rules">
        <NFormItem path="username" label="用户名">
          <NInput v-model:value="formValue.username" placeholder="请输入用户名" size="large" />
        </NFormItem>
        <NFormItem path="email" label="邮箱">
          <NInput v-model:value="formValue.email" placeholder="请输入邮箱" size="large" />
        </NFormItem>
        <NFormItem path="password" label="密码">
          <NInput v-model:value="formValue.password" type="password" placeholder="请输入密码" size="large" show-password-on="click" />
        </NFormItem>
        <NFormItem path="confirmPassword" label="确认密码">
          <NInput v-model:value="formValue.confirmPassword" type="password" placeholder="请再次输入密码" size="large" show-password-on="click" @keydown.enter="handleSubmit" />
        </NFormItem>
        <NButton type="primary" block size="large" :loading="loading" @click="handleSubmit">
          注册
        </NButton>
      </NForm>

      <div class="mt-6 text-center text-dark-muted">
        已有账户？
        <RouterLink to="/login" class="text-primary-400 hover:text-primary-300">
          立即登录
        </RouterLink>
      </div>
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
