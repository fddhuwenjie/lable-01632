from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.core.security import get_current_user, get_optional_user
from app.models.user import User
from app.models.article import Article, article_tags
from app.models.tag import Tag
from app.models.category import Category
from app.schemas.article import ArticleCreate, ArticleUpdate, ArticleResponse, ArticleListResponse
from app.schemas.common import PaginatedResponse

router = APIRouter()


@router.get("", response_model=PaginatedResponse[ArticleListResponse])
async def get_articles(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    category_id: Optional[int] = None,
    tag_id: Optional[int] = None,
    status: Optional[str] = None,
    author_id: Optional[int] = None,
    my_articles: bool = Query(False, description="只获取当前用户的文章"),
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)
):
    query = select(Article).options(
        selectinload(Article.category),
        selectinload(Article.author),
        selectinload(Article.tags)
    )
    
    # 如果请求自己的文章
    if my_articles and current_user:
        query = query.where(Article.author_id == current_user.id)
        # 自己的文章可以看到所有状态
        if status:
            query = query.where(Article.status == status)
    elif author_id:
        query = query.where(Article.author_id == author_id)
        if status:
            query = query.where(Article.status == status)
        elif not current_user or current_user.role != "admin":
            query = query.where(Article.status == "published")
    else:
        # Filter by status (only show published to non-admins)
        if status:
            query = query.where(Article.status == status)
        elif not current_user or current_user.role != "admin":
            query = query.where(Article.status == "published")
    
    if category_id:
        query = query.where(Article.category_id == category_id)
    
    if tag_id:
        query = query.join(article_tags).where(article_tags.c.tag_id == tag_id)
    
    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # Paginate
    query = query.order_by(desc(Article.created_at))
    query = query.offset((page - 1) * page_size).limit(page_size)
    
    result = await db.execute(query)
    articles = result.scalars().all()
    
    return PaginatedResponse(
        items=[ArticleListResponse.model_validate(a) for a in articles],
        total=total,
        page=page,
        page_size=page_size,
        pages=(total + page_size - 1) // page_size
    )


@router.get("/recent", response_model=List[ArticleListResponse])
async def get_recent_articles(
    limit: int = Query(6, ge=1, le=20),
    db: AsyncSession = Depends(get_db)
):
    query = select(Article).options(
        selectinload(Article.category),
        selectinload(Article.author),
        selectinload(Article.tags)
    ).where(Article.status == "published").order_by(desc(Article.created_at)).limit(limit)
    
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{article_id}", response_model=ArticleResponse)
async def get_article(
    article_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)
):
    query = select(Article).options(
        selectinload(Article.category),
        selectinload(Article.author),
        selectinload(Article.tags)
    ).where(Article.id == article_id)
    
    result = await db.execute(query)
    article = result.scalar_one_or_none()
    
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")
    
    # Only admins can see draft articles
    if article.status != "published":
        if not current_user or current_user.role != "admin":
            raise HTTPException(status_code=404, detail="文章不存在")
    
    # Increment views
    article.views += 1
    await db.flush()
    
    return article


@router.post("", response_model=ArticleResponse)
async def create_article(
    article_data: ArticleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Generate slug if not provided
    slug = article_data.slug or article_data.title.lower().replace(" ", "-")
    
    # Check if slug exists
    result = await db.execute(select(Article).where(Article.slug == slug))
    if result.scalar_one_or_none():
        slug = f"{slug}-{int(func.now().compile())}"
    
    # Get tags
    tag_ids = [t.id for t in (article_data.tags or [])]
    tags = []
    if tag_ids:
        result = await db.execute(select(Tag).where(Tag.id.in_(tag_ids)))
        tags = result.scalars().all()
    
    article = Article(
        title=article_data.title,
        slug=slug,
        summary=article_data.summary,
        content=article_data.content,
        cover_image=article_data.cover_image,
        category_id=article_data.category_id,
        author_id=current_user.id,
        status=article_data.status,
        tags=list(tags)
    )
    db.add(article)
    await db.flush()
    
    # Reload with relationships
    query = select(Article).options(
        selectinload(Article.category),
        selectinload(Article.author),
        selectinload(Article.tags)
    ).where(Article.id == article.id)
    result = await db.execute(query)
    return result.scalar_one()


@router.put("/{article_id}", response_model=ArticleResponse)
async def update_article(
    article_id: int,
    article_data: ArticleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = select(Article).options(
        selectinload(Article.category),
        selectinload(Article.author),
        selectinload(Article.tags)
    ).where(Article.id == article_id)
    result = await db.execute(query)
    article = result.scalar_one_or_none()
    
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")
    
    # 权限检查：只有作者或管理员可以修改文章
    if article.author_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="无权修改此文章")
    
    # Update fields
    update_data = article_data.model_dump(exclude_unset=True)
    
    if "tags" in update_data:
        tags_data = update_data.pop("tags")
        tag_ids = [t["id"] for t in tags_data] if tags_data else []
        if tag_ids:
            result = await db.execute(select(Tag).where(Tag.id.in_(tag_ids)))
            article.tags = list(result.scalars().all())
        else:
            article.tags = []
    
    for field, value in update_data.items():
        setattr(article, field, value)
    
    await db.flush()
    await db.refresh(article)
    return article


@router.delete("/{article_id}")
async def delete_article(
    article_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Article).where(Article.id == article_id))
    article = result.scalar_one_or_none()
    
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")
    
    # 权限检查：只有作者或管理员可以删除文章
    if article.author_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="无权删除此文章")
    
    await db.delete(article)
    return {"message": "删除成功"}
