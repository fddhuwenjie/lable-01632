from typing import Optional
from pydantic import BaseModel


class TagCreate(BaseModel):
    name: str
    slug: Optional[str] = None
    color: Optional[str] = "#0ea5e9"


class TagUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    color: Optional[str] = None


class TagResponse(BaseModel):
    id: int
    name: str
    slug: str
    color: Optional[str] = None
    article_count: int = 0

    class Config:
        from_attributes = True
