<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { NForm, NFormItem, NInput, NButton, NIcon, useMessage } from 'naive-ui'
import type { FormInst, FormRules } from 'naive-ui'
import { PersonOutline, LockClosedOutline, RocketOutline } from '@vicons/ionicons5'
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

// 动态背景粒子
const particles = ref<Array<{ id: number; x: number; y: number; size: number; speed: number; opacity: number }>>([])

onMounted(() => {
  // 生成粒子
  for (let i = 0; i < 50; i++) {
    particles.value.push({
      id: i,
      x: Math.random() * 100,
      y: Math.random() * 100,
      size: Math.random() * 4 + 1,
      speed: Math.random() * 0.5 + 0.1,
      opacity: Math.random() * 0.5 + 0.1
    })
  }
})

async function handleSubmit() {
  try {
    await formRef.value?.validate()
    loading.value = true
    
    await userStore.login(formValue.value.username, formValue.value.password)
    message.success('登录成功，欢迎回来！')
    
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
  <div class="login-container">
    <!-- 动态背景 -->
    <div class="bg-animation">
      <div class="gradient-orb orb-1"></div>
      <div class="gradient-orb orb-2"></div>
      <div class="gradient-orb orb-3"></div>
      <div class="grid-overlay"></div>
    </div>

    <!-- 粒子效果 -->
    <div class="particles">
      <div
        v-for="p in particles"
        :key="p.id"
        class="particle"
        :style="{
          left: p.x + '%',
          top: p.y + '%',
          width: p.size + 'px',
          height: p.size + 'px',
          opacity: p.opacity,
          animationDuration: (10 / p.speed) + 's'
        }"
      ></div>
    </div>

    <!-- 登录卡片 -->
    <div class="login-wrapper">
      <div class="login-card">
        <!-- Logo 区域 -->
        <div class="logo-section">
          <div class="logo-icon">
            <NIcon size="32" color="#fff"><RocketOutline /></NIcon>
          </div>
          <h1 class="logo-title">Blog Admin</h1>
          <p class="logo-subtitle">内容管理系统</p>
        </div>

        <!-- 分隔线 -->
        <div class="divider">
          <span>账号登录</span>
        </div>

        <!-- 表单 -->
        <NForm ref="formRef" :model="formValue" :rules="rules" class="login-form">
          <NFormItem path="username">
            <NInput
              v-model:value="formValue.username"
              placeholder="请输入用户名"
              size="large"
              @keydown.enter="handleSubmit"
            >
              <template #prefix>
                <NIcon :component="PersonOutline" class="input-icon" />
              </template>
            </NInput>
          </NFormItem>
          
          <NFormItem path="password">
            <NInput
              v-model:value="formValue.password"
              type="password"
              placeholder="请输入密码"
              size="large"
              show-password-on="click"
              @keydown.enter="handleSubmit"
            >
              <template #prefix>
                <NIcon :component="LockClosedOutline" class="input-icon" />
              </template>
            </NInput>
          </NFormItem>

          <NButton
            type="primary"
            block
            size="large"
            :loading="loading"
            class="login-btn"
            @click="handleSubmit"
          >
            <template #icon>
              <NIcon v-if="!loading"><RocketOutline /></NIcon>
            </template>
            {{ loading ? '登录中...' : '立即登录' }}
          </NButton>
        </NForm>

        <!-- 底部信息 -->
        <div class="footer-info">
          <p>默认账号: admin / admin123</p>
        </div>
      </div>

      <!-- 装饰元素 -->
      <div class="decoration decoration-1"></div>
      <div class="decoration decoration-2"></div>
    </div>
  </div>
</template>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #0a0a0f;
  position: relative;
  overflow: hidden;
}

/* 动态背景 */
.bg-animation {
  position: absolute;
  inset: 0;
  overflow: hidden;
}

.gradient-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  animation: float 20s ease-in-out infinite;
}

.orb-1 {
  width: 600px;
  height: 600px;
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.4), rgba(139, 92, 246, 0.2));
  top: -200px;
  left: -100px;
}

.orb-2 {
  width: 500px;
  height: 500px;
  background: linear-gradient(135deg, rgba(6, 182, 212, 0.3), rgba(59, 130, 246, 0.2));
  bottom: -150px;
  right: -100px;
  animation-delay: -5s;
}

.orb-3 {
  width: 400px;
  height: 400px;
  background: linear-gradient(135deg, rgba(236, 72, 153, 0.2), rgba(168, 85, 247, 0.15));
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation-delay: -10s;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  25% { transform: translate(30px, -30px) scale(1.05); }
  50% { transform: translate(-20px, 20px) scale(0.95); }
  75% { transform: translate(-30px, -20px) scale(1.02); }
}

