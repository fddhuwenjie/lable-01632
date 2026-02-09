import axios, { AxiosError } from 'axios'

// API 错误类型
export interface ApiError {
  error: boolean
  error_code: string
  detail: string
  path?: string
}

// 错误码映射 - 更完善的错误提示
const ERROR_MESSAGES: Record<string, string> = {
  // 认证相关
  UNAUTHORIZED: '登录已过期，请重新登录',
  FORBIDDEN: '没有权限执行此操作',
  INVALID_CREDENTIALS: '用户名或密码错误',
  TOKEN_EXPIRED: '登录已过期，请重新登录',
  
  // 资源相关
  NOT_FOUND: '请求的资源不存在',
  CONFLICT: '资源已存在',
  ALREADY_EXISTS: '该数据已存在',
  
  // 数据验证
  VALIDATION_ERROR: '数据验证失败，请检查输入',
  INVALID_INPUT: '输入数据格式不正确',
  
  // 服务器错误
  INTERNAL_ERROR: '服务器繁忙，请稍后重试',
  DATABASE_ERROR: '数据库操作失败，请稍后重试',
  
  // 网络错误
  NETWORK_ERROR: '网络连接失败，请检查网络设置',
  TIMEOUT: '请求超时，请检查网络后重试',
  CONNECTION_REFUSED: '无法连接到服务器',
  
  // 业务错误
  CANNOT_DELETE_ADMIN: '不能删除超级管理员',
  CANNOT_MODIFY_ADMIN: '不能修改超级管理员',
  CATEGORY_HAS_ARTICLES: '该分类下还有文章，无法删除',
  TAG_HAS_ARTICLES: '该标签下还有文章，无法删除'
}

// HTTP 状态码对应的友好提示
const HTTP_STATUS_MESSAGES: Record<number, string> = {
  400: '请求参数错误',
  401: '请先登录',
  403: '没有操作权限',
  404: '请求的内容不存在',
  405: '请求方法不允许',
  408: '请求超时',
  409: '数据冲突',
  413: '上传的文件太大',
  422: '数据验证失败',
  429: '请求太频繁，请稍后再试',
  500: '服务器内部错误',
  502: '网关错误',
  503: '服务暂时不可用',
  504: '网关超时'
}

// 获取友好错误信息
export function getErrorMessage(error: unknown): string {
  if (axios.isAxiosError(error)) {
    const axiosError = error as AxiosError<ApiError>
    
    // 网络错误（无响应）
    if (!axiosError.response) {
      if (axiosError.code === 'ECONNABORTED') {
        return ERROR_MESSAGES.TIMEOUT
      }
      if (axiosError.code === 'ERR_NETWORK') {
        return ERROR_MESSAGES.NETWORK_ERROR
      }
      if (axiosError.message?.includes('Network Error')) {
        return ERROR_MESSAGES.CONNECTION_REFUSED
      }
      return ERROR_MESSAGES.NETWORK_ERROR
    }
    
    // API 返回的错误
    const data = axiosError.response.data
    if (data?.detail) {
      // 优先使用后端返回的具体错误信息
      return data.detail
    }
    if (data?.error_code && ERROR_MESSAGES[data.error_code]) {
      return ERROR_MESSAGES[data.error_code]
    }
    
    // HTTP 状态码错误
    const status = axiosError.response.status
    if (HTTP_STATUS_MESSAGES[status]) {
      return HTTP_STATUS_MESSAGES[status]
    }
    
    // 通用错误
    if (status >= 500) return ERROR_MESSAGES.INTERNAL_ERROR
  }
  
  if (error instanceof Error) {
    return error.message
  }
  
  return '发生未知错误，请稍后重试'
}

// 判断是否为网络错误（可重试）
export function isNetworkError(error: unknown): boolean {
  if (axios.isAxiosError(error)) {
    return !error.response || error.code === 'ECONNABORTED' || error.code === 'ERR_NETWORK'
  }
  return false
}

// 判断是否为认证错误
export function isAuthError(error: unknown): boolean {
  if (axios.isAxiosError(error)) {
    return error.response?.status === 401
  }
  return false
}

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('admin_token')
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
    // 401 自动跳转登录
    if (error.response?.status === 401) {
      localStorage.removeItem('admin_token')
      // 避免在登录页循环跳转
      if (!window.location.pathname.includes('/login')) {
        window.location.href = '/login'
      }
    }
    
    // 开发环境打印错误详情
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
  getList: (params?: { page?: number; page_size?: number; category_id?: number; tag_id?: number; status?: string; my_articles?: boolean }): Promise<PaginatedResponse<Article>> =>
    api.get('/articles', { params }),
  getById: (id: number): Promise<Article> => api.get(`/articles/${id}`),
  create: (data: Partial<Article>): Promise<Article> => api.post('/articles', data),
  update: (id: number, data: Partial<Article>): Promise<Article> => api.put(`/articles/${id}`, data),
  delete: (id: number): Promise<void> => api.delete(`/articles/${id}`)
}

// Categories API
export const categoriesApi = {
  getList: (): Promise<Category[]> => api.get('/categories'),
  getById: (id: number): Promise<Category> => api.get(`/categories/${id}`),
  create: (data: Partial<Category>): Promise<Category> => api.post('/categories', data),
  update: (id: number, data: Partial<Category>): Promise<Category> => api.put(`/categories/${id}`, data),
  delete: (id: number): Promise<void> => api.delete(`/categories/${id}`)
}

// Tags API
export const tagsApi = {
  getList: (): Promise<Tag[]> => api.get('/tags'),
  getById: (id: number): Promise<Tag> => api.get(`/tags/${id}`),
  create: (data: Partial<Tag>): Promise<Tag> => api.post('/tags', data),
  update: (id: number, data: Partial<Tag>): Promise<Tag> => api.put(`/tags/${id}`, data),
  delete: (id: number): Promise<void> => api.delete(`/tags/${id}`)
}

// Users API
export const usersApi = {
  getList: (params?: { page?: number; page_size?: number }): Promise<PaginatedResponse<User>> =>
    api.get('/users', { params }),
  getById: (id: number): Promise<User> => api.get(`/users/${id}`),
  create: (data: { username: string; email: string; password: string; role?: 'admin' | 'user' }): Promise<User> =>
    api.post('/users', data),
  update: (id: number, data: Partial<User>): Promise<User> => api.put(`/users/${id}`, data),
  delete: (id: number): Promise<void> => api.delete(`/users/${id}`),
  updateRole: (id: number, role: 'admin' | 'user'): Promise<User> => api.patch(`/users/${id}/role`, { role })
}

// Settings API
export const settingsApi = {
  get: (): Promise<SiteSettings> => api.get('/settings'),
  update: (data: Partial<SiteSettings>): Promise<SiteSettings> => api.put('/settings', data)
}

// Stats API
export const statsApi = {
  getDashboard: (): Promise<{
    total_articles: number
    total_users: number
    total_views: number
    total_tags: number
    recent_articles: Article[]
    popular_articles: Article[]
  }> => api.get('/stats/dashboard')
}

// Upload API
export const uploadApi = {
  uploadImage: async (file: File): Promise<{ url: string }> => {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/upload/image', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  }
}

export default api
