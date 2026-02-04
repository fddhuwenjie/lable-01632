from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal
from app.core.config import settings
from app.core.security import get_password_hash
from app.models.user import User
from app.models.category import Category
from app.models.tag import Tag
from app.models.article import Article
from app.models.settings import SiteSettings


async def init_db():
    async with AsyncSessionLocal() as db:
        # Check if admin exists
        result = await db.execute(select(User).where(User.username == settings.ADMIN_USERNAME))
        admin = result.scalar_one_or_none()
        
        if not admin:
            # Create admin user
            admin = User(
                username=settings.ADMIN_USERNAME,
                email=settings.ADMIN_EMAIL,
                hashed_password=get_password_hash(settings.ADMIN_PASSWORD),
                role="admin"
            )
            db.add(admin)
            await db.flush()
            
            # Create default categories
            categories = [
                Category(name="技术", slug="tech", description="技术相关文章"),
                Category(name="生活", slug="life", description="生活随笔"),
                Category(name="教程", slug="tutorial", description="教程指南"),
            ]
            for cat in categories:
                db.add(cat)
            await db.flush()
            
            # Create default tags
            tags = [
                Tag(name="Vue", slug="vue", color="#42b883"),
                Tag(name="Python", slug="python", color="#3776ab"),
                Tag(name="Docker", slug="docker", color="#2496ed"),
                Tag(name="FastAPI", slug="fastapi", color="#009688"),
                Tag(name="TypeScript", slug="typescript", color="#3178c6"),
            ]
            for tag in tags:
                db.add(tag)
            await db.flush()
            
            # Create sample article
            sample_article = Article(
                title="欢迎使用博客系统",
                slug="welcome",
                summary="这是一篇示例文章，展示博客系统的基本功能。",
                content="""# 欢迎使用博客系统

这是一个使用 **Vue 3** + **FastAPI** 构建的现代博客系统。

## 功能特性

- 📝 文章管理：创建、编辑、删除文章
- 🏷️ 标签系统：灵活的标签分类
- 👤 用户管理：多用户支持
- 🎨 现代化UI：深色主题，响应式设计

## 技术栈

### 前端
- Vue 3 + TypeScript
- Vite 构建工具
- Naive UI 组件库
- Tailwind CSS

### 后端
- FastAPI
- PostgreSQL
- SQLAlchemy

## 开始使用

1. 使用管理员账号登录
2. 进入后台管理
3. 开始创建您的第一篇文章

祝您使用愉快！
""",
                category_id=1,
                author_id=admin.id,
                status="published",
                views=0
            )
            db.add(sample_article)
            
            # Create site settings
            site_settings = SiteSettings(
                site_name="My Blog",
                site_description="一个使用 Vue 3 + FastAPI 构建的现代博客系统",
                site_keywords="博客,Vue,FastAPI,技术",
                author_name="Admin",
                author_bio="热爱技术的全栈开发者",
                author_avatar="",
                github_url="https://github.com",
                email="admin@example.com"
            )
            db.add(site_settings)
            
            await db.commit()
            print("✅ 初始化数据创建成功")
        else:
            print("ℹ️ 数据已存在，跳过初始化")
