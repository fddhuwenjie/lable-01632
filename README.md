# Blog System - 现代化博客系统

## How to Run

### 🐳 Docker 启动（推荐）

```bash
# 1. 克隆项目
git clone <repository-url>
cd p-1632

# 2. 一键启动所有服务
docker compose up --build -d

# 3. 查看容器状态
docker compose ps

# 4. 查看日志（可选）
docker compose logs -f

# 5. 停止服务
docker compose down
```

**启动成功后访问：**
- 🌐 博客前台: http://localhost:8081
- 🔧 后台管理: http://localhost:8082
- 📚 API 文档: http://localhost:8080/docs

---

### 💻 本地开发启动

#### 前置要求
- Node.js >= 18
- Python >= 3.11
- PostgreSQL >= 15

#### 1. 启动数据库

```bash
# 使用 Docker 启动 PostgreSQL（推荐）
docker run -d \
  --name blog-postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=blog \
  -p 5432:5432 \
  postgres:15-alpine
```

#### 2. 启动后端

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量（可选，使用默认值）
export DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/blog"

# 启动服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

后端启动后访问: http://localhost:8000/docs

#### 3. 启动博客前台

```bash
cd frontend-web

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

博客前台启动后访问: http://localhost:5173

#### 4. 启动后台管理

```bash
cd frontend-admin

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

后台管理启动后访问: http://localhost:5174

## Services

| 服务 | 端口 | 说明 |
|------|------|------|
| Web (博客前台) | 8081 | Vue 3 博客展示页面 |
| Admin (后台管理) | 8082 | Vue 3 后台管理系统 |
| Backend | 8080 | FastAPI 后端 API |
| Database | 5432 (内部) | PostgreSQL 数据库 |

## 测试账号

| 角色 | 用户名 | 密码 |
|------|--------|------|
| 管理员 | admin | admin123 |

> 注意：首次启动时会自动创建管理员账号和示例数据

## 题目内容

本项目是一个完整的博客系统，已拆分为两个独立的前端项目：

### 博客前台 (frontend-web/)
- 博客首页（模仿 jiewen.run 风格设计）
- 文章列表与详情页
- 标签云页面
- 关于页面
- 用户注册与登录

### 后台管理 (frontend-admin/)
- 仪表盘（统计数据展示）
- 文章管理（创建、编辑、删除、发布）
- 分类管理
- 标签管理
- 用户管理（权限控制）
- 系统设置

---

## 技术栈

### 前端 (frontend-web/ & frontend-admin/)
- **Vue 3** - 渐进式 JavaScript 框架
- **TypeScript** - 类型安全的 JavaScript
- **Vite** - 下一代前端构建工具
- **Naive UI** - Vue 3 组件库
- **Tailwind CSS** - 原子化 CSS 框架
- **Pinia** - Vue 状态管理
- **Vue Router** - 官方路由

### 后端 (backend/)
- **FastAPI** - 现代 Python Web 框架
- **SQLAlchemy** - Python ORM
- **PostgreSQL** - 关系型数据库
- **JWT** - 身份认证
- **Pydantic** - 数据验证

### DevOps
- **Docker** - 容器化
- **Docker Compose** - 容器编排
- **Nginx** - Web 服务器 / 反向代理

## 项目结构

```
├── frontend-web/             # 博客前台项目
│   ├── src/
│   │   ├── api/             # API 接口
│   │   ├── layouts/         # 布局组件
│   │   ├── router/          # 路由配置
│   │   ├── stores/          # 状态管理
│   │   ├── styles/          # 样式文件
│   │   └── views/           # 页面组件
│   ├── Dockerfile
│   └── nginx.conf
├── frontend-admin/           # 后台管理项目
│   ├── src/
│   │   ├── api/             # API 接口
│   │   ├── layouts/         # 布局组件
│   │   ├── router/          # 路由配置
│   │   ├── stores/          # 状态管理
│   │   ├── styles/          # 样式文件
│   │   └── views/           # 页面组件
│   ├── Dockerfile
│   └── nginx.conf
├── backend/                  # 后端项目
│   ├── app/
│   │   ├── api/             # API 路由
│   │   ├── core/            # 核心配置
│   │   ├── models/          # 数据模型
│   │   └── schemas/         # Pydantic 模式
│   ├── Dockerfile
│   └── requirements.txt
├── docker-compose.yml
├── .gitignore
└── README.md
```

## 功能特性

### 🎨 现代化 UI
- 深色主题设计
- 响应式布局
- 流畅的动画效果
- 玻璃拟态风格

### 🔐 完整的权限系统
- JWT 身份认证
- 角色权限控制（管理员/普通用户）
- 路由守卫

### 📝 丰富的编辑功能
- Markdown 编辑器
- 代码语法高亮
- 封面图片支持

### 🏷️ 灵活的分类系统
- 多级分类
- 标签管理
- 标签云展示

## 环境变量

后端支持以下环境变量配置：

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| DATABASE_URL | postgresql+asyncpg://postgres:postgres@db:5432/blog | 数据库连接 |
| SECRET_KEY | your-super-secret-key-change-in-production | JWT 密钥 |
| ADMIN_USERNAME | admin | 管理员用户名 |
| ADMIN_EMAIL | admin@example.com | 管理员邮箱 |
| ADMIN_PASSWORD | admin123 | 管理员密码 |

## 许可证

MIT License
