import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
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
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('admin_token')
      window.location.href = '/login'
    }
    return Promise.reject(error.response?.data || error)
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
  getCurrentUser: (): Promise<User> => api.get('/auth/me')
}

// Articles API
export const articlesApi = {
  getList: (params?: { page?: number; page_size?: number; category_id?: number; tag_id?: number; status?: string }): Promise<PaginatedResponse<Article>> =>
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

export default api
