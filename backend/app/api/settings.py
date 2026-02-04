from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import get_current_admin
from app.models.settings import SiteSettings
from app.models.user import User
from app.schemas.settings import SiteSettingsUpdate, SiteSettingsResponse

router = APIRouter()


@router.get("", response_model=SiteSettingsResponse)
async def get_settings(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(SiteSettings))
    settings = result.scalar_one_or_none()
    
    if not settings:
        # Return default settings
        return SiteSettingsResponse(
            site_name="My Blog",
            site_description="A modern blog system",
            site_keywords="blog,vue,fastapi",
            author_name="Admin",
            author_bio="",
            author_avatar="",
            github_url="",
            email=""
        )
    
    return settings


@router.put("", response_model=SiteSettingsResponse)
async def update_settings(
    settings_data: SiteSettingsUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    result = await db.execute(select(SiteSettings))
    settings = result.scalar_one_or_none()
    
    if not settings:
        settings = SiteSettings()
        db.add(settings)
    
    update_data = settings_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(settings, field, value)
    
    await db.flush()
    await db.refresh(settings)
    return settings
