from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import traceback

from app.core.config import settings
from app.core.database import engine, Base
from app.core.exceptions import AppException
from app.core.logger import logger, log_error, log_info
from app.api import auth, articles, categories, tags, users, settings as settings_api, stats
from app.core.init_data import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await init_db()
    log_info("服务启动成功", api_url="http://localhost:8000", docs_url="http://localhost:8000/docs")
    yield
    # Shutdown
    log_info("服务关闭")
    await engine.dispose()


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Blog System API",
    version="1.0.0",
    lifespan=lifespan
)


# 全局异常处理
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    log_error(
        f"应用异常: {exc.detail}",
        path=request.url.path,
        method=request.method,
        error_code=exc.error_code
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "error_code": exc.error_code,
            "detail": exc.detail,
            "path": request.url.path
        }
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    log_error(
        f"未处理异常: {str(exc)}",
        exc=exc,
        path=request.url.path,
        method=request.method,
        traceback=traceback.format_exc()
    )
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "error_code": "INTERNAL_ERROR",
            "detail": "服务器内部错误，请稍后重试",
            "path": request.url.path
        }
    )

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
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
