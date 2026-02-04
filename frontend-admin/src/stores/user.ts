import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi, type User } from '@/api'
import { encryptPassword } from '@/utils/crypto'

export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('admin_token'))

  const isLoggedIn = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.role === 'admin')

  async function login(username: string, password: string) {
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
  }

  async function fetchUser() {
    if (!token.value) return
    try {
      user.value = await authApi.getCurrentUser()
    } catch {
      logout()
    }
  }

  function logout() {
    user.value = null
    token.value = null
    localStorage.removeItem('admin_token')
  }

  if (token.value) {
    fetchUser()
  }

  return {
    user,
    token,
    isLoggedIn,
    isAdmin,
    login,
    fetchUser,
    logout
  }
})
