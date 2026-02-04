from typing import Optional
from pydantic import BaseModel


class SiteSettingsUpdate(BaseModel):
    site_name: Optional[str] = None
    site_description: Optional[str] = None
    site_keywords: Optional[str] = None
    author_name: Optional[str] = None
    author_bio: Optional[str] = None
    author_avatar: Optional[str] = None
    github_url: Optional[str] = None
    email: Optional[str] = None


class SiteSettingsResponse(BaseModel):
    site_name: str
    site_description: Optional[str] = None
    site_keywords: Optional[str] = None
    author_name: Optional[str] = None
    author_bio: Optional[str] = None
    author_avatar: Optional[str] = None
    github_url: Optional[str] = None
    email: Optional[str] = None

    class Config:
        from_attributes = True