.grid-overlay {
  position: absolute;
  inset: 0;
  background-image: 
    linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
  background-size: 50px 50px;
}

/* 粒子效果 */
.particles {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.particle {
  position: absolute;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 50%;
  animation: twinkle 3s ease-in-out infinite;
}

@keyframes twinkle {
  0%, 100% { opacity: 0.1; transform: scale(1); }
  50% { opacity: 0.6; transform: scale(1.2); }
}

/* 登录卡片容器 */
.login-wrapper {
  position: relative;
  z-index: 10;
}

.login-card {
  width: 420px;
  padding: 48px 40px;
  background: rgba(15, 15, 23, 0.8);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 24px;
  box-shadow: 
    0 25px 50px -12px rgba(0, 0, 0, 0.5),
    0 0 0 1px rgba(255, 255, 255, 0.05) inset;
}

/* Logo 区域 */
.logo-section {
  text-align: center;
  margin-bottom: 32px;
}

.logo-icon {
  width: 72px;
  height: 72px;
  margin: 0 auto 16px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6, #a855f7);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 10px 40px -10px rgba(139, 92, 246, 0.5);
  animation: pulse-glow 3s ease-in-out infinite;
}

@keyframes pulse-glow {
  0%, 100% { box-shadow: 0 10px 40px -10px rgba(139, 92, 246, 0.5); }
  50% { box-shadow: 0 10px 60px -10px rgba(139, 92, 246, 0.8); }
}

.logo-title {
  font-size: 28px;
  font-weight: 700;
  background: linear-gradient(135deg, #fff, #a5b4fc);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 8px;
}

.logo-subtitle {
  color: rgba(255, 255, 255, 0.5);
  font-size: 14px;
}

/* 分隔线 */
.divider {
  display: flex;
  align-items: center;
  margin-bottom: 28px;
}

.divider::before,
.divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
}

.divider span {
  padding: 0 16px;
  color: rgba(255, 255, 255, 0.4);
  font-size: 13px;
}

/* 表单样式 */
.login-form {
  margin-bottom: 24px;
}

.input-icon {
  color: rgba(255, 255, 255, 0.4);
}

:deep(.n-input) {
  --n-border-radius: 12px !important;
  --n-height: 48px !important;
  --n-color: rgba(255, 255, 255, 0.05) !important;
  --n-color-focus: rgba(255, 255, 255, 0.08) !important;
  --n-border: 1px solid rgba(255, 255, 255, 0.1) !important;
  --n-border-hover: 1px solid rgba(139, 92, 246, 0.5) !important;
  --n-border-focus: 1px solid rgba(139, 92, 246, 0.8) !important;
  --n-box-shadow-focus: 0 0 0 2px rgba(139, 92, 246, 0.2) !important;
}

:deep(.n-form-item) {
  --n-label-text-color: rgba(255, 255, 255, 0.7) !important;
  --n-feedback-text-color-error: #f87171 !important;
}

:deep(.n-form-item-blank) {
  min-height: 48px;
}

.login-btn {
  height: 48px !important;
  border-radius: 12px !important;
  font-size: 16px !important;
  font-weight: 600 !important;
  background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
  border: none !important;
  box-shadow: 0 10px 30px -10px rgba(139, 92, 246, 0.5) !important;
  transition: all 0.3s ease !important;
}

.login-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 15px 40px -10px rgba(139, 92, 246, 0.6) !important;
}

.login-btn:active {
  transform: translateY(0);
}

/* 底部信息 */
.footer-info {
  text-align: center;
  padding-top: 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.footer-info p {
  color: rgba(255, 255, 255, 0.3);
  font-size: 13px;
}

/* 装饰元素 */
.decoration {
  position: absolute;
  border-radius: 50%;
  pointer-events: none;
}

.decoration-1 {
  width: 200px;
  height: 200px;
  border: 1px solid rgba(139, 92, 246, 0.2);
  top: -80px;
  right: -80px;
  animation: rotate 20s linear infinite;
}

.decoration-2 {
  width: 150px;
  height: 150px;
  border: 1px dashed rgba(99, 102, 241, 0.2);
  bottom: -60px;
  left: -60px;
  animation: rotate 15s linear infinite reverse;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* 响应式 */
@media (max-width: 480px) {
  .login-card {
    width: calc(100vw - 32px);
    padding: 32px 24px;
    margin: 16px;
  }
  
  .logo-icon {
    width: 60px;
    height: 60px;
  }
  
  .logo-title {
    font-size: 24px;
  }
}
</style>
