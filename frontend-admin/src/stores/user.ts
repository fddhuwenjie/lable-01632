import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi, type User, getErrorMessage } from '@/api'
import { encryptPassword } from '@/utils/crypto'

export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('admin_token'))
  const loading = ref(false)
  const initialized = ref(false)

  const isLoggedIn = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.role === 'admin')

  async function login(username: string, password: string) {
    try {
      // RSA 加密密码
      const encryptedPassword = await encryptPassword(password)
      const res = await authApi.login({ username, password: encryptedPassword })
      token.value = res.access_token
      localStorage.setItem('admin_token', res.access_token)
      await fetchUser()
      
      if (user.value?.role !== 'admin') {
        logout()
        throw new Error('权限不足，只有管理员可以登录')
      }
      
      return res
    } catch (error) {
      // 使用友好的错误信息
      throw new Error(getErrorMessage(error))
    }
  }

  async function fetchUser() {
    if (!token.value) {
      initialized.value = true
      return
    }
    loading.value = true
    try {
      user.value = await authApi.getCurrentUser()
    } catch {
      // token 无效，清除
      token.value = null
      user.value = null
      localStorage.removeItem('admin_token')
    } finally {
      loading.value = false
      initialized.value = true
    }
  }

  function logout() {
    user.value = null
    token.value = null
    localStorage.removeItem('admin_token')
  }

  // 初始化时获取用户信息
  const initPromise = token.value ? fetchUser() : Promise.resolve().then(() => { initialized.value = true })

  return {
    user,
    token,
    loading,
    initialized,
    isLoggedIn,
    isAdmin,
    login,
    fetchUser,
    logout,
    initPromise
  }
})
