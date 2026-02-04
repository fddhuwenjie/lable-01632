import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi, type User } from '@/api'
import { encryptPassword } from '@/utils/crypto'

export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('token'))

  const isLoggedIn = computed(() => !!token.value)

  async function login(username: string, password: string) {
    const encryptedPassword = await encryptPassword(password)
    const res = await authApi.login({ username, password: encryptedPassword })
    token.value = res.access_token
    localStorage.setItem('token', res.access_token)
    await fetchUser()
    return res
  }

  async function register(username: string, email: string, password: string) {
    const encryptedPassword = await encryptPassword(password)
    return authApi.register({ username, email, password: encryptedPassword })
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
