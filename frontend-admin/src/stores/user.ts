import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi, type User, getErrorMessage } from '@/api'

export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('admin_token'))
  const loading = ref(false)
  const initialized = ref(false)

  const isLoggedIn = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.role === 'admin')

  async function login(username: string, password: string) {
    try {
      const res = await authApi.login({ username, password })
      token.value = res.access_token
      localStorage.setItem('admin_token', res.access_token)
      await fetchUser()
      return res
    } catch (error) {
      throw new Error(getErrorMessage(error))
    }
  }

  async function register(username: string, email: string, password: string) {
    try {
      return await authApi.register({ username, email, password })
    } catch (error) {
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

  const initPromise = token.value ? fetchUser() : Promise.resolve().then(() => { initialized.value = true })

  return {
    user,
    token,
    loading,
    initialized,
    isLoggedIn,
    isAdmin,
    login,
    register,
    fetchUser,
    logout,
    initPromise
  }
})
