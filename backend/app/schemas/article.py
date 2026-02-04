from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

from app.schemas.category import CategoryResponse
from app.schemas.tag import TagResponse
from app.schemas.user import UserResponse


class TagInput(BaseModel):
    id: int


class ArticleCreate(BaseModel):
    title: str
    slug: Optional[str] = None
    summary: str
    content: str
    cover_image: Optional[str] = None
    category_id: int
    tags: Optional[List[TagInput]] = []
    status: str = "draft"


class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    summary: Optional[str] = None
    content: Optional[str] = None
    cover_image: Optional[str] = None
    category_id: Optional[int] = None
    tags: Optional[List[TagInput]] = None
    status: Optional[str] = None


class ArticleResponse(BaseModel):
    id: int
    title: str
    slug: str
    summary: str
    content: str
    cover_image: Optional[str] = None
    category_id: int
    category: Optional[CategoryResponse] = None
    author: Optional[UserResponse] = None
    tags: List[TagResponse] = []
    status: str
    views: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ArticleListResponse(BaseModel):
    id: int
    title: str
    slug: str
    summary: str
    cover_image: Optional[str] = None
    category: Optional[CategoryResponse] = None
    author: Optional[UserResponse] = None
    tags: List[TagResponse] = []
    status: str
    views: int
    created_at: datetime

    class Config:
        from_attributes = True
