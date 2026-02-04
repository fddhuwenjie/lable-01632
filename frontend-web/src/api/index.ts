import axios, { AxiosError } from 'axios'

// API 错误类型
export interface ApiError {
  error: boolean
  error_code: string
  detail: string
  path?: string
}

// 错误码映射
const ERROR_MESSAGES: Record<string, string> = {
  UNAUTHORIZED: '登录已过期，请重新登录',
  FORBIDDEN: '没有权限执行此操作',
  NOT_FOUND: '请求的资源不存在',
  VALIDATION_ERROR: '数据验证失败',
  INTERNAL_ERROR: '服务器错误，请稍后重试',
  NETWORK_ERROR: '网络连接失败，请检查网络',
  TIMEOUT: '请求超时，请稍后重试'
}

// 获取友好错误信息
export function getErrorMessage(error: unknown): string {
  if (axios.isAxiosError(error)) {
    const axiosError = error as AxiosError<ApiError>
    
    if (!axiosError.response) {
      if (axiosError.code === 'ECONNABORTED') {
        return ERROR_MESSAGES.TIMEOUT
      }
      return ERROR_MESSAGES.NETWORK_ERROR
    }
    
    const data = axiosError.response.data
    if (data?.detail) {
      return data.detail
    }
    if (data?.error_code && ERROR_MESSAGES[data.error_code]) {
      return ERROR_MESSAGES[data.error_code]
    }
    
    const status = axiosError.response.status
    if (status === 401) return ERROR_MESSAGES.UNAUTHORIZED
    if (status === 403) return ERROR_MESSAGES.FORBIDDEN
    if (status === 404) return ERROR_MESSAGES.NOT_FOUND
    if (status >= 500) return ERROR_MESSAGES.INTERNAL_ERROR
  }
  
  if (error instanceof Error) {
    return error.message
  }
  
  return '发生未知错误'
}

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

api.interceptors.response.use(
  (response) => response.data,
  (error: AxiosError<ApiError>) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      if (!window.location.pathname.includes('/login')) {
        window.location.href = '/login'
      }
    }
    
    if (import.meta.env.DEV) {
      console.error('[API Error]', {
        url: error.config?.url,
        method: error.config?.method,
        status: error.response?.status,
        data: error.response?.data
      })
    }
    
    return Promise.reject(error)
  }
)

// Types
export interface User {
  id: number
  username: string
  email: string
  role: 'admin' | 'user'
  avatar?: string
  created_at: string
}

export interface Article {
  id: number
  title: string
  slug: string
  summary: string
  content: string
  cover_image?: string
  category_id: number
  category?: Category
  tags: Tag[]
  author: User
  views: number
  status: 'draft' | 'published'
  created_at: string
  updated_at: string
}

export interface Category {
  id: number
  name: string
  slug: string
  description?: string
  article_count?: number
}

export interface Tag {
  id: number
  name: string
  slug: string
  color?: string
  article_count?: number
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  page_size: number
  pages: number
}

// Auth API
export const authApi = {
  login: (data: { username: string; password: string }): Promise<{ access_token: string; token_type: string }> =>
    api.post('/auth/login', data),
  register: (data: { username: string; email: string; password: string }): Promise<User> =>
    api.post('/auth/register', data),
  getCurrentUser: (): Promise<User> => api.get('/auth/me')
}

// Articles API
export const articlesApi = {
  getList: (params?: { page?: number; page_size?: number; category_id?: number; tag_id?: number; status?: string }): Promise<PaginatedResponse<Article>> =>
    api.get('/articles', { params }),
  getById: (id: number): Promise<Article> => api.get(`/articles/${id}`),
  getRecent: (limit?: number): Promise<Article[]> => api.get('/articles/recent', { params: { limit } })
}

// Categories API
export const categoriesApi = {
  getList: (): Promise<Category[]> => api.get('/categories')
}

// Tags API
export const tagsApi = {
  getList: (): Promise<Tag[]> => api.get('/tags')
}

// Site Settings
export interface SiteSettings {
  site_name: string
  site_description: string
  site_keywords: string
  author_name: string
  author_bio: string
  author_avatar: string
  github_url: string
  email: string
}

export const settingsApi = {
  get: (): Promise<SiteSettings> => api.get('/settings')
}

export default api
