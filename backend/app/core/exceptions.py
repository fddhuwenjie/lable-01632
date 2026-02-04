"""
统一异常处理模块
"""
from typing import Any, Optional
from fastapi import HTTPException, status


class AppException(HTTPException):
    """应用基础异常"""
    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: Optional[str] = None,
        headers: Optional[dict] = None
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        self.error_code = error_code or f"ERR_{status_code}"


class NotFoundError(AppException):
    """资源不存在"""
    def __init__(self, resource: str = "资源", detail: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail or f"{resource}不存在",
            error_code="NOT_FOUND"
        )


class UnauthorizedError(AppException):
    """未授权"""
    def __init__(self, detail: str = "请先登录"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            error_code="UNAUTHORIZED",
            headers={"WWW-Authenticate": "Bearer"}
        )


class ForbiddenError(AppException):
    """禁止访问"""
    def __init__(self, detail: str = "没有权限执行此操作"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
            error_code="FORBIDDEN"
        )


class BadRequestError(AppException):
    """请求错误"""
    def __init__(self, detail: str = "请求参数错误"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            error_code="BAD_REQUEST"
        )


class ConflictError(AppException):
    """资源冲突"""
    def __init__(self, detail: str = "资源已存在"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
            error_code="CONFLICT"
        )


class ValidationError(AppException):
    """验证错误"""
    def __init__(self, detail: str = "数据验证失败"):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            error_code="VALIDATION_ERROR"
        )
