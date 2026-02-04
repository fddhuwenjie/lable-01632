from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import engine, Base
from app.api import auth, articles, categories, tags, users, settings as settings_api, stats
from app.core.init_data import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await init_db()
    print("=" * 50)
    print("🚀 Startup Success")
    print(f"📦 Backend API: http://localhost:8000")
    print(f"📖 API Docs: http://localhost:8000/docs")
    print("=" * 50)
    yield
    # Shutdown
    await engine.dispose()


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Blog System API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
app.include_router(articles.router, prefix="/api/articles", tags=["文章"])
app.include_router(categories.router, prefix="/api/categories", tags=["分类"])
app.include_router(tags.router, prefix="/api/tags", tags=["标签"])
app.include_router(users.router, prefix="/api/users", tags=["用户"])
app.include_router(settings_api.router, prefix="/api/settings", tags=["设置"])
app.include_router(stats.router, prefix="/api/stats", tags=["统计"])


@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "Blog API is running"}
