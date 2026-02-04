from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.core.security import get_current_admin
from app.models.user import User
from app.models.article import Article
from app.models.tag import Tag

router = APIRouter()


@router.get("/dashboard")
async def get_dashboard_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    # Total articles
    article_count = await db.execute(select(func.count(Article.id)))
    total_articles = article_count.scalar() or 0
    
    # Total users
    user_count = await db.execute(select(func.count(User.id)))
    total_users = user_count.scalar() or 0
    
    # Total views
    views_sum = await db.execute(select(func.sum(Article.views)))
    total_views = views_sum.scalar() or 0
    
    # Total tags
    tag_count = await db.execute(select(func.count(Tag.id)))
    total_tags = tag_count.scalar() or 0
    
    # Recent articles
    recent_query = select(Article).options(
        selectinload(Article.category),
        selectinload(Article.author),
        selectinload(Article.tags)
    ).order_by(desc(Article.created_at)).limit(5)
    recent_result = await db.execute(recent_query)
    recent_articles = recent_result.scalars().all()
    
    # Popular articles
    popular_query = select(Article).options(
        selectinload(Article.category),
        selectinload(Article.author),
        selectinload(Article.tags)
    ).where(Article.status == "published").order_by(desc(Article.views)).limit(5)
    popular_result = await db.execute(popular_query)
    popular_articles = popular_result.scalars().all()
    
    return {
        "total_articles": total_articles,
        "total_users": total_users,
        "total_views": total_views,
        "total_tags": total_tags,
        "recent_articles": recent_articles,
        "popular_articles": popular_articles
    }
