import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi, type User, getErrorMessage } from '@/api'
import { encryptPassword } from '@/utils/crypto'

export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('token'))

  const isLoggedIn = computed(() => !!token.value)

  async function login(username: string, password: string) {
    try {
      const encryptedPassword = await encryptPassword(password)
      const res = await authApi.login({ username, password: encryptedPassword })
      token.value = res.access_token
      localStorage.setItem('token', res.access_token)
      await fetchUser()
      return res
    } catch (error) {
      throw new Error(getErrorMessage(error))
    }
  }

  async function register(username: string, email: string, password: string) {
    try {
      const encryptedPassword = await encryptPassword(password)
      return authApi.register({ username, email, password: encryptedPassword })
    } catch (error) {
      throw new Error(getErrorMessage(error))
    }
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
    localStorage.removeItem('token')
  }

  if (token.value) {
    fetchUser()
  }

  return {
    user,
    token,
    isLoggedIn,
    login,
    register,
    fetchUser,
    logout
  }
})
